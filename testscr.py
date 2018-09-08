import os

class runFolder:
    def runfolder(self,folderpath):
        filenames = os.listdir(folderpath)  # get all files' and folders' names in the current directory
        xml = []
        jpg = []
        for filename in filenames:  # loop through all the files and folders
            #Listing the separate xml and jpg files
            if(filename.find(".xml") != -1):
                xml.append(filename)
            elif(filename.find(".jpg") != -1):
                jpg.append(filename)

        # Sorting the files
        xml.sort()
        jpg.sort()

        result = list(zip(xml,jpg))
        return(result)