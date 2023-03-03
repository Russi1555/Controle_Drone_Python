
#Se eu entendi bem só preciso rodar isso aqui e eu conecto o Mission Planner COM essa conexão SITL e não o contrário (correto)
#MANDAR O MISSION PLANNER SE CONECTAR COM A PORTA 5602 (acredito que ele cria uma porta de saida na 5600 e uma de entrada na 5601)




#***Necessário pra evitar dor de cabeça relacionada a versão de python***
import sys
if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections
    setattr(collections, "MutableMapping", collections.abc.MutableMapping)

from dronekit import connect, VehicleMode
import dronekit_sitl
import time
import tkinter as tk
import pymavlink
import lib_controle_drone as control
import queue
from multiprocessing import Process
import subprocess


QGC_stdout = ""

def processo_QGC():
    global QGC_stdout 
    QGC_stdout = subprocess.Popen(r"C:\Users\PECCE\Desktop\qgroundcustom\build-qgroundcontrol-Desktop_Qt_5_15_2_MSVC2019_64bit-Debug\staging\QGroundControl.exe",shell = True, stdout=subprocess.PIPE, stderr = subprocess.STDOUT )
    while True:
       line = str(QGC_stdout.stdout.readline()).replace("b","").replace("'","")
       print(line)
       #OK. Isso aqui funciona. Da pra fazer um botão no QGroundControl que console.log("ABRA CONTROLE MANUAL") e liga o modo guiado do python
       if "TESTE" in line:
           print("AAAAAAAAAAAAAAAAAAAA\n\n\n\n\n")
           quit

###### CÓDIGO MAIN #####
if __name__ == '__main__': 
    sitl = dronekit_sitl.start_default(-27.593764, -48.541548) #coordenadas da quadra do IFSC
    connection_string = sitl.connection_string()


    print ("Start simulator (SITL)")
    #comando pra conectar com o drone por porta serial
    #connect('COM3', wait_ready=True, baud=57600))
    QGC = Process(target=processo_QGC)
    QGC.start()

    # Connect to the Vehicle.
    print("Connecting to vehicle on: %s" % (connection_string,))
    vehicle = connect(connection_string, baud=11520, wait_ready=True)
    #vehicle = connect("com3", baud=11520, wait_ready=True)
    gnd_speed = 1
    fila_comandos = queue.Queue(maxsize=10) #estrutura de fila garante que o drone não vai seguir uma quantidade de comandos imensa que pode leva-lo a uma situação perigosa
    vehicle.initialize

    time.sleep(10)

    def key(evento):
        global gnd_speed
        global fila_comandos
    
        print(evento.keysym)
        if evento.keysym == "Up":
            if  fila_comandos.full():
                pass
            else:
                print("ENQUEUE UP")
                fila_comandos.put("up")

        elif evento.keysym == "Down":
            if fila_comandos.full():
                pass
            else:
                fila_comandos.put("down")

        elif evento.keysym == "Right":
            if fila_comandos.full():
                pass
            else:
                fila_comandos.put("right")
        elif evento.keysym == "Left":
            if fila_comandos.full():
                pass
            else:
                fila_comandos.put("left")

        elif evento.keysym == "plus": #Controle de velocidade no + do keypad
            if gnd_speed >= 1 and gnd_speed < 12:
                gnd_speed +=1
            elif gnd_speed > 0 and gnd_speed < 1: #movimentos precisos
                gnd_speed += 0.1
            print(str(gnd_speed))
            time.sleep(1)

        elif evento.keysym == "minus": #Controle de velocidade no - do keypad
            if gnd_speed > 1 :
                gnd_speed -=1
            elif gnd_speed > 0.2 and gnd_speed <= 1: #movimentos precisos
                gnd_speed -= 0.1
            print(str(gnd_speed))
            time.sleep(1)

        elif evento.keysym == "e" or evento.keysym == "E":
            print("TESTE e")
            if fila_comandos.full():
                pass
            else:
                fila_comandos.put("e")
            time.sleep(1)

        elif evento.keysym == "q" or evento.keysym == "Q":
            print("TESTE q")
            if fila_comandos.full():
                pass
            else:
                fila_comandos.put("q")
            time.sleep(1)

        elif evento.keysym == 'bracketleft':
            if fila_comandos.full():
                pass
            else:
                fila_comandos.put("[")
            time.sleep(1)
    
        elif evento.keysym == 'bracketright':
            if fila_comandos.full():
                pass
            else:
                fila_comandos.put("]")
            time.sleep(1)

        else:
            pass


    root = tk.Tk()


    #this creates a new label to the GUI

    control.arm_and_takeoff(vehicle, 3)
    while True:
        root.bind_all("<Key>", key)
        if not(fila_comandos.empty()):
            print("TESTE2")
            command = fila_comandos.get()
            if command == "up":
                control.set_velocity_body(vehicle, gnd_speed, 0, 0)
                time.sleep(0.5)
            elif command == "down":
                control.set_velocity_body(vehicle, -gnd_speed, 0, 0)
                time.sleep(0.5)
            elif command == "right":
                control.set_velocity_body(vehicle, 0, gnd_speed, 0)
                time.sleep(0.5)
            elif command == "left":
                control.set_velocity_body(vehicle, 0, -gnd_speed, 0)
                time.sleep(0.5)
            elif command == 'e':
                control.rotate(vehicle,0,0,10) #(pitch, roll, yaw)
                time.sleep(0.5)
            elif command == 'q':
                control.rotate(vehicle,0,0,-10) #(pitch, roll, yaw)
                time.sleep(0.5)
            elif command == '[':
                control.set_velocity_body(vehicle, 0, 0, -0.5)
            elif command == ']':
                control.set_velocity_body(vehicle, 0, 0, 0.5)

        print("MUITO FODA O : ", str(QGC_stdout.communicate()[0]))
        root.update_idletasks()
        root.update()


    # Get some vehicle attributes (state)

    # Close vehicle object before exiting script
    vehicle.close()

    # Shut down simulator
    sitl.stop()
    print("Completed")
    QGC.join()

