import bpy
import os

from .misc_functions import return_shot_infos_from_path, suppress_files_in_folder, activate_metadatas, activate_stamp_metadatas

class ND_render_settings(bpy.types.Operator):
    bl_idname = "nd.render_settings"
    bl_label = "Render Settings"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    possible_states = [
                ("0","Render","Render"),
                ("1","Render proxy","Render proxy"),
                ("2","Playblast","Playblast"),
                ]
    state= bpy.props.EnumProperty(name="State", default="1", items=possible_states)
    proxy_percentage = bpy.props.IntProperty(name="Proxy Percentage", default=50, min=5, max=95)
    suppress_previous=bpy.props.BoolProperty(name="Suppress previous render", default=False)
    relative=bpy.props.BoolProperty(name="Relative Path", default=False)
    
    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved==True and context.scene.camera is not None
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=500, height=100)
    
    def check(self, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "state")
        row=layout.row()
        row.prop(self, "suppress_previous")
        if self.state!='2':
            row.prop(self, "relative")
        if self.state!='0':
            layout.prop(self, 'proxy_percentage')

    def execute(self, context):
        scn=bpy.context.scene
        rd=scn.render
        pct=self.proxy_percentage
        coef=pct/100
        blend_path=bpy.data.filepath
        blend_name=os.path.splitext(blend_path)[0]
        name=blend_name+"_"+scn.name+"_"+scn.camera.name
        
        #get shot number
        shot, cat, dir=return_shot_infos_from_path(blend_path)
    
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
            #create folder if needed
            playblast_path=os.path.join(dir, os.path.join("004_PLAYBLAST", name))
            rd.filepath=os.path.join(playblast_path, name+"_PLAYBLAST_####")
            
            rd.image_settings.file_format = 'PNG'
            rd.image_settings.color_mode = 'RGBA'
            rd.image_settings.compression = 15
            rd.image_settings.color_depth = '8'
            rd.resolution_percentage = pct
            #rd.use_overwrite = True
            activate_stamp_metadatas()

        #proxy
        elif self.state=='1':
            #create folder if needed
            proxy_path=os.path.join(dir, os.path.join(os.path.join("005_RENDER","PROXY"), name))
            rd.filepath=os.path.join(proxy_path, name+"_RENDER_PROXY_####")
            
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
            #create folder if needed
            render_path=os.path.join(dir, os.path.join(os.path.join("005_RENDER","MASTERS"), name))
            rd.filepath=os.path.join(render_path, name+"_RENDER_MASTER_####")
            
            #suppress previous render if needed
            if self.suppress_previous==True:
                suppress_files_in_folder(render_path)
            #get render settings
            #get render layer and passes
            rd.resolution_percentage = 100
            rd.use_stamp=False
        
        return {"FINISHED"}