import bpy

#subdir list
class NDUIList(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, flt_flag):
        layout.label(item.name)

class NDFileBrowserUI(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'
    bl_category = "Bookmarks"
    bl_label = "Notre-Dame"
    
    def draw(self, context):
        layout = self.layout
        
        winman=bpy.data.window_managers['WinMan']
        try:
            prop=winman.nd_props[0]
            layout.prop(prop, 'shot_index')
        except IndexError:
            pass
        
        if len(prop.dirpath_coll)>0:
            layout.template_list("NDUIList", "", prop, "dirpath_coll", prop, "path_index", rows=5)
            
        row=layout.row(align=True)
        row.operator("nd.reload_custom_path", text='Reload', icon='FILE_REFRESH')
        row.operator("nd.open_custom_path_folder", text='Open', icon='FILE_FOLDER')