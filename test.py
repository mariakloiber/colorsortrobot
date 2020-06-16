import time
import ev3dev.ev3 as ev3
from SturdyRobot import SturdyRobot

class Test(object):
    """This behavior should move forward at a fixed, not-too-fast speed if no object
    is close enough in front of it. When an object is detected, it should stop moving."""
    def __init__(self, robot = None, bttn = None, leftM = 'outD', rightM = 'outA', armM = 'outC', medM = 'outB', cs = 'in3', us = 'in1', cs2 = 'in4'):
        self.bttn = ev3.Button()
        self.leftM = ev3.LargeMotor(leftM)
        self.rightM = ev3.LargeMotor(rightM)
        self.armM = ev3.LargeMotor(armM)
        self.medM = ev3.MediumMotor(medM)
        #self.leftT = ev3.TouchSensor('in4')
        #self.rightT = ev3.TouchSensor('in1')
        self.cs = ev3.ColorSensor('in3')
        self.us = ev3.UltrasonicSensor('in1')
        self.cs2 = ev3.ColorSensor('in4')
        self.lflag = 0
        self.rflag = 0

        if(self.leftM.is_running):
            lflag = 1
            print("Left booster is on")

        if(self.rightM.is_running):
            rflag = 1
            print("Right booster is on")
        pass

if __name__ == '__main__':
    # set up robot object here if using it
    # testBehav = Test(rob)  # pass robot object here if need be
    rob = SturdyRobot()
    testBehav = SturdyRobot(rob)

    # add code to stop robot motors
    rob.leftM.stop()
    rob.rightM.stop()
    buttons = ev3.Button()

    while(not buttons.any()):
        while True:
            if(rob.cs.color == 1):
                    rob.leftM.stop()
                    rob.rightM.stop()
                    print("turning")
                    rob.curve(-0.4, 0.4)
                    time.sleep(.5)
                    pass
            if ((rob.readDistance()) > 15):
                rob.wander()
                print(rob.cs.color)
                pass
            if rob.Wary() == 'found':
                time.sleep(.5)
                if rob.Wary() == 'found':
                    break
            time.sleep(.01)
        rob.forward(.2)
        time.sleep(.5)
        rob.leftM.stop()
        rob.rightM.stop()
        print("object color: ")
        objcolor = rob.cs2.color
        print(objcolor)
        time.sleep(.5)

        rob.backward(.1)
        time.sleep(.5)
        rob.leftM.stop()
        rob.rightM.stop()
        time.sleep(.3)
        rob.Grab_Obj()
        rob.forward

        while(rob.cs.color == 6):
            rob.forward(.1)
            #print(rob.wander())
            print(rob.cs.color)

        rob.run1(objcolor)

        rob.leftM.stop()
        rob.rightM.stop()

        time.sleep(.3)
        rob.backward(.3)
        rob.curve(-0.9, 0.9)
