from hub import light_matrix
from hub import port
import runloop
import motor
import force_sensor
import motor_pair
from hub import motion_sensor


async def main():
    #Conversion
    DECIDEGREES_TO_DEGREES = 1/10
  
    #Reset the yaw (turn angle) of the robot to zero
    motion_sensor.reset_yaw(0)

    '''
    Motor Assignments (Assuming color sensors are at the front of robot):

    A - Left Drive
    E - Right Drive
    D - Front Gear
    C - Front Force Sensor
    B - Back Force Sensor 
    F - Right Color Sensor
    '''

    #Drive motor pair
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)

    #Default drive speed (top motor speed is 10,000)
    speed = 500;

    while (True):
        #Get the angles and yaw of the robot, then convert to degrees
        angles = motion_sensor.tilt_angles()
        yaw = angles[0] * DECIDEGREES_TO_DEGREES

        #If the force sensor is pressed, back up, turn 180*, then use a P controller to turn back to 0*
        if force_sensor.pressed(port.B):
            await motor_pair.move_tank_for_time(motor_pair.PAIR_1, speed, speed, 1000)
            while (abs(abs(yaw) - 180) > 5.0):
                angles = motion_sensor.tilt_angles()
                yaw = angles[0] * DECIDEGREES_TO_DEGREES
                motor_pair.move_tank(motor_pair.PAIR_1, 200, -200)
                print(yaw)
            pController = round(yaw * 100)
            while (abs(pidController) > 1.0):
                angles = motion_sensor.tilt_angles()
                yaw = angles[0] * DECIDEGREES_TO_DEGREES

                #List of potential P values for people to try out if they want
                #5.0, 7.5, 10.0, 15.0, 20.0
                kP = 7.5 
                pidController = round(yaw * kP)
                motor_pair.move_tank(motor_pair.PAIR_1, min(1000, max(pidController, -1000)), -min(1000, max(pidController, -1000)))
                print(yaw)
        else:
            motor_pair.move_tank(motor_pair.PAIR_1, -speed, -speed)

runloop.run(main())
