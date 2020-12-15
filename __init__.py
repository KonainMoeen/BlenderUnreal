import bpy
from . import Handler
    
bl_info = {
    "name": "MayaToUnreal",
    "description": "Connects Blender to Quixel Bridge for one-click imports with shader setup and geometry",
    "author": "Konain",
    "version": (1, 1),
    "blender": (2, 91, 0),
    "location": "File > Import",
    "support": "COMMUNITY",
    "category": "Import-Export"
}   
    
gtools = None    
    
pathInFile = Handler.FetchPath()

project = pathInFile[1]
content = pathInFile[2]

class FileClass(bpy.types.PropertyGroup):
    project_path: bpy.props.StringProperty(name="Unreal Project",
                                        description="This is the path to unreal engine project",
                                        default=project,
                                        maxlen=256,
                                        subtype="FILE_PATH")
                                        
                                        
    content_location: bpy.props.StringProperty(name="Content Location",
                                        description="This is the content location inside the project",
                                        default=content,
                                        maxlen=128
                                        )                                 
    asset_prefix: bpy.props.StringProperty(name="Asset Prefix",
                                        description="This is the prefix name added to the asset name ",
                                        default='',
                                        maxlen=128
                                        )
                                        



class BTU_PT_MainPanel(bpy.types.Panel):
    bl_label = "Blender To Unreal"
    bl_category = "Blender To Unreal"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        global gtools
        gtools = context.scene.gtools
        row.prop(gtools, "project_path")
        row = layout.row()
        row.prop(gtools, "content_location",icon="TOPBAR")
        row = layout.row()
        row.prop(gtools, "asset_prefix", icon="TEXT")
        layout.operator("scene.button_operator", icon="EXPORT")


class ButtonOperator(bpy.types.Operator):
    bl_idname = "scene.button_operator"
    bl_label = "Export To Unreal"

    def execute(self, context):
        
        # Save the project path in file
        Handler.savePathInFile("Project Path =" + gtools.project_path + '\n', 1)
        Handler.savePathInFile("Content Path =" + gtools.content_location + '\n', 2)
    
        Handler.SendPaths(gtools.project_path)
        Handler.DeleteTempAssets()
        Handler.ExportTempAssets()
        Handler.EnablePythonPlugin()
        Handler.Execute()
            
        return {'FINISHED'}


classes = (FileClass, BTU_PT_MainPanel, ButtonOperator)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.gtools = bpy.props.PointerProperty(type=FileClass)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.gtools


def getAssetPrefix():
    return gtools.asset_prefix


if __name__ == "__main__":
    register()