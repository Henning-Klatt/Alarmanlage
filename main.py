#!/usr/bin/python

import os
import pifacedigitalio as p
import time
import os.path
p.init()
print("programm läuft!")
os.system("sudo rm /var/www/camera.info")
os.system("vcgencmd measure_temp")
x=0
a=0

while(True):
    button_1 = p.digital_read(7)
    button_2 = p.digital_read(1)

    def getCpuTemperature():
        tempFile= open( "/sys/class/thermal/thermal_zone0/temp" )
        cpu_temp = tempFile.read()
        tempFile.close()
        return float(cpu_temp)/1000

    Camerada = os.path.exists("/var/www/camera.info")
    if Camerada == True:
        os.system("sudo fswebcam -c /etc/webcam1.cfg")
        print("Foto wurde von Website aus gemacht!")
        os.system("mpack -s 'Pi hat ein Foto gemacht!' /home/pi/Fotos/Bild.jpg henning.klatt@web.de")
        print("Foto wurde gesendet!")
        time.sleep(0.5)
        os.system("sudo mv /home/pi/Fotos/Bild.jpg /var/www/Bild.png")
        print("Foto wurde in den Webserver verschoben")
        os.system("sudo rm /var/www/camera.info")

    Powerda = os.path.exists("/var/www/power.info")
    if Powerda == True:
        os.system("sudo rm /var/www/power.info")
        time.sleep(0.3)
        os.system("sudo shutdown -h now")

    if getCpuTemperature() > 70.000:
        print("CPU liegt über 70°C !")
        os.system("echo 'Die CPU Temperatur liegt über 70° Der Pi schaltet sich nun aus!' | mail -s '[CPU BEI 65°C!]' henning.klatt@web.de")
        os.system("sudo shutdown -h now")

    if x==0:
        if getCpuTemperature() > 55.000:
            print("CPU liegt über 55°C !")
            os.system("echo 'Die CPU Temperatur liegt über 55°C! Der Pi kann unter: http://212.86.176.50  heruntergefahren werden!' | mail -s '[CPU über 55°C!' henning.klatt@web.de")
            x=1

    Dateida = os.path.exists("/var/www/go.info")
    if Dateida == True:
        a=1
        if button_1 == 1:
            print("Tür wurde geöffnet!")
            time.sleep(0.5)
            os.system("sudo fswebcam -c /etc/webcam1.cfg")
            print("Foto wurde gemacht!")
            os.system("mpack -s 'Pi hat ein Foto gemacht!' /home/pi/Fotos/Bild.jpg henning.klatt@web.de")
            print("Foto wurde gesendet!")
            time.sleep(0.5)
            os.system("sudo mv /home/pi/Fotos/Bild.jpg /var/www/Bild.png")
            print("Foto wurde vom Pi gelöscht und in den Webserver verschoben!")
            p.digital_write(0,1)
            time.sleep(0.4)
            p.digital_write(0,0)
            time.sleep(0.4)
            p.digital_write(0,1)
            time.sleep(0.4)
            p.digital_write(0,0)
        
            if getCpuTemperature() > 55.000:
                print("CPU Temperatur liegt über 55°!")
                os.system("echo 'Die CPU Temperatur liegt ueber 55°C ! Pi herunterfahren unter: http://212.86.176.50' | mail -s '[CPU WARNUNG]' henning.klatt@web.de")
                print(getCpuTemperature())
                time.sleep(5)
