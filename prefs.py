import bpy
import os

addon_name = os.path.basename(os.path.dirname(__file__))

class VCacheAddonPrefs(bpy.types.AddonPreferences):
    bl_idname = addon_name
    
    prefs_folderpath = bpy.props.StringProperty(
            name="Preferences Folder Path",
            default=r"\\motionorama\MOTIONORAMA_DRIVE\----ELEMENTS\BLENDER\ne_pas_toucher_blender_common_scripts\config\notre_dame_prefs",
            description="Folder where Prefs Files will be stored",
            subtype="DIR_PATH",
            )
            
    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'prefs_folderpath')
        

# get addon preferences
def get_addon_preferences():
    addon = bpy.context.user_preferences.addons.get(addon_name)
    return getattr(addon, "preferences", None)