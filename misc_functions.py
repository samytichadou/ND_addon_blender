import bpy
import os
import platform
import subprocess

from .prefs import get_addon_preferences

#create prop if doesn't exist
def create_prop():
    winman=bpy.data.window_managers['WinMan']
    try:
        prop=winman.nd_props[0]
        return(prop)
    except IndexError:
        new=winman.nd_props.add()
        return(new)
        
#find folder from filebrowser
def find_folder_filebrowser():
    prefs=get_addon_preferences()
    prefs_folder=prefs.prefs_folderpath
    
    winman=bpy.data.window_managers['WinMan']
    prop=winman.nd_props[0]
    shot=str(prop.shot_index).zfill(2)
    
    shot_folder_file=os.path.join(prefs_folder, 'shots_folder.txt')
    f = open(shot_folder_file,"r") 
    shot_folder=f.read()
    
    shot=os.path.join(shot_folder, shot)
    
    if os.path.isdir(shot):
        return (shot)
    else:
        return('')
    
#update function for filebrowser shot
def update_folderpath_shot(self, context):
    area=context.area
    
    folder=find_folder_filebrowser()
    #change directory
    if folder!='':
        area.spaces[0].params.directory=convert_windowspath_to(folder)
        
#update function for filebrowser custom path
def update_folderpath_path(self, context):
    winman=bpy.data.window_managers['WinMan']
    prop=winman.nd_props[0]
    
    area=context.area
    try:
        folder=prop.dirpath_coll[prop.path_index]
        area.spaces[0].params.directory=convert_windowspath_to(folder.path)
    except IndexError:
        pass
        
#get content of txt file
def get_content_txt(filepath):
    f = open(filepath,"r") 
    content=f.read()
    return (content)

#clear collection prop
def clear_coll_prop(prop):
    if len(prop)>=1:
        for i in range(len(prop)-1,-1,-1):
            prop.remove(i)
    return(prop)

#find os
def convert_windowspath_to(windows_path):
    if platform.system()=='Darwin':
        newpath=windows_path.replace('\\\\motionorama\\', '/Volumes/').replace('\\', '/')
    elif platform.system()=='Linux':
        newpath=windows_path.replace('\\\\motionorama\\', '/mnt/').replace('\\', '/')
    elif platform.system()=='Windows':
        newpath=windows_path
    return(newpath)

#create custom path from path and prop
def create_custom_path_props(path, prop):
    for f in os.listdir(path):
        new=prop.add()
        new.name=f.split('.txt')[0]
        new.path=get_content_txt(os.path.join(path, f))
        
#open specific folder
def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])