#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Walk - Make NAO waddle like a penguin"""

import qi
import argparse
import sys
import time
import almath


def main(session):
    """
    Walk: Small example to make Nao walk with gait customization.
    NAO will waddle.
    This example is only compatible with NAO.
    """
    # Get the services ALMotion & ALRobotPosture.

    motion_service = session.service("ALMotion")
    posture_service = session.service("ALRobotPosture")

    # Wake up robot
    motion_service.wakeUp()

    # Send robot to Stand Init
    posture_service.goToPosture("StandInit", 0.5)

    # TARGET VELOCITY
    X         = 1.0
    Y         = 0.0
    Theta     = 0.0
    Frequency = 1.0
    

    # Defined a waddle walk
    try:
        motion_service.moveToward(X, Y, Theta,[["Frequency", Frequency],
                                                # LEFT FOOT
                                                ["LeftStepHeight", 0.005],
                                                ["LeftTorsoWx", -5.5*almath.TO_RAD],
                                                ["LeftTorsoWy", 5.0*almath.TO_RAD],
                                                ["LeftMaxStepX", 0.02], 
                                                ["LeftMaxStepY", 0.14],
                                                ["LeftMaxStepFrequency", 0.5],
                                                # RIGHT FOOT
                                                ["RightStepHeight", 0.005],
                                                ["RightMaxStepX", 0.02],
                                                ["RightMaxStepY", 0.14],
                                                ["RightMaxStepFrequency", 0.5],
                                                ["RightTorsoWx", 5.5*almath.TO_RAD],
                                                ["RightTorsoWy", 5.0*almath.TO_RAD]
                                               ])
        time.sleep(10.0)
    
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()

    time.sleep(4.0)

    # stop walk in the next double support
    motion_service.stopMove()

    # Go to rest position
    motion_service.rest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
