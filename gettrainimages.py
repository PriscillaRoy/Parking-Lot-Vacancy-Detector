from xml.dom import minidom
import cv2
import numpy as np
from datetime import datetime

#opencv_createsamples -bg output//Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/output/pos/posdat1.txt.txt -info output/info.lst
#opencv_createsamples -num 28 -w 20 -h 20 -info posdat.txt -vec output/info/positive.vec
#opencv_traincascade -data output/data -vec output/info/positive.vec -bg output/neg/negdat.txt -numPos 2000 -numNeg -2000 -numStages 10 -minHitRate 0.995 -w 20 -h 20 -mode ALL -featureType LBP
#Ref : https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
class getTrain:


    def ThreeD(self, a, b, c):
        lst = [[['#' for col in range(a)] for col in range(b)] for row in range(c)]
        return lst

    def parseXML(self, image, xmlfile,imgpath ):
        # Folder paths for storing example images
        #Positive path not needed as slicing images is not done - just to check if the examples are good enough
        posf = open("smalloutput/pos/posdat.txt", "a")
        negf = open("smalloutput/neg/negdat.txt", "a")
        #Parsing the xml file
        doc = minidom.parse(xmlfile)
        #Getting all the contour points
        contours = doc.getElementsByTagName("contour")
        px = list()
        py = list()
        poslen = 0
        neglen = 0
        poswrite = 0

        #Finding if a spot is occupied or not
        occupied_data = doc.getElementsByTagName("space")
        occupancy = list()
        for occ in occupied_data:
            occupancy.append(occ.getAttribute("occupied"))
            ocp = occ.getAttribute("occupied")

            if(ocp == '1'):
                poslen = poslen+1
            elif(ocp == '0'):
                neglen = neglen + 1

        if(poslen > 0):
            posf.write("%s %i " % (imgpath, poslen))

        points_list = self.ThreeD(2,4,len(contours))
        i = 0
        #Finding all the contours
        for contour in contours:
            point1 = contour.getElementsByTagName("point")[0]
            p1x = point1.getAttribute("x")
            p1y = point1.getAttribute("y")
            px.append(p1x)
            py.append(p1y)
            temp_p1 = (p1x, p1y)
            point2 = contour.getElementsByTagName("point")[1]
            p2x = point2.getAttribute("x")
            p2y = point2.getAttribute("y")
            px.append(p2x)
            py.append(p2y)
            temp_p2 = (p2x, p2y)
            point3 = contour.getElementsByTagName("point")[2]
            p3x = point3.getAttribute("x")
            p3y = point3.getAttribute("y")
            px.append(p3x)
            py.append(p3y)
            temp_p3 = (p3x, p3y)
            point4 = contour.getElementsByTagName("point")[3]
            p4x = point4.getAttribute("x")
            p4y = point4.getAttribute("y")
            px.append(p4x)
            py.append(p4y)
            temp_p4 = (p4x, p4y)
            points_list[i][0]= temp_p1
            points_list[i][1] = temp_p2
            points_list[i][2] = temp_p3
            points_list[i][3] = temp_p4
            i = i+1

        i = 0
        pos_dir = '/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/smalloutput/pos/images/' + imgpath[-14: -4]
        neg_dir = '/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/smalloutput/neg/images/' + imgpath[ -14: -4]
        #Getting the x,y,w,h and storing them
        for points in points_list:
            point = np.array([(int(points[0][0]),int(points[0][1])),(int(points[1][0]),int(points[1][1])),(int(points[2][0]),int(points[2][1])),(int(points[3][0]),int(points[3][1]))])

            rectangle = cv2.minAreaRect(point)
            points_new = cv2.boxPoints(rectangle)  # Find four vertices of rectangle from above rect
            points_new = np.int0(np.around(points_new))
            if(occupancy[i] == '1'):

                t = datetime.now()
                s = t.strftime('%H_%M_%S')
                output_path = pos_dir + s +str(i)+ ".jpg"

                xvalues = np.array([points_new[0][0], points_new[1][0], points_new[2][0], points_new[3][0]])
                yvalues = np.array([points_new[0][1], points_new[1][1], points_new[2][1], points_new[3][1]])
                newxmin = np.amin(xvalues)
                newymin = np.amin(yvalues)
                newxmax = np.amax(xvalues)
                newymax = np.amax(yvalues)
                pic = image[newymin:newymax, newxmin:newxmax]

                posf.write("%i %i %i %i " % (newxmin, newymin, newxmax - newxmin,newymax - newymin ))
                poswrite = 1

                cv2.imwrite(output_path, pic)
            elif(occupancy[i] == '0'):
                t = datetime.now()
                s = t.strftime('%H_%M_%S')
                output_path = neg_dir + s +str(i)+ ".jpg"
                xvalues = np.array([points_new[0][0], points_new[1][0], points_new[2][0], points_new[3][0]])
                yvalues = np.array([points_new[0][1], points_new[1][1], points_new[2][1], points_new[3][1]])
                newxmin = np.amin(xvalues)
                newymin = np.amin(yvalues)
                newxmax = np.amax(xvalues)
                newymax = np.amax(yvalues)
                pic = image[newymin:newymax, newxmin:newxmax]
                negf.write("%i %i %i %i " % (newxmin, newymin, newxmax, newymax))
                negwrite = 1
                negf.write(output_path)
                negf.write("\n")
                cv2.imwrite(output_path, pic)
            i = i+1

        if(poswrite == 1):
            posf.write("\n")
        posf.close()



