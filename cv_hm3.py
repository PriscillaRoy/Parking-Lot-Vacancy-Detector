"""cv_hw2.py: Starter file to run howework 2"""

# Example Usage: ./cv_hw2 -i1 image1 -i2 image2 -t threshold -m GA
# Example Usage: python cv_hw2.py -i1 image1 -i2 image2 -t threshold -m LS

import cv2
import argparse
from gettrainimages import getTrain
from testscr import runFolder


def display_image(window_name, image):
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(0)


def main():

    parser = argparse.ArgumentParser()
    #Path to the folder which contains the images and xml base truth files
    parser.add_argument("-f", "--folder_path", dest="folder_path", help="Specify the path to the folder",
                        required=True)
    args = parser.parse_args()

    fpath = args.folder_path

    runf = runFolder()
    data = runf.runfolder(fpath)

    for i in range(0, len(data)):
        xmlfilepath = fpath + "/"+data[i][0]
        imagepath = fpath + "/"+data[i][1]
        image = cv2.imread(imagepath)
        xmltrain = getTrain()
        xmltrain.parseXML(image, xmlfilepath,imagepath)


if __name__ == "__main__":
    main()










