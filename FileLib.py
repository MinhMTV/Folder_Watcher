import os
from os import walk
from os.path import isfile, join
import pathlib
import timeit
import time
import glob
import re
import shutil

#all Images Extensions
valid_images = ["ase", "art", "bmp", "blp", "cd5", "cit", "cpt", "cr2", "cut", "dds", "dib", "djvu", "egt", "exif", "gif", "gpl", "grf", "icns", "ico", "iff", "jng", "jpeg", "jpg", "jfif", "jp2", "jps",
                "lbm", "max", "miff", "mng", "msp", "nitf", "ota", "pbm", "pc1", "pc2", "pc3", "pcf", "pcx", "pdn", "pgm", "PI1", "PI2", "PI3", "pict", "pct", "pnm", "pns", "ppm", "psb", "psd", "pdd",
                "psp", "px", "pxm", "pxr", "qfx", "raw", "rle", "sct", "sgi", "rgb", "int", "bw", "tga", "tiff", "tif", "vtf", "xbm", "xcf", "xpm", "3dv", "amf", "ai", "awg", "cgm", "cdr", "cmx",
                "dxf", "e2d", "egt", "eps", "fs", "gbr", "odg", "svg", "stl", "vrml", "x3d", "sxd", "v2d", "vnd", "wmf", "emf", "art", "xar", "png", "webp", "jxr", "hdp", "wdp", "cur", "ecw",
                "iff", "lbm", "liff", "nrrd", "pam", "pcx", "pgf", "sgi", "rgb", "rgba", "bw", "int", "inta", "sid", "ras", "sun", "tga"
                ]

#all video Extensions
valid_videos = ["3g2", "3gp", "aaf", "asf", "avchd", "avi", "drc", "flv", "m2v", "m4p", "m4v", "mkv", "mng", "mov", "mp2", "mp4", "mpe", "mpeg", "mpg", "mpv", "mxf", "nsv", "ogg", "ogv", "qt", "rm",
                "rmvb", "roq", "svi", "vob", "webm", "wmv", "yuv"
                ]

#write text to a text_file
#@path path with given text ending e.g ./double/test.txt
#@text can be a list of text or a string
def writeText(path,text):
    isEmpty = True
    text_file = open(path, "a+")
    text_file.seek(0)
    data = text_file.read(100)
    if len(data) > 0:
        isEmpty = False
    if isinstance(text, list):
        for x in text:
            if isEmpty == False:
                text_file.write("\n")
            text_file.write(x)
        text_file.write("\n")
    elif isinstance(text, str):
        if isEmpty == False:
            text_file.write("\n")
        text_file.write(text)
    text_file.close()

#get List w all Folders with path within the given @path
def getListofFolders(path):
    list_subfolders_with_paths = [
        f.path for f in os.scandir(path) if f.is_dir()]
    print("There are " + str(len(list_subfolders_with_paths)) +
          " SubFolder in this Folder")
    print(type(list_subfolders_with_paths))
    for x in list_subfolders_with_paths:
        print(x)

#get List of all the files w/o path within the given @path
def getListofFileswPath(path):
    onlyfiles = [join(path, f) for f in os.listdir(path) if isfile(join(path, f))]
    print("all the files in path")
    temp = len(onlyfiles)
    print(f"{temp} Files exist in Folder and Subfolder")
    print(onlyfiles)
    return onlyfiles

def getListofFileswoPath(path):
    onlyfiles = [f for f in os.listdir(path) if isfile(join(path, f))]
    print("all the files in path")
    temp = len(onlyfiles)
    print(f"{temp} Files exist in Folder and Subfolder")
    print(onlyfiles)
    return onlyfiles

