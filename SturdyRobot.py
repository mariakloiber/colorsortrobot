import ev3dev.ev3 as ev3
import random
import time

leftspeed = .1
rightspeed = .1
held = 'False'

class SturdyRobot(object):

    default = 0.2 # good number idk??
    defaultcolor = 3

    def __init__(self, robot = None, bttn = None, leftM = 'outD', rightM = 'outA', armM = 'outC', medM = 'outB', cs = 'in3', us = 'in1', cs2 = 'in4'):
        # self.name = name

        self.bttn = ev3.Button()
        self.leftM = ev3.LargeMotor(leftM)
        self.rightM = ev3.LargeMotor(rightM)
        self.armM = ev3.LargeMotor(armM)
        self.medM = ev3.MediumMotor(medM)
        self.cs = ev3.ColorSensor('in3')
        self.us = ev3.UltrasonicSensor('in1')
        self.cs2 = ev3.ColorSensor('in4')
        self.state = 'advance'

    #speed_sp range -900 -> 900 roughly
    def forward(self, speed, time=None):
        mapSpeed = speed * 900
        if time is not None:
            self.leftM.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.rightM.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.leftM.wait_until_not_moving()
        else:
            self.leftM.run_forever(speed_sp = mapSpeed)
            self.rightM.run_forever(speed_sp = mapSpeed)
        return

    def backward(self, speed, time=None):
        mapSpeed = speed * -900
        if time is not None:
            self.leftM.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.rightM.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.leftM.wait_until_not_moving()
        else:
            self.leftM.run_forever(speed_sp = mapSpeed)
            self.rightM.run_forever(speed_sp = mapSpeed)
        return

    def turnLeft(self, speed, time=None):
        mapSpeed = speed * 900
        if time is not None:
            self.leftM.run_timed(time_sp=time, speed_sp = (-1*mapSpeed))
            self.rightM.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.leftM.wait_until_not_moving()
        else:
            self.leftM.run_forever(speed_sp = (-1*mapSpeed))
            self.rightM.run_forever(speed_sp = mapSpeed)
        return

    def turnRight(self, speed, time=None):
        mapSpeed = speed * 900
        if time is not None:
            self.leftM.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.rightM.run_timed(time_sp=time, speed_sp = (-1*mapSpeed))
            self.leftM.wait_until_not_moving()
        else:
            self.leftM.run_forever(speed_sp = mapSpeed)
            self.rightM.run_forever(speed_sp = (-1*mapSpeed))
        return

    def stop(self):
        self.leftM.stop()
        self.rightM.stop()
        return

    def curve(self, leftSpeed, rightSpeed, time=None):
        mapLeftSpeed = leftSpeed * 900
        mapRightSpeed = rightSpeed * 900
        if time is not None:
            self.leftM.run_timed(time_sp=time, speed_sp = mapLeftSpeed)
            self.rightM.run_timed(time_sp=time, speed_sp = mapRightSpeed)
            self.leftM.wait_until_not_moving()
        else:
            self.leftM.run_forever(speed_sp = mapLeftSpeed)
            self.rightM.run_forever(speed_sp = mapRightSpeed)

        return

    def zeroPointer(self):
        self.medM.run_to_abs_pos(position_sp = 0, stop_action = "hold")
        self.medM.wait_until_not_moving()
        return

    def pointerLeft(self, speed=default, time=None):
        mapSpeed = speed * -1000
        if time is not None:
            self.medM.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.medM.wait_until_not_moving()
        else:
            self.medM.run_forever(speed_sp = mapSpeed)
        return

    def pointerRight(self, speed=default, time=None):
        mapSpeed = speed * 1000
        if time is not None:
            self.medM.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.medM.wait_until_not_moving()
        else:
            self.medM.run_forever(speed_sp = mapSpeed)
        return

    def pointerTo(self, angle):
        self.medM.run_to_abs_pos(position_sp = angle, stop_action = "hold")
        self.medM.wait_until_not_moving()
        return

    def wander(self):
        global leftspeed
        global rightspeed
        leftspeed = leftspeed + random.randint(-10, 10)/100
        rightspeed = rightspeed + random.randint(-10, 10)/100
        if leftspeed < .10:
                leftspeed = .10
        if leftspeed > .25:
                leftspeed = .25
        if rightspeed < .10:
                rightspeed = .10
        if rightspeed > .25:
                rightspeed = .25
        self.curve(leftspeed,rightspeed)
        time.sleep(.1)
        return (leftspeed, rightspeed)
    def exit(self):
        global leftspeed
        global rightspeed
        lspeed = leftspeed/2
        rspeed = rightspeed/2
        self.curve(leftspeed,rightspeed)
        time.sleep(.1)
    def isBlack(self):
        if self.cs.color == 6:
            return True
        return False

    def readDistance(self):
        return self.us.distance_centimeters

    def Wary(self):
        if self.state == 'advance' and self.us.distance_centimeters <= 7:
            self.stop()
            self.state = 'found'
        elif self.state == 'found' and self.us.distance_centimeters > 7:
            self.state = 'advance'
            self.forward(0.15)
        elif self.state == 'found' and self.us.distance_centimeters <= 5:
            self.state = 'retreat'
            self.backward(0.15)
        elif self.state == 'retreat' and self.us.distance_centimeters > 5:
            self.stop()
            self.state = 'found'
        return(self.state)

    def Grab_Obj(self):
        global held
        self.armM.stop_action = 'hold'
        stoptime = 0

        # open hand
        self.medM.speed_sp = 180
        self.medM.stop_action = 'hold'
        self.medM.position_sp = -90
        self.medM.run_to_rel_pos()
        self.medM.wait_until_not_moving()
        self.medM.stop()
        stoptime = 1

        #moves arm down
        if(stoptime == 1):
             self.armM.speed_sp = 200
             self.armM.run_timed(time_sp = 2500)
             self.armM.wait_until_not_moving()


        #closes hand
        self.medM.position_sp = 90
        self.medM.run_to_rel_pos()
        self.medM.wait_until_not_moving()
        self.medM.stop()

        #moves arm up
        self.armM.speed_sp = -200
        self.armM.run_timed(time_sp = 2500)
        self.armM.wait_until_not_moving()
        # print(self.armM.is_holding)
        held = 'True'


    def runBehavior(behavObj, runTime = None):
        """Takes in a behavior object and an optional time to run. It runs
    a loop that calls the run method of the behavObj over and over until
    either the time runs out or a button is pressed."""
        buttons = ev3.Button()
        startTime = time.time()
        elapsedTime = time.time() - startTime
        ev3.Sound.speak("Starting")
        # while (not buttons.any()) and ((runTime is None) or (elapsedTime < runTime)):
        behavObj.run()
        # Could add time.sleep here if need to slow loop down
        elapsedTime = time.time() - startTime
        # break
        ev3.Sound.speak("Done")
        return

    def run1(self, objcolor=defaultcolor):
        stoptime = 0
        while(not self.cs.color == objcolor):
             if(self.cs.color == 1):
                      print(self.cs.color)
                      self.leftM.speed_sp = 100
                      self.rightM.speed_sp = -100
                      self.leftM.run_timed(time_sp = 500)
                      self.rightM.run_timed(time_sp = 500)
                      self.leftM.speed_sp = 200
                      self.rightM.speed_sp = 200
                      self.leftM.run_timed(time_sp = 500)
                      self.rightM.run_timed(time_sp = 500)
             elif(self.cs.color == 6):
                      print(self.cs.color)
                      self.leftM.speed_sp = -100
                      self.rightM.speed_sp = 100
                      self.leftM.run_timed(time_sp = 500)
                      self.rightM.run_timed(time_sp = 500)
             elif(self.cs.color == objcolor):
                      #self.leftM.speed_sp = 100
                      #self.rightM.speed_sp = 100
                      #self.leftM.run_timed(time_sp = 1000)
                      #self.rightM.run_timed(time_sp = 1000)
                      break
             else:
                      self.leftM.speed_sp = -200
                      self.rightM.speed_sp = 200
                      self.leftM.run_timed(time_sp = 2000)
                      self.rightM.run_timed(time_sp = 2000)

        self.leftM.stop()
        self.rightM.stop()
        time.sleep(2)

        stoptime = 1
        print("stoptime:")
        print(stoptime)

        if(stoptime == 1):
             self.leftM.speed_sp = 200
             self.rightM.speed_sp = 200
             self.leftM.run_timed(time_sp = 1000)
             self.rightM.run_timed(time_sp = 1000)
             self.leftM.stop()
             self.rightM.stop()
             stoptime = 2

        # move arm down
        if(stoptime == 2):
             self.armM.speed_sp = 200
             self.armM.run_timed(time_sp = 3000)
             self.armM.wait_until_not_moving()
             #time.sleep(1.5)
             stoptime = 3

        # open hand
        if(stoptime == 3):
             self.medM.speed_sp = 180
             self.medM.stop_action = 'hold'
             self.medM.position_sp = -90
             self.medM.run_to_rel_pos()
             self.medM.wait_until_not_moving()
             self.medM.stop()
             stoptime = 4

        """# move forward
        if(self.rflag == 0 and self.lflag == 0):
                self.leftM.speed_sp = 200
                self.rightM.speed_sp = 200
                self.rightM.run_timed(time_sp = 700)
                self.leftM.run_timed(time_sp = 700)
                self.leftM.wait_until_not_moving()
                self.rightM.wait_until_not_moving()
                stoptime = 1
        else:
                self.rightM.stop()
                self.leftM.stop()"""

        # move arm up
        if(stoptime == 4):
              self.armM.speed_sp = -200
              self.armM.run_timed(time_sp = 3000)
              self.armM.wait_until_not_moving()
              stoptime = 5

        # close hand motor
        if(stoptime == 5):
                #self.medM.speed_sp = 180
                #self.medM.stop_action = 'hold'

                self.medM.position_sp = 90
                self.medM.run_to_rel_pos()
                self.medM.wait_until_not_moving()
                self.armM.stop_action = 'hold'
                #self.medM.stop()
                stoptime = 6

        """# move arm up
        if(stoptime == 4):
              self.armM.speed_sp = -200
              self.armM.run_timed(time_sp = 1000)
              # move arm up again b/c of slippage
              self.armM.wait_until_not_moving()
              print(self.armM.is_holding)
              self.armM.stop_action = 'hold'
              print(self.armM.is_holding)
              stoptime = 5

        # move forwards
        if(stoptime == 4):
              self.leftM.speed_sp = 200
              self.rightM.speed_sp = 200
              self.leftM.run_timed(time_sp = 2000)
              self.rightM.run_timed(time_sp = 2000)
              self.leftM.wait_until_not_moving()
              self.rightM.wait_until_not_moving()
              self.leftM.stop()
              self.rightM.stop()
              stoptime = 5

        if(stoptime == 5):
                self.armM.speed_sp = 200
                self.armM.run_timed(time_sp = 2000)
                self.armM.wait_until_not_moving()
                self.medM.position_sp = -90
                self.medM.run_to_rel_pos()
                self.medM.wait_until_not_moving()
                self.medM.stop()
                stoptime = 6
        #       self.leftM.speed_sp = -200
        #       self.rightM.speed_sp = 200
        #       print("turning left")
        #       self.leftM.run_timed(time_sp = 3000)
        #       self.rightM.run_timed(time_sp = 3000)
        #       self.leftM.wait_until_not_moving()
        #       self.rightM.wait_until_not_moving()
        #       self.leftM.stop()
        #       self.rightM.stop()

        if(stoptime == 6):
                self.armM.speed_sp = -200
                self.armM.run_timed(time_sp = 2000)"""

        return
