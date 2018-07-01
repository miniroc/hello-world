'''
'''
import os

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
    #creating an empty dictionary or use "di = dict()" to creat an empty dictionary
    di = {}
    
    root_dir_files_tuple = os.walk(root_dir)
#     print("\!")
#     print("!")
    # check if an object is empty use if(not obj), do not use len(obj)
    if(root_dir_files_tuple): 
        print("walked through files")
    
    for root, dirs, files in root_dir_files_tuple:
        for f in files:
            fname = f[:-16] + f[-4:]
            fname = fname.replace("&", "-")
            fname = fname.replace("!", "")
            fname = fname.replace(" ", "")
            fname = fname.replace(",", "")
            fname = fname.replace("\'", "")
#             print(fname+"\n")
            os.rename(root+"\\"+f, root+"\\"+fname)
#             print(root+"\\"+fname)
      
def printfilenames(root, extension):
    with open("E:\\5.Ethan\\English Video\\mp42mp3.bat", "w") as outf:
        for rootdir, dir, files in os.walk(root):
            for f in files:
                fnamesplit = f.split(".")
    #             print(fnamesplit[len(fnamesplit)-1])
                
                if(fnamesplit[len(fnamesplit)-1] == extension):
                    fname = f[:-4]
#                     print("file name is: " + fname)
#                     print("ffmpeg -i \"{0}\" -vn -acodec copy \"{1}.mp3\"".format(f, fname))
                    outf.write("ffmpeg -i \"{0}\" -vn -acodec libmp3lame \"{1}.mp3\"\n".format(f, fname))
    

def main():
    root_dir = "E:\\5.Ethan\\English Video"
    print(root_dir)
#     remove_duplicate_files(root_dir)
#     printfilenames(root_dir, "mp4")
    rename_files(root_dir)


if __name__ == "__main__":
    main()