#get current dir, all subfoldernames, all subfoldernames w path,all files w path from given @path
#dirfolders list of all folders with path from given @path
#dirnames list of all foldernames w/o path
#filenames list of all files w/o path
def getFileAndDirPath(path):
    f = []
    f0 = []
    f1 = []
    f2 = []
    f.append(path)
    for (dirfolders, dirnames, filenames) in walk(path):
        if len(dirnames) > 0:
            f0.append(dirnames)
        for y in dirnames:
             f1.append(os.path.join(dirfolders, y))
        for x in filenames:
            f2.append(os.path.join(dirfolders, x))
    f.append(f0)
    f.append(f1)
    f.append(f2)
    return f #[current dir, subdir w/o path,subdir w path, file w path ]

#get all Images w path from given @path
#save every extension images in list and add it to result list
def getAllImages(path):
    f = []
    count = 0
    tic = time.perf_counter()
    for x in valid_images:
        temp = glob.glob(path + '/**/*.' + x, recursive=True)
        if len(temp) > 0:
            f.append(temp)
    toc = time.perf_counter()
    print(f"Get all Images in {toc - tic:0.4f} seconds")
    for lists in f:
        count += len(lists)
    print("There are " + str(count) +
          " Images in this Folder")
    #depends on how many extensions were found
    return f #[[img w jpeg],[img w png]...]

#get the overall Number of Images from the given @path
def getNrofImages(path):
    count = 0
    list = getAllImages(path)
    for x in list:
        count += len(x)
    return count

# my_path/     the dir
# **/       every file and dir under my_path
# *.txt     every file that ends with '.txt'
# check specific extensions and return files with this extensions
def getspecificFileExtension(path):
    files = []
    userExt = input("Which File extensions do you want to check?\n")
    files = glob.glob(path + '/**/*.' + userExt, recursive=True)
    if not files:
        print("no files with " + userExt + " found")
    else:
        for x in files:
            files.append(x)
        print("There are " + str(len(files)) + " Files with ." + userExt)
    reCheck = input("\nDo you want to check other extensions?\nY/N\n")
    if reCheck.lower() == 'y':
        getspecificFileExtension(path)

    elif reCheck.lower() == 'n':
        print("")
    else:
        print("Invalid Input. Please Enter Y / N\n")
        getspecificFileExtension(path)
    return files

# get all Extensions from path
def getAllFileExtension(path):
    ListFiles = walk(path)
    SplitTypes = []
    for walk_output in ListFiles:
        for file_name in walk_output[-1]:
            if file_name.split(".")[-1] not in SplitTypes:
                SplitTypes.append(file_name.split(".")[-1])
    print(SplitTypes)

# get all Extensions from a given List with images with paths
def getAllImageExt(path, ImageList):
    SplitTypes = []
    for images in ImageList:
        for file_name in images:
            if file_name.split(".")[-1] not in SplitTypes:
                SplitTypes.append(file_name.split(".")[-1])
    print(SplitTypes)

#get file extension from given filepath or name
def getFileExt(path):
    file_ext = path.split(".")[-1]
    return file_ext


# find all duplicates which has Indicator at the end e.g (1)
def findDuplicateImagesByInd(path,ImageList,indicator):
    duImageList = []
    for images in ImageList:
        for filepath in images:
            pos = filepath.rfind(".")
            if indicator in filepath[len(filepath[:pos])-len(indicator):pos]:
                duImageList.append(filepath)
    print("There are " + str(len(duImageList)) +
          " duplicate Images in this Folder")
    return duImageList

def createFolder(path,FolderName):
    copyFolderPath = os.path.join(path,FolderName)
    if os.path.isdir(copyFolderPath):
        print("folder already exist")
    else:
        os.mkdir(copyFolderPath)
    return copyFolderPath

#@ImgList all Images in List with path
#@DuList duplicateImages with path
#@newDirPath Dirpath where new Folder for Copies is created
#@FolderName folderName for new Folder
#@filewOrg fileList w Original
#returns path w new folder & all the duplicate file paths
def copyFiles(newDirPath,FolderName,DuList,ImgList,Indicator,filewOrg):
    copy = []
    copyFolderPath = os.path.join(newDirPath,FolderName)
    cnt_new = 0
    cnt_exist = 0
    destImgList = []
    scrImgList = []
    doubleImg = []
    if os.path.isdir(copyFolderPath):
        print("folder already exist")
    else:
        os.mkdir(copyFolderPath)

