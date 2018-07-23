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


def copyDiffFiles(srcRootDir, destRootDir, copyUpdates=True):
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
#             print(fullpath)       
        for f in srcfiles:
            fullpath = os.path.join(srcrootdir, f)
            srcfn += 1
            srcf[srcfn] = fullpath
#             print(fullpath)
#     print("src file numbers", srcfn)        

#     print("des files:")        
    for desrootdir, desdir, desfiles in os.walk(destRootDir):
        for folder in desdir:
            fullpath = os.path.join(srcrootdir, folder)
            desfn += 1
            desf[desfn] = fullpath
#             print(fullpath)
        for f in desfiles:
            fullpath = os.path.join(desrootdir, f)
            desfn += 1
            desf[fullpath] = desfn
#             print(fullpath)
#     print("des file numbers", desfn) 
    
    i = 1    
    while(i <= srcfn):
#         print("before replace: ", srcf[i])
        des = srcf[i].replace(srcRootDir, destRootDir)
#         print("after replace: ", srcf[i])

#         check if this file already exits, check if key exist need to use in
        if des in desf:
#             check if src file is updated than des file.
            des_stat = os.stat(des)
            src_stat = os.stat(srcf[i]) 
            
            if(copyUpdates == True):
                if(des_stat.st_mtime < src_stat.st_mtime):
                    shutil.copyfile(srcf[i], des)
                    print("copied ", srcf[i])
            i += 1
            continue
        
#         if directory not exist, create the directory
        if os.path.isdir(srcf[i]):
            if not os.path.exists(des):
                os.makedirs(des)
        else:
            shutil.copyfile(srcf[i], des)
#           shutil.copy(srcf[i], des)
            print("copied ", srcf[i])
        i += 1 
    print("all copied.")

def edit_distance(str1, str2):
# compare two text strings, find Longest Common Subsequence (LCS) problem
# using Levenshtein distance
    data = [[]] #empty 2D array
    cost = 0
    
    for i in range(0, len(str1), 1):
        data[i][0] = i
    for j in range(0, len(str2), 1):
        data[0][j] = j
        
    for i in range(1, len(str1), 1):
        for j in range(1, len(str2), 1):
            if(str1[i]==str2[j]):
                cost = 0
            else:
                cost = 1
                data[i][j] = min(data[i-1][j] +1, #delete 
                                 data[i][j-1] + 1, #insert
                                 data[i-1][j-1] + cost) #replace


def lcs_recursive(X, Y, m, n):
# LCS Problem Statement: Given two sequences, find the length of longest subsequence present in both of them
# Let the input sequences be X[0..m-1] and Y[0..n-1] of lengths m and n respectively. And let L(X[0..m-1], Y[0..n-1]) be the length of LCS of the two sequences X and Y. Following is the recursive definition of L(X[0..m-1], Y[0..n-1]).
# If last characters of both sequences match (or X[m-1] == Y[n-1]) then
# L(X[0..m-1], Y[0..n-1]) = 1 + L(X[0..m-2], Y[0..n-2])
# If last characters of both sequences do not match (or X[m-1] != Y[n-1]) then
# L(X[0..m-1], Y[0..n-1]) = MAX ( L(X[0..m-2], Y[0..n-1]), L(X[0..m-1], Y[0..n-2])
    if m == 0 or n == 0:
        return 0;
    elif X[m-1] == Y[n-1]:
        return 1 + lcs(X, Y, m-1, n-1);
    else:
        return max(lcs(X, Y, m, n-1), lcs(X, Y, m-1, n));

def lcs(X , Y):
# LCS Problem Statement: Given two sequences, find the length of longest subsequence present in both of them
# Let the input sequences be X[0..m-1] and Y[0..n-1] of lengths m and n respectively. And let L(X[0..m-1], Y[0..n-1]) be the length of LCS of the two sequences X and Y. Following is the recursive definition of L(X[0..m-1], Y[0..n-1]).
# If last characters of both sequences match (or X[m-1] == Y[n-1]) then
# L(X[0..m-1], Y[0..n-1]) = 1 + L(X[0..m-2], Y[0..n-2])
# If last characters of both sequences do not match (or X[m-1] != Y[n-1]) then
# L(X[0..m-1], Y[0..n-1]) = MAX ( L(X[0..m-2], Y[0..n-1]), L(X[0..m-1], Y[0..n-2])
    # find the length of the strings
    m = len(X)
    n = len(Y)
 
    # declaring the array for storing the dp values
    L = [[None]*(n+1) for i in range(m+1)]
 
    """Following steps build L[m+1][n+1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0 :
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1]+1
            else:
                if L[i-1][j] > L[i][j-1]:
                    L[i][j] = L[i-1][j]
                else:
                    L[i][j] = L[i][j-1]
#                 L[i][j] = max(L[i-1][j], L[i][j-1])
 
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]
#end of function lcs
           
def main():
#     root_dir = "E:\\5.Ethan\\English Video\\new"
#     print(root_dir)
#     remove_duplicate_files(root_dir)
#     printfilenames(root_dir, "mkv")
#     rename_files(root_dir)
#     copyDiffFiles("\\\\10.0.0.99\\d\\1.Kevin\\TakeAway","E:\\Lenovo Work PC Backup\\TakeAway", True)
    copyDiffFiles("E:\\111","E:\\222", True)
#     longestLen = lcs("abcdefg", "egx")
#     print(longestLen)

if __name__ == "__main__":
    main()