import bpy

class ND_an_offset_indexpy(bpy.types.Operator):
    bl_idname = "nd.an_offset_index"
    bl_label = "Offset AN Index"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    
    prop_to_offset=bpy.props.StringProperty(default="Index", name="Prop Name")
    offset=bpy.props.IntProperty(name="Offset")

    @classmethod
    def poll(cls, context):
        chk=0
        for ob in bpy.context.scene.objects:
            if ob.select==True:
                chk=1
        return chk==1
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=300, height=100)
    
    def check(self, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "prop_to_offset")
        layout.prop(self, "offset")
        

    def execute(self, context):
        
        customprop="AN*Integer*"+self.prop_to_offset
        
        for ob in bpy.context.scene.objects:
            if ob.select==True:
                try:
                    old_idx=ob[customprop]
                    ob[customprop]=old_idx+self.offset
                    print("AN Offset --- "+ob.name+" offset ok")
                except:
                    print("AN Offset --- "+'Error on '+ob.name)
                    pass
                
        return {"FINISHED"}
        