#filenames duplicateImagesName without path
    fileNames = getFileName(DuList)
    tic = time.perf_counter()
    destFolderImg = getAllImages(copyFolderPath)

    for Image in destFolderImg:
        for x in Image:
            destImgList.append(x)
    for x in filewOrg[0]:
        if getFileName(x) not in doubleImg:
            if len(destImgList) > 0:
                    if getFileName(x) in getFileName(destImgList):
                        doubleImg.append(getFileName(x))
                        cnt_exist += 1
                    else:
                        doubleImg.append(getFileName(x))
                        copyFile(x,copyFolderPath)
                        cnt_new += 1
            else:
                doubleImg.append(getFileName(x))
                copyFile(x,copyFolderPath)
                cnt_new += 1

    toc = time.perf_counter()
    print("These duplicates dont have an original file\n")
    print(filewOrg[1])
    print(f"\nCopy Files took {toc - tic:0.4f} seconds")
    print(f"{cnt_new} New Files were copied")
    print(f"{cnt_exist} Files already existed")
    print(f"{getNrofImages(copyFolderPath)} total Images are in the directory\n")
    copy = [copyFolderPath,filewOrg,[cnt_new,cnt_exist]]
    return copy

#copy a file by given src path to destination path
def copyFile(file,destpath):
    try:
        shutil.copy(file,destpath)
        print(file)

# If source and destination are same
    except shutil.SameFileError:
        print("Source and destination represents the same file.")

# If there is any permission issue
    except PermissionError:
        print("Permission denied.")

# # For other errors
    except:
        print("Error occurred while copying file.")

def removeFile(rmFile):
    os.remove(rmFile)

#remove file by provided FileList
def removeFiles(rmFileList):
    for x in rmFileList:
        os.remove(x)
        print("remove following files")
        print(x)

#check if original file is in the same folder than duplicate
def checkDupInSameFold(duList, fileList, indicator):
    dupList = []
    dupwOrg =  []
    for dup in duList:
        duExt = "." + getFileName(dup).split(".")[-1]
        dutemp = getFileName(dup)[:-len(indicator)-len(duExt)]
        dutemp = dutemp.strip() + duExt
        for x in fileList:
            if getFileName(x) == dutemp:
                if x.replace(getFileName(x),'') == dup.replace(getFileName(dup),''):
                     dupwOrg.append(dup)
#                     print("original file is in same folder")

    dupList = [dupwOrg,[x for x in duList if x not in dupwOrg]]
    temp = len(dupList[1])
    print(f"{temp} duplicate Files are not in the same folder as original")
    print(dupList[1])
    temp = len(dupList[0])
    print(f"{temp} duplicate Files are in the same directory")
    return dupList #[DuplicatePath with Original Files, DuplicateFiles W/o Orginal Files]


#check if file with indicator is really duplicate or if its the only file without original
#duList List of duplicateImages w path
#fileList List of all Img in Folders
def checkDuplicateByEndInd(duList, fileList,indicator):
    dupList = []
    dupwOrg = []
    for dup in duList:
        duExt = "." + getFileName(dup).split(".")[-1] #.jpg
        dutemp = getFileName(dup)[:-len(indicator)-len(duExt)]
        dutemp = dutemp.strip() + duExt #IMAG0046
        for x in fileList:
            if getFileName(x) == dutemp:
                if dup not in dupwOrg:
                    dupwOrg.append(dup)
    dupList = [dupwOrg,[x for x in duList if x not in dupwOrg]]
    return dupList #[DuplicatePath with Original Files, DuplicateFiles W/o Orginal Files]

#get only file name without path
def getFileName(FileList):
    fileNames = []
    if isinstance(FileList, list):
        for x in FileList:
            fileNames.append(os.path.basename(x))
        return fileNames
    elif isinstance(FileList, str):
        return os.path.basename(FileList)
