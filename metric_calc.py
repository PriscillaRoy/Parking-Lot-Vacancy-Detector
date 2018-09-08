from xml.dom import minidom
from trainalg import startTest
import numpy as np
import cv2
from datetime import datetime

class startMetrics:
    def bb_intersection_over_union(self,boxA, boxB):
        #The following code is taken from https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/
        # determine the (x, y)-coordinates of the intersection rectangle
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        # compute the area of intersection rectangle
        interArea = (xB - xA + 1) * (yB - yA + 1)

        # compute the area of both the prediction and ground-truth
        # rectangles
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = interArea / float(boxAArea + boxBArea - interArea)
        return(iou)

    def ThreeD(self, a, b, c):
        lst = [[['#' for col in range(a)] for col in range(b)] for row in range(c)]
        return lst

    def calc(self, xml_path,img_path,clf_path):
        #xml_path = "/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/PKLot/parking2/cloudy/2012-10-31/2012-10-31_08_08_03.xml"
        #img_path = "/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/PKLot/parking2/cloudy/2012-10-31/2012-10-31_08_08_03.jpg"
        doc = minidom.parse(xml_path)

        # Getting points list from xml file
        contours = doc.getElementsByTagName("contour")
        occupied_data = doc.getElementsByTagName("space")
        poslen = 0
        occupancy = list()
        for occ in occupied_data:
            occupancy.append(occ.getAttribute("occupied"))
            ocp = occ.getAttribute("occupied")

            if (ocp == '1'):
                poslen = poslen + 1
        #print(poslen)

        i = 0
        j = 0
        points_list = [['#' for x in range(4)] for y in range(poslen)]

        #Considering points only that are occupied
        for contour in contours:
            if(occupancy[i] == '1'):
                point1 = contour.getElementsByTagName("point")[0]
                p1x = point1.getAttribute("x")
                p1y = point1.getAttribute("y")
                temp_p1 = (p1x, p1y)
                point2 = contour.getElementsByTagName("point")[1]
                p2x = point2.getAttribute("x")
                p2y = point2.getAttribute("y")
                temp_p2 = (p2x, p2y)
                point3 = contour.getElementsByTagName("point")[2]
                p3x = point3.getAttribute("x")
                p3y = point3.getAttribute("y")
                temp_p3 = (p3x, p3y)
                point4 = contour.getElementsByTagName("point")[3]
                p4x = point4.getAttribute("x")
                p4y = point4.getAttribute("y")
                temp_p4 = (p4x, p4y)
                pts = [['#' for x in range(2)] for y in range(4)]
                pts[0] = temp_p1
                pts[1] = temp_p2
                pts[2] = temp_p3
                pts[3] = temp_p4
                #Converting them to the format needed for minAreaRect
                point = np.array([(int(pts[0][0]), int(pts[0][1])), (int(pts[1][0]), int(pts[1][1])),(int(pts[2][0]), int(pts[2][1])), (int(pts[3][0]), int(pts[3][1]))])
                rectangle = cv2.minAreaRect(point)
                points_new = cv2.boxPoints(rectangle)  # Find four vertices of rectangle from above rect
                points_new = np.int0(np.around(points_new))
                xvalues = np.array([points_new[0][0], points_new[1][0], points_new[2][0], points_new[3][0]])
                yvalues = np.array([points_new[0][1], points_new[1][1], points_new[2][1], points_new[3][1]])
                newxmin = np.amin(xvalues)
                newymin = np.amin(yvalues)
                newxmax = np.amax(xvalues)
                newymax = np.amax(yvalues)
                #Finding x,y,w,h
                points_list[j] = [newxmin, newymin, newxmax - newxmin,newymax - newymin]
                j = j + 1
            i = i + 1


        imag = cv2.imread(img_path)
        count = 0
        #Drawing the bounding boxes from the base truth file
        for (x, y, w, h) in points_list:
            cv2.rectangle(imag, (x, y), (x + w, y + h), (255, 0, 255), 3)
            count = count + 1
        #Finding the bounding boxes from the classifier
        test1 = startTest()
        clf_points = test1.doImgTest(clf_path,img_path)
        count_clf = 0
        for (x, y, w, h) in clf_points:
            cv2.rectangle(imag, (x, y), (x+ w, y + h), (0, 255, 0), 2)
            count_clf = count_clf + 1

        #Verifying visually how the boxes are drawn
        output_path =  "/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/Test_Images/Compare_" + datetime.now().strftime(
            "%m%d-%H%M%S") + ".jpg"
        cv2.imwrite(output_path, imag)
        i = 0
        tp = 0 # True Positives Count
        fp = 0 # False Positive Count
        for (x, y, w, h) in clf_points:
            #print("Iteration no >>", i)
            boxA = np.array([x,y,x+w,y+h]) # box from classifier

            #Comparing it with every box from the base truth file
            for box in points_list:

                boxB = np.array([box[0], box[1], box[2],box[3]])
                iou = self.bb_intersection_over_union(boxB,boxA)

                if(iou > 20):
                    print("IOU", iou)
                    tp = tp + 1
                    break
            i = i + 1

        metric_file = open('/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/output_metrics.txt', 'a')
        metric_file.write(datetime.now().strftime("%m%d-%H%M%S"))
        metric_file.write('\n')
        metric_file.write("True Positives : %i , False Positives :  %i , Accuracy : %f " % (tp, count_clf - tp, ((tp*100)/count)))
        metric_file.write('\n')
        print("True Positives >>", tp)
        print("False Positives >>", count_clf - tp)
        print("Accuracy >>", ((tp*100)/count))
        metric_file.close()

