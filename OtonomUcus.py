import cv2
import dronekit
from dronekit import VehicleMode, connect, LocationGlobalRelative, LocationGlobal
import dronekit_sitl
import time
import numpy as np
import math



global konum1, konum2
bayrak1=True
kontrol1=True
kontrol2=False
kontrol3=False
kontrol4=False
kontrol5=False
kontrol6=False
sitl=dronekit_sitl.start_default()
baglanti=sitl.connection_string()
vehicle=connect(baglanti, wait_ready=True)
vehicle.mode=VehicleMode('GUIDED')
vehicle.simple_takeoff(10)
vehicle.mode=VehicleMode('AUTO')

def otonomUcuske(konum1,konum2):
    global kontrol1
    vehicle.simple_goto(konum1)
    print("konum1'e yöneliyor")

    while kontrol1:
        en=konum1.lat-vehicle.location.global_relative_frame.lat
        boy=konum1.lon-vehicle.location.global_relative_frame.lon
        fark=math.sqrt(en*en)+(boy*boy)
        print(fark)
        if (fark<=0.5): #alana olan mesafesi minimumsa;
            enlem=vehicle.location.global_frame.lat #anlık enlem alınır
            boylam=vehicle.location.global_frame.lon #anlık boylam alınır
            nokta1=vehicle.location.global_relative_frame(enlem,boylam,1) #irtifa 5'e indi, alanın enlem boylamı koordinat olarak alındı
            vehicle.simple_goto(nokta1) #nokta1'e gönderildi
            print("Hedefe doğru gidiliyor ")
            kontrol1=False #döngüden çıkarıldı
            kontrol2=True #başka bir döngü şartı

    while kontrol2:
        print("Hedeflenen irtifaya inildi") #su alma-bırakma mesafesi
        if vehicle.location.global_relative_frame<=1: #irtifa şartı
            time.sleep(7) #su alma-bırakma bekleme süresi
            enlem = vehicle.location.global_frame.lat  #anlık enlem
            boylam = vehicle.location.global_frame.lon  #anlık boylam
            nokta2 = vehicle.location.global_relative_frame(enlem, boylam, 10) #irtifa tekrar yükseldi
            vehicle.simple_goto(nokta2)
            print("nokta2'ye yönleniyor..")
            kontrol2=False
            kontrol3=True

    while kontrol3:
        print("Hedeflenen irtifaya çıkarıldı")
        if (vehicle.location.global_relative_frame.alt>=9): #irtifa şartı
            vehicle.simple_goto(konum2)
            kontrol3=False
            kontrol4=True

    while kontrol4:
        enlem2=konum2.lat-vehicle.location.global_relative_frame.lat
        boylam2=konum2.lon-vehicle.location.global_relative_frame.lon
        fark=math.sqrt((enlem2*enlem2)+(boylam2*boylam2))*1.113195e5
        print(fark)
        if(fark<=0.5):
            enlem=vehicle.location.global_frame.lat
            boylam=vehicle.location.global_frame.lon
            nokta3=LocationGlobalRelative(enlem,boylam,2)
            vehicle.simple_goto(nokta3)
            print("nokta3'e yönleniyor..")
            kontrol4=False
            kontrol5=True

    while kontrol5:
        print("hedeflenen irtifaya inildi")
        if vehicle.location.global_relative_frame.alt<=2:
            time.sleep(5)
            enlem=vehicle.location.global_frame.lat
            boylam=vehicle.location.global_frame.lon
            nokta4=LocationGlobalRelative(enlem,boylam,10)
            vehicle.simple_goto(nokta4)
            print("nokta4'e yönleniyor..")
            kontrol5=False
            kontrol6=True

    while kontrol6:
        print("hedeflenen irtifaya çıkıldı")
        if(vehicle.location.global_relative_frame.alt>=10):
            vehicle.mode=VehicleMode("AUTO")
            print("İşlem tamamlandı!")
            time.sleep(2)
            kontrol6=False
while True:
    mod=vehicle.mode
    nextwp=vehicle.commands.next #nextWayPoint
    print("WayPoint bekleniyor... ")
    if nextwp==1:
        vehicle.mode=VehicleMode('GUIDED')
        print("GUIDED moda alındı.")
        break

while True:
    konum1=dronekit.LocationGlobalRelative(39.233,30.232) #su alma alanı koordinatları girilecek
    konum2=LocationGlobalRelative(39.233,30.232) #su bırakma alanı, sonradan görüntü işleme dahil olacak
    if bayrak1==True:
        otonomUcuske(konum1,konum2)
        bayrak1=False

