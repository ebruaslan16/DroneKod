import cv2
import numpy as np
from matplotlib import pyplot as plt
import math


lower_red=np.array([0,140,50])
upper_red=np.array([6,255,255])
lower_red1=np.array([35,170,50])
upper_red1=np.array([185,255,255])

lower_blue=np.array([90,50,50])
upper_blue=np.array([130,255,255])

kernel = np.ones((9,9), dtype=np.uint8)


def kirmiziAlan(hsv):
    global red_mask

    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    red = cv2.bitwise_and(copy, copy, mask=red_mask)
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red1 = cv2.bitwise_and(copy, copy, mask=red_mask1)
    sayac = red + red1
    return sayac


def maviAlan(hsv):
    global blue_mask

    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue = cv2.bitwise_and(copy, copy, mask=blue_mask)
    return blue




goruntu=cv2.VideoCapture(0)


while True:
    ret,kare=goruntu.read()
    copy=kare.copy()
    
    gri = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    gaussionBlur = cv2.GaussianBlur(copy, (9, 9), cv2.BORDER_DEFAULT)
    canny = cv2.Canny(gaussionBlur, 100, 100)
    dilation = cv2.dilate(canny, kernel, iterations=1)
    hsv = cv2.cvtColor(kare, cv2.COLOR_BGR2HSV)
    blue_p = maviAlan(hsv)
    red_p = kirmiziAlan(hsv)

    def kameraMerkezi(merkez1, merkez2, cap):
        cv2.circle(copy, (merkez1, merkez2), cap, (0, 255, 165), 4)
        cv2.circle(red_p, (merkez1, merkez2), cap, (0, 255, 165), 4)
        cv2.circle(blue_p, (merkez1, merkez2), cap, (0, 255, 165), 4)


    kameraMerkezi(320, 240, 120)





    cv2.circle(copy, (320, 240), 3, (0, 255, 255), cv2.FILLED, 1)

    cv2.circle(blue_p, (320, 240), 3, (0, 255, 255), cv2.FILLED, 1)
    cv2.circle(red_p, (320, 240), 3, (0, 255, 255), cv2.FILLED, 1)



    cv2.putText(copy, "Merkez", (320, 240), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
    cv2.putText(blue_p, "Merkez", (320, 240), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
    cv2.putText(red_p, "Merkez", (320, 240), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)




    circles = cv2.HoughCircles(dilation, cv2.HOUGH_GRADIENT, 1, copy.shape[0] / 10, param1=350, param2=28,
                              minRadius=60,
                              maxRadius=88)

    mavi_circles = cv2.HoughCircles(dilation, cv2.HOUGH_GRADIENT, 1, blue_p.shape[0] / 24, param1=350, param2=28,
                               minRadius=7,
                               maxRadius=45)

    kirmizi_circles = cv2.HoughCircles(dilation, cv2.HOUGH_GRADIENT, 1, red_p.shape[0] / 10, param1=250, param2=16,
                               minRadius=60,
                               maxRadius=88)

    if circles is not None:
        kose = np.uint16(np.around(circles[0,:]))

        for x,y,r in kose:

            cv2.putText(copy, "Algilandi", (15,15), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0),2)
            cv2.circle(copy, (x, y), r, (0, 255, 0), 2)
            cv2.circle(copy, (x, y), 2, (255, 255, 255), 3)
            
            cv2.line(copy, (320, 240), (x, y), (255, 255, 0), 4)


    if mavi_circles is not None:
        mavi = np.uint16(np.around(mavi_circles[0, :]))

        for a, b, c in mavi:

            cv2.putText(blue_p, "Algilandi", (15, 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            cv2.circle(blue_p, (a, b), c, (0, 255, 0), 2)
            cv2.circle(blue_p, (a, b), 2, (255, 255, 255), 3)
            cv2.line(blue_p,(320,240), (a,b), (255,255,0), 4)
            hesap=cv2.putText(blue_p, "{}".format(int(np.sqrt((a - 20) ** 2 + (b - 200) ** 2))), (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            if 418<a<184 and 340<b<311:
                kameraMerkezi(320,240,120)
                cv2.putText(blue_p, "Hedef Tespit Edildi", (15,15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                break






    if kirmizi_circles is not None:
        kirmizi = np.uint16(np.around(kirmizi_circles[0, :]))

        for o, k, u in kirmizi:
            cv2.putText(red_p, "Algilandi", (15, 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            cv2.circle(red_p, (o, k), u, (0, 255, 0), 2)
            cv2.circle(red_p, (o, k), 2, (255, 255, 255), 3)
            cv2.line(red_p, (320, 240), (o, k), (255, 255, 0), 4)
            #hesap=cv2.putText(blue_p, "{}".format(int(np.sqrt((o - 20) ** 2 + (k - 200) ** 2))), (100, 100),
                        #cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    

    #cv2.imshow("MAVI",blue_p)
    cv2.imshow("KIRMIZI",red_p)
    cv2.imshow("Daire",copy)
    print(mavi_circles)


    if cv2.waitKey(25) & 0xFF == ord("q"):
        break


goruntu.release()
cv2.destroyAllWindows()