
#Se eu entendi bem só preciso rodar isso aqui e eu conecto o Mission Planner COM essa conexão SITL e não o contrário (correto)
#MANDAR O MISSION PLANNER SE CONECTAR COM A PORTA 5602 (acredito que ele cria uma porta de saida na 5600 e uma de entrada na 5600)


#FUNCIONAAAA!!!!
#FUNCIONAAAA PORRAAA!!!
from dronekit import connect, VehicleMode
import dronekit_sitl
import time
import tkinter as tk
import pymavlink
import lib_controle_drone as control


###### CÓDIGO MAIN #####
sitl = dronekit_sitl.start_default(-27.593764, -48.541548) #coordenadas da quadra do IFSC
connection_string = sitl.connection_string()


print ("Start simulator (SITL)")
#comando pra conectar com o drone por porta serial
#connect('COM3', wait_ready=True, baud=57600))

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
#vehicle = connect(connection_string, baud=11520, wait_ready=True)
vehicle = connect("com3", baud=11520, wait_ready=True)
gnd_speed = 1

time.sleep(10)

def key(evento):
    global gnd_speed
    print(evento.keysym)
    if evento.keysym == "Up":
        control.set_velocity_body(vehicle, gnd_speed, 0, 0)
        time.sleep(0.5)
    elif evento.keysym == "Down":
        control.set_velocity_body(vehicle, -gnd_speed, 0, 0)
        time.sleep(0.5)
    elif evento.keysym == "Right":
        control.set_velocity_body(vehicle, 0, gnd_speed, 0)
        time.sleep(0.5)
    elif evento.keysym == "Left":
        control.set_velocity_body(vehicle, 0, -gnd_speed, 0)
        time.sleep(0.5)
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
    else:
        pass


root = tk.Tk()


control.arm_and_takeoff(vehicle, 10)
while vehicle.location.global_relative_frame.alt < 5:
    pass
root.bind_all("<Key>", key)
root.mainloop()



# Get some vehicle attributes (state)





# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
sitl.stop()
print("Completed")

