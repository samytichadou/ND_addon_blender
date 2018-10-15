import bpy
import os

from .misc_functions import return_shot_infos_from_path, suppress_files_in_folder, activate_metadatas, activate_stamp_metadatas, create_folder
from .render_settings_functions import read_json, apply_render_settings_from_dataset

class ND_render_settings(bpy.types.Operator):
    bl_idname = "nd.render_settings"
    bl_label = "Set Render Settings"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    index=bpy.props.IntProperty(min=0, default=0)
    
    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved==True and context.scene.camera is not None
    
    def invoke(self, context, event):
        winman=bpy.data.window_managers['WinMan']
        prop=winman.nd_props[0]
        
        blend_path=bpy.data.filepath
        blend_name=os.path.splitext(os.path.basename(blend_path))[0]
        shot, cat, dir=return_shot_infos_from_path(blend_path)
        render_folder=os.path.join(os.path.join(dir, "006_MISC"), "000_RENDER_SETTINGS")
        
        #erase list
        custompath=clear_coll_prop(prop.render_coll)
        
        #create new list
        create_render_settings_props(render_folder, prop.render_coll)

        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=500, height=100)
    
    def check(self, context):
        return True
    
    def draw(self, context):
        winman=bpy.data.window_managers['WinMan']
        prop=winman.nd_props[0]
        
        layout = self.layout
        layout.template_list("NDUIList", "", prop, "render_coll", self, "index", rows=5)

    def execute(self, context):
        scn=bpy.context.scene
        rd=scn.render
        pct=self.proxy_percentage
        coef=pct/100
        blend_path=bpy.data.filepath
        blend_name=os.path.splitext(os.path.basename(blend_path))[0]
        name=blend_name+"_"+scn.name+"_"+scn.camera.name
        
        prefix="RENDER_SETTINGS_"
        
        #get shot number
        shot, cat, dir=return_shot_infos_from_path(blend_path)
    
        name_sc=prefix+blend_name+"_"+scn.name+".json"
        name_cam=prefix+blend_name+"_"+scn.name+"_"+scn.camera.name+".json"
        json_sc=os.path.join(os.path.join(dir, "006_MISC"), name_sc)
        json_cam=os.path.join(os.path.join(dir, "006_MISC"), name_cam)
        
        if os.path.isfile(json_cam):
            json_file=json_cam
        elif os.path.isfile(json_sc):
            json_file=json_sc
        else:
            json_file=""

        #general settings
        activate_metadatas()
        
        rd.use_file_extension = True
        rd.use_render_cache = False
        rd.use_freestyle = False
        rd.use_motion_blur = False
        
        #relative path
        if self.state!='2' and self.relative==True:
            bpy.ops.file.make_paths_relative()
        
        #playblast
        if self.state=='2':
            tmp=os.path.join(dir, "004_PLAYBLAST")
            playblast_path=os.path.join(tmp, name)
            abs_filepath=os.path.join(playblast_path, name+"_PLAYBLAST_####")
            #create folder if needed
            create_folder(playblast_path)
            
            rd.image_settings.file_format = 'PNG'
            rd.image_settings.color_mode = 'RGBA'
            rd.image_settings.compression = 15
            rd.image_settings.color_depth = '8'
            rd.resolution_percentage = pct
            #rd.use_overwrite = True
            activate_stamp_metadatas()

        #proxy
        elif self.state=='1':
            tmp=os.path.join(os.path.join(dir, "005_RENDER"), "PROXYS")
            proxy_path=os.path.join(tmp, name)
            abs_filepath=os.path.join(proxy_path, name+"_RENDER_PROXY_####")
            #create folder if needed
            create_folder(proxy_path)
            
            #suppress previous render if needed
            if self.suppress_previous==True:
                suppress_files_in_folder(proxy_path)
            #get render settings
            #get render layer and passes
            rd.resolution_percentage = pct
            old=scn.cycles.samples
            old_aa=scn.cycles.aa_samples
            scn.cycles.samples = old*coef
            scn.cycles.aa_samples = old_aa*coef
            rd.use_stamp=False

        #render
        elif self.state=='0':
            tmp=os.path.join(os.path.join(dir, "005_RENDER"), "MASTERS")
            render_path=os.path.join(tmp, name)
            abs_filepath=os.path.join(render_path, name+"_RENDER_MASTER_####")
            #create folder if needed
            create_folder(render_path)
            
            #suppress previous render if needed
            if self.suppress_previous==True:
                suppress_files_in_folder(render_path)
            #get render settings
            #get render layer and passes
            rd.resolution_percentage = 100
            rd.use_stamp=False
            
        rd.filepath=bpy.path.relpath(abs_filepath)
        
        if self.state!='2' and json_file!="":
            datas=read_json(json_file)
            apply_render_settings_from_dataset(datas)
            inf="ND - settings loaded"
            print(inf)
            self.report({'INFO'}, inf)
            
        if self.state!='2' and json_file=="":
            inf="ND - no existing settings for this shot"
            print(inf)
            self.report({'WARNING'}, inf)
        return {"FINISHED"}