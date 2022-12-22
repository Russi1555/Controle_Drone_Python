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
            0b0000111111000111, #-- BITMASK -> Consider only the velocities #atualmente não tem suporte pra controlar o drone através de aceleração.
            0, 0, 0,        #-- POSITION
            vx, vy, vz,     #-- VELOCITY
            0, 0, 0,        #-- ACCELERATIONS
            0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()


    