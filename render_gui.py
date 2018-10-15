import bpy

class ND_render_panel(bpy.types.Panel):
    bl_idname = "nd_render_panel"
    bl_label = "Nd Management"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    #bl_category = "category"
    

    def draw(self, context):
        layout = self.layout
        
        row=layout.row()
        row.operator("nd.save_render_settings", icon='DISK_DRIVE')
        row.operator("nd.render_settings", icon='LOAD_FACTORY')
        row=layout.row()
        row.operator("nd.open_settings_folder", icon='FILE_FOLDER')
        row.operator("nd.open_shot_folder", icon='FILE_FOLDER')
        row=layout.row()
        row.operator("nd.create_shot_folders", icon='NEWFOLDER')
        row.operator("nd.play_shot", icon='PLAY')