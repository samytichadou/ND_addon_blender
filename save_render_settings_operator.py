import bpy
import os

from .misc_functions import return_shot_infos_from_path, suppress_file
from .render_settings_functions import format_render_settings_info, create_json

class ND_save_render_settings(bpy.types.Operator):
    bl_idname = "nd.save_render_settings"
    bl_label = "Save Render Settings"
    bl_description = ""
    bl_options = {"REGISTER"}
    
    name=bpy.props.StringProperty(name='Preset Name', default='')

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved==True
    
    def invoke(self, context, event):
        scn=context.scene
        blend_path=bpy.data.filepath
        blend_name=os.path.splitext(os.path.basename(blend_path))[0]
        
        prefix="RENDER_SETTINGS_"
        
        try:
            name_temp=prefix+blend_name+"_"+scn.name+"_"+scn.camera.name
        except AttributeError:
            name_temp=prefix+blend_name+"_"+scn.name
                    
        self.name=name_temp
        
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400, height=100)
    
    def check(self, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name")

    def execute(self, context):
        scn=context.scene
        blend_path=bpy.data.filepath
        blend_name=os.path.splitext(os.path.basename(blend_path))[0]
    
        shot, cat, dir=return_shot_infos_from_path(blend_path)
        
        prefix="RENDER_"
        
        json_file=os.path.join(os.path.join(dir, "006_MISC"),self.name+".json")
            
        #check json exists or not
        if os.path.isfile(json_file):
            #delete if exists
            suppress_file(json_file)
        #save
        if json_file!="":
            datas=format_render_settings_info()
            create_json(json_file, datas)
            
            inf="ND - json created"
            print(inf)
            self.report({'INFO'}, inf)
        else:
            inf="ND - no camera in the scene"
            print(inf)
            self.report({'WARNING'}, inf)
        
        return {"FINISHED"}
        