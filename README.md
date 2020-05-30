# Folder Watcher

Watch a folder and automatically sort out all files with same extensions from specific folder to a group of new folders

## Getting Started

Just start the gui.pyw. 
A GUI will open where you can select a Folder to watch.
The programm will automatically start.

### Prerequisites

What things you need to install the software and how to install them

1. You need Python3+ in order to work with the scripts
If not installed, download python on the latest website:
[https://www.python.org/downloads/]


2. You need 1 extra libraries to work with the script

Pystray: Allows the usage of an Icon Tray on Windows and works with Tkinter

```
pip install pystray
```


### Running

Open the gui.pyw which will open the programm.
If you need want to have the exe, you can download it through this link: [here](https://drive.google.com/file/d/11m_ARY4-j1bStRjN3q6JbxhQ0AfZkOzd/view?usp=sharing)

Unpack the Folder_Watcher.rar file in your personal Folder and doubleclick FdW.exe to start the programm


### Additional Functions

If you want to change the possibilty to sort the files, just change the line in Handler.py

```
f.sortbyGroup(path)
```

to you specifig algorithm in FileLib
By default the sort alrigthm is sortbyGroup

```
# sort files by given file groups and copy them into group folder
def sortbyGroup(path):
    list = getListofFileswPath(path)
    for file in list:
        if os.path.exists(file):
            if getFileExt(file) in valid_images:
                folderpath = createFolder(os.curdir, VALID_IMG)
                copyFile(getFileName(file), folderpath)
                removeFile(file)
            elif getFileExt(file) in valid_archiv:
                folderpath = createFolder(os.curdir, VALID_ARCHIV)
                copyFile(getFileName(file), folderpath)
                removeFile(file)
            elif getFileExt(file) in valid_exe:
                folderpath = createFolder(os.curdir, VALID_EXE)
                copyFile(getFileName(file), folderpath)
                removeFile(file)
            elif getFileExt(file) in valid_tf:
                folderpath = createFolder(os.curdir, VALID_TF)
                copyFile(getFileName(file), folderpath)
                removeFile(file)
            elif getFileExt(file) in valid_pres:
                folderpath = createFolder(os.curdir, VALID_PRES)
                copyFile(getFileName(file), folderpath)
                removeFile(file)

            elif getFileExt(file) in valid_videos:
                folderpath = createFolder(os.curdir, VALID_VIDEOS)
                copyFile(getFileName(file), folderpath)
                removeFile(file)

            elif getFileExt(file) in valid_spread:
                folderpath = createFolder(os.curdir, VALID_SPREAD)
                copyFile(getFileName(file), folderpath)
                removeFile(file)
            else:
                folderpath = createFolder(os.curdir, OTHER)
                copyFile(getFileName(file), folderpath)
                removeFile(file)
```

Another way to sort the files is also included in the FileLib.py.
It sorts all the files in the Folder and create new folder with the name extensions.

```
# sort files by their file extension and copy them into new folder
def sortbyext(path):
    list = getListofFileswPath(path)
    for file in list:
        if os.path.exists(file):
            if getFileExt(file) in valid_images:
                folderpath = createFolder(os.curdir, getFileExt(file))
                copyFile(getFileName(file), folderpath)
                removeFile(file)

```
