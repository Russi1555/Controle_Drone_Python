
#Se eu entendi bem só preciso rodar isso aqui e eu conecto o Mission Planner COM essa conexão SITL e não o contrário (correto)
#MANDAR O MISSION PLANNER SE CONECTAR COM A PORTA 5602 (acredito que ele cria uma porta de saida na 5600 e uma de entrada na 5600)


#FUNCIONAAAA!!!!
#FUNCIONAAAA PORRAAA!!!
from dronekit import connect, VehicleMode
import dronekit_sitl
import time
import tkinter as tk
import pymavlink


def arm_and_takeoff(vehicle, altitude):
    while not vehicle.is_armable:
        print("Aguardando poder armar o veiculo")
        time.sleep(1)
    
    time.sleep(5)
    print("armando motores")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed: time.sleep(1)

    print("levantando voo")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    vehicle.simple_takeoff(altitude)

    while True:
        v_alt = vehicle.location.global_relative_frame.alt
        print(">>> Altitude atual :  " + str(v_alt))
        if v_alt >= altitude - 1:
            print("Altitude desejada atingida")
            break
        time.sleep(1)

def set_velocity_body(vehicle, vx , vy , vz):
    #vz é positivo quando esta indo em direção ao chão

    msg = vehicle.message_factory.set_position_target_local_ned_encode(
            0,
            0, 0,
            pymavlink.mavutil.mavlink.MAV_FRAME_BODY_NED,
            0b0000111111000111, #-- BITMASK -> Consider only the velocities
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()


###### CÓDIGO MAIN #####
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()







print ("Start simulator (SITL)")
#comando pra conectar com o drone por porta serial
#connect('COM3', wait_ready=True, baud=57600))

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, baud=11520, wait_ready=True)
gnd_speed = 1

time.sleep(10)

def key(evento):
    global gnd_speed
    print(evento.keysym)
    if evento.keysym == "Up":
        set_velocity_body(vehicle, gnd_speed, 0, 0)
        time.sleep(0.5)
    elif evento.keysym == "Down":
        set_velocity_body(vehicle, -gnd_speed, 0, 0)
        time.sleep(0.5)
    elif evento.keysym == "Right":
        set_velocity_body(vehicle, 0, gnd_speed, 0)
        time.sleep(0.5)
    elif evento.keysym == "Left":
        set_velocity_body(vehicle, 0, -gnd_speed, 0)
        time.sleep(0.5)
    elif evento.keysym == "plus": #Controle de velocidade no + do keypad
        if gnd_speed < 12:
            gnd_speed +=1
        print(str(gnd_speed))
        time.sleep(1)
    elif evento.keysym == "minus": #Controle de velocidade no - do keypad
        if gnd_speed > 1 :
            gnd_speed -=1
        print(str(gnd_speed))
        time.sleep(1)
    else:
        pass


root = tk.Tk()


arm_and_takeoff(vehicle, 10)
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

