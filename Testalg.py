#opencv_traincascade -data output/data/classifier -vec output/info/positive2.vec -bg output/neg/negdat.txt -numPos 5000 -numNeg 4000 -numStages 20 -minHitRate 0.995 -w 20 -h 20 -mode ALL
#opencv_createsamples -num 6000 -w 20 -h 20 -info posdat.txt -vec output/info/positive2.vec

from metric_calc import startMetrics

def main():
    test2 = startMetrics()
    img_ptr = open('/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/imagefile.txt', 'r')
    xml_ptr = open('/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/xmlfiles.txt','r')
    #clf = '/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/smalloutput/data/HAAR3/cascade.xml'
    clf = '/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/smalloutput/data/HAAR3/cascade.xml'

    image_path = '/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/PKLot/parking1b/rainy/2013-04-12/2013-04-12_17_50_13.jpg'
    xml_path = '/Users/priscilla/PycharmProjects/homework-3-PriscillaRoy/PKLot/parking1b/rainy/2013-04-12/2013-04-12_17_50_13.xml'
    test2.calc(xml_path,image_path,clf)




if __name__ == "__main__":
    main()