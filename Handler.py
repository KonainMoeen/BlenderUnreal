"""
Handles all the file handling and export/import process
"""
import os,subprocess

backendpath = "C:/UnrealPlugin"

FILE = backendpath + "/PathFile.txt"
UE_CMD =r""
PROJECT =r""
    
# Fetches the path from PathFile
def FetchPath():
    pathInFile=['','','']
    try:
        with open(FILE, "r") as f:
            lines = f.readlines()
            pathInFile[0] = lines[0].split("=",1)[-1].strip()
            pathInFile[1] = lines[1].split("=",1)[-1].strip()
            pathInFile[2] = lines[2].split("=",1)[-1].strip()
        return pathInFile
    except:
        print("Text File Not Found or File is Missing Data")
        return pathInFile

    
# Saves the new path in file for future reference
def savePathInFile(path, line):
    try:
        fin = open(FILE, 'r')
        lines = fin.readlines()
        lines[line] = path
        fin.close()
        
        fout = open(FILE, 'w')
        fout.writelines(lines)
        fout.close()
    except:
        print("Error Saving paths to file")
        
# Runs the Commandline argument for the UE Imports
def Execute(): 
   
    if UE_CMD=="":
        print("Unreal Path Error. Check README for more info")
        return
        
    if PROJECT=="":
        print("Path to Unreal Project file is missing. Check README for more info")
        return
        
    cmd = subprocess.run( r'"{}" "{}" -run=pythonscript -script="{}/UnrealImport.py"'.format(UE_CMD,PROJECT,backendpath), shell= True)
    
# Deletes the temporary assets in tempExports folder
def DeleteTempAssets():
    folder = backendpath + '/tempExports'
    myfiles = os.listdir(folder)
    for file in myfiles:
            os.unlink(folder+ '/' + file)    
    
# Exports the temporary assets in tempExports folder 
def ExportTempAssets():
    import bpy
    from . import getAssetPrefix

    view_layer = bpy.context.view_layer

    obj_active = view_layer.objects.active
    selection = bpy.context.selected_objects

    bpy.ops.object.select_all(action='DESELECT')

    for obj in selection:

        obj.select_set(True)
        # some exporters only use the active object
        view_layer.objects.active = obj
        name = bpy.path.clean_name(obj.name)
        bpy.ops.export_scene.fbx(filepath=backendpath + '/tempExports/' + getAssetPrefix() + name + ".fbx", use_selection=True)

        # Can be used for multiple formats
        # bpy.ops.export_scene.x3d(filepath=fn + ".x3d", use_selection=True)
        obj.select_set(False)

    # To Reselect the objects selected in the first place after export
    for obj in selection:
        obj.select_set(True)

    view_layer.objects.active = obj_active
    
# Gets the path of Cmd and Project right: used right when the export button is clicked
def SendPaths(ProjectPath):
    global PROJECT, UE_CMD
    
    PROJECT = ProjectPath

    from . import UnrealPath
    upath = UnrealPath.GetUnrealCMD()
    
    if upath:
        savePathInFile("UE4Editor-Cmd.exe =" + upath + '\n', 0)
        UE_CMD = upath

    
def FindUnrealProjectVersion():
    file = PROJECT
    lines = []
    version = ""

    fin = open(file, 'r')
    lines = fin.readlines()
    fin.close()
    
    for line in lines:
        if line.lstrip().startswith("\"EngineAssociation"):
            version = line.split(':')[1].strip()
        
    return version[1:5]


def EnablePythonPlugin():
    import json
    file = PROJECT
    plugindata = {
    'Name': 'PythonScriptPlugin', 
    'Enabled': True
    }
    with open(file) as json_file: 
        data = json.load(json_file) 
        
        if 'Plugins' in data.keys():
            for item in data['Plugins']:
                if item['Name'] == 'PythonScriptPlugin':
                    return
        else:
            data['Plugins'] = []

        data['Plugins'].append(plugindata) 
        
    with open(file,'w') as f: 
        json.dump(data, f, indent=4) 
        
