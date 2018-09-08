import os


folderpath = "/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/smalloutput/neg/images"
filenames = os.listdir(folderpath)  # get all files' and folders' names in the current directory
print("Folder path in test>>", folderpath)
print("LENGTH >>", len(filenames))
filenames.sort()
print(filenames)
str = "/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/smalloutput/neg/images/"
f = open('/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/smalloutput/neg/negdat.txt', 'a')
for filename in filenames:  # loop through all the files and folders
    temp = str + filename
    f.write(temp)
    f.write("\n")


f.close()