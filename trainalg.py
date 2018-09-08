import cv2
from datetime import datetime

class startTest:
    def ThreeD(self, a, b, c):
        lst = [[['#' for col in range(a)] for col in range(b)] for row in range(c)]
        return lst

    def doVidTest(self, imagepath):
        #imagepath = '/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/output/data/classifierHAAR/cascade.xml'
        car_cascade = cv2.CascadeClassifier(imagepath)
        cap = cv2.VideoCapture(0)

        while 1:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, 50, 50)
            #Drawing the bounding box for every detection
            for (x, y, w, h) in cars:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.imshow('img', img)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def doImgTest(self, clfpath,imgpath):

        #Path to the classifier
        #clfpath = '/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/smalloutput/data/HAAR3/cascade.xml'
        car_cascade = cv2.CascadeClassifier(clfpath)
        #Path to the image
        #imgpath = '/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/PKLot/parking2/cloudy/2012-10-31/2012-10-31_08_08_03.jpg'
        img = cv2.imread(imgpath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        i = 0
        #Does not detect if no image is given
        if gray is not None:
            cars = car_cascade.detectMultiScale(gray, 7, 15)
        # Draw border
            points_list = [[ -1 for x in range(4)] for y in range(len(cars))]
            for (x, y, w, h) in cars:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                points_list[i] = [int(x), int(y) , int(w), int(h)]
                i = i + 1

        #Saving the image for verification
        output_path =  "/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/Test_Images/Detected_clf" + datetime.now().strftime(
            "%m%d-%H%M%S") + ".jpg"
        cv2.imwrite(output_path, img)
        #Return list of detection from the classifier
        return(points_list)