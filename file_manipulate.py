'''
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import shutil

def remove_duplicate_files(root_dir):
    #creating an empty dictionary or use "di = dict()" to creat an empty dictionary
    di = {}
    
    root_dir_files_tuple = os.walk(root_dir)
    
    # check if an object is empty use if(not obj), do not use len(obj)
    if(root_dir_files_tuple): 
        print("walked through files")
    
    for root, dirs, files in root_dir_files_tuple:
        for f in files:
            fnamesplit = f.split('.')
            if(len(fnamesplit) != 2): #file name contains '.' other than the one before extension, skip it
                continue
            
            if(fnamesplit[0] in di.keys()):
                if(fnamesplit[1] == "webm"): # remove webm duplicate file
                    os.remove(os.path.join(root,f))
                    print("Removed "+ f )
            
                if(di[fnamesplit[0]] == "mp4"): # left mp4 file, remove other duplicate format
                    os.remove(os.path.join(root,f))
                    print("Removed "+f)
                
                if(fnamesplit[1] == "mp4"): # if current is mp4 and dictionary store is other format, delete other format
                    print(f)
                    os.remove(os.path.join(root, fnamesplit[0] + "." + di[fnamesplit[0]]))
                    di[fnamesplit[0]] = fnamesplit[1]
                    print("Removed " + os.path.join(root, fnamesplit[0] + "." + di[fnamesplit[0]]))
            else:
                di[fnamesplit[0]] = fnamesplit[1]

def rename_files(root_dir):
    root_dir_files_tuple = os.walk(root_dir)
#     print("\!")
#     print("!")
    # check if an object is empty use if(not obj), do not use len(obj)
    if(root_dir_files_tuple): 
        print("walked through files")
    
    for root, dirs, files in root_dir_files_tuple:
        for f in files:
#             fname = f[:-16] + f[-4:]
            fname = f
            fname = fname.replace("&", "-")
            fname = fname.replace("!", "")
            fname = fname.replace(" ", "")
            fname = fname.replace(",", "")
            fname = fname.replace("\'", "")
            fname = fname.replace("+", "")
#             print(fname+"\n")
            os.rename(root+"\\"+f, root+"\\"+fname)
#             print(root+"\\"+fname)
      
def printfilenames(root, extension):
    with open("E:\\5.Ethan\\English Video\\new\\mp42mp3.bat", "w") as outf:
        for rootdir, dir, files in os.walk(root):
            for f in files:
                fnamesplit = f.split(".")
    #             print(fnamesplit[len(fnamesplit)-1])
                
                if(fnamesplit[len(fnamesplit)-1] == extension):
                    fname = f[:-4]
#                     print("file name is: " + fname)
#                     print("ffmpeg -i \"{0}\" -vn -acodec copy \"{1}.mp3\"".format(f, fname))
                    outf.write("ffmpeg -i \"{0}\" -vn -acodec libmp3lame \"{1}.mp3\"\n".format(f, fname))
    
def recursiveTraverse(RootDir):
    for lists in os.listdir(RootDir):
        path = os.path.join(RootDir, lists)
        print(path)
        if os.path.isdir(path):
            recursiveTraverse(path)


def copyDiffFiles(srcRootDir, destRootDir):
    srcf={}
    srcfn = 0
    desf={}
    desfn = 0
#     record folders and files, record folders first for later folder creation before file inside copy failure
    for srcrootdir, srcdir, srcfiles in os.walk(srcRootDir):
        for folder in srcdir:
            fullpath = os.path.join(srcrootdir, folder)
            srcfn += 1
            srcf[srcfn] = fullpath
            print(fullpath)       
        for f in srcfiles:
            fullpath = os.path.join(srcrootdir, f)
            srcfn += 1
            srcf[srcfn] = fullpath
            print(fullpath)
    print("src file numbers", srcfn)        

#     print("des files:")        
    for desrootdir, desdir, desfiles in os.walk(destRootDir):
        for folder in desdir:
            fullpath = os.path.join(srcrootdir, folder)
            desfn += 1
            desf[desfn] = fullpath
            print(fullpath)
        for f in desfiles:
            fullpath = os.path.join(desrootdir, f)
            desfn += 1
            desf[fullpath] = desfn
            print(fullpath)
    print("des file numbers", desfn) 
    
    i = 1    
    while(i <= srcfn):
#         print("before replace: ", srcf[i])
        des = srcf[i].replace(srcRootDir, destRootDir)
#         print("after replace: ", srcf[i])

#         check if this file already exits, check if key exist need to use in
        if des in desf:
            i += 1
            continue
        
#         print("des file: ", des)
        if os.path.isdir(srcf[i]):
            if not os.path.exists(des):
                os.makedirs(des)
        else:
            shutil.copyfile(srcf[i], des)
#           shutil.copy(srcf[i], des)
            print("copied ", srcf[i])
        i += 1 

def main():
#     root_dir = "E:\\5.Ethan\\English Video\\new"
#     print(root_dir)
#     remove_duplicate_files(root_dir)
#     printfilenames(root_dir, "mkv")
#     rename_files(root_dir)
    copyDiffFiles("F:\\Coursera","F:\\New folder")

if __name__ == "__main__":
    main()