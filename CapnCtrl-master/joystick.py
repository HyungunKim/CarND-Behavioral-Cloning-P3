
# step 1: https://sourceforge.net/projects/vjoystick/files/latest/download
# step 2: SDK: http://vjoystick.sourceforge.net/site/index.php/component/weblinks/weblink/13-uncategorised/11-redirect-vjoy2sdk?task=weblink.go
# step 3: CONST_DLL_VJOY = "vJoyInterface.dll" ...KEEP .DLL local?

# SOURCE: https://gist.github.com/Flandan/fdadd7046afee83822fcff003ab47087#file-vjoy-py

import ctypes
import struct, time

CONST_DLL_VJOY = "vJoyInterface.dll"

class vJoy:
    btn_map = {'a':0b00000001,
               'b':0b00000010,
               'x':0b00000100,
               'y':0b00001000,
               'right_bumper':0b00010000,
               'left_bumper':0b00100000,
               'start':0b01000000,
               'back':0b10000000}

    def __init__(self, idx = 1):
        self.dll = ctypes.CDLL( CONST_DLL_VJOY )
        self.idx = idx

        # init joystick state
        self.left_stick_x, self.left_stick_y = 0,0
        self.right_stick_x , self.right_stick_y = 0,0
        self.left_trigger, self.right_trigger = 0,0
        self.throttle, self.rudder, self.aileron = 0,0,0
        self.slider, self.dial, self.wheel = 0,0,0
        self.vx, self.vy, self.vz = 0,0,0
        self.vbrx, self.vbry, self.vbrz = 0,0,0
        self.bHats, self.bHatsEx1, self.bHatsEx2,self.bHatsEx3 = 0,0,0,0
        self.button_bitmask = 0b00000000

    def open(self):
        if not self.dll.AcquireVJD( self.idx ):
            raise RuntimeError("Unable to open joystick: {}".format(self.idx))

    def close(self):
        if not self.dll.RelinquishVJD( self.idx ):
            raise RuntimeError("Unable to release joystick: {}".format(self.idx))

    def _notnone(self,x,default):
        if x is not None:
            return x
        return default

    def sticks(self,left_stick_x=None, left_stick_y=None,
                    right_stick_x=None,right_stick_y=None,
                    right_trigger=None,left_trigger=None):

        self.left_stick_x = self._notnone(left_stick_x,self.left_stick_x)
        self.left_stick_y = self._notnone(left_stick_y,self.left_stick_y)
        self.right_stick_x = self._notnone(right_stick_x,self.right_stick_x)
        self.right_stick_y = self._notnone(right_stick_y,self.right_stick_y)
        self.right_trigger = self._notnone(right_trigger,self.right_trigger)
        self.left_trigger = self._notnone(left_trigger,self.left_trigger)
        self.update()

    def aux_sticks(self,throttle=None,rudder=None,aileron=None,
                slider=None,dial=None,wheel=None,
                vx=None,vy=None,vz=None,
                vbrx=None,vbry=None,vbrz=None):

        self.throttle = self._notnone(throttle,self.throttle)
        self.rudder = self._notnone(rudder,self.rudder)
        self.aileron = self._notnone(aileron,self.aileron)
        self.slider = self._notnone(slider,self.slider)
        self.dial = self._notnone(dial,self.dial)
        self.wheel = self._notnone(wheel,self.wheel)
        self.vx = self._notnone(vx,self.vx)
        self.vy = self._notnone(vy,self.vy)
        self.vz = self._notnone(vz,self.vz)
        self.vbrx = self._notnone(vx,self.vbrx)
        self.vbry = self._notnone(vy,self.vbry)
        self.vbrz = self._notnone(vz,self.vbrz)
        self.update()

    def hat_switch(self,bHats = None, bHatsEx1 = None, bHatsEx2 = None, bHatsEx3 = None):
        self.bHats = bHats,self.bHats
        self.bHatsEx1 = self._notnone(self.bHatsEx1,self.bHatsEx1)
        self.bHatsEx2 = self._notnone(self.bHatsEx2,self.bHatsEx2)
        self.bHatsEx3 = self._notnone(self.bHatsEx3,self.bHatsEx3)
        self.update()

    def button_down(self,*args):
        for btn in args:
            if btn in self.__class__.btn_map:
                self.button_bitmask |= self.__class__.btn_map[btn]
            else:
                raise ValueError("Button '{}' is not supported".format(btn))
        self.update()

    def button_up(self,*args):
        for btn in args:
            if btn in self.__class__.btn_map:
                self.button_bitmask &= ~self.__class__.btn_map[btn]
            else:
                raise ValueError("Button '{}' is not supported".format(btn))
        self.update()

    def button_press(self,*args,hold_time=0):
        self.button_down(*args)
        time.sleep(hold_time)
        self.button_up(*args)

    def update(self):
        # Left thumb stick and trigger
        wAxisX = int(min(max(-1,self.left_stick_x),1) * 16384 + 16384)
        wAxisY = int(min(max(-1,self.left_stick_y),1) * 16384 + 16384)
        wAxisZ = int(min(max(0,self.left_trigger),1) * 32767)
        # right thumb stick and trigger
        wAxisXRot = int(min(max(-1,self.right_stick_x),1) * 16384 + 16384)
        wAxisYRot = int(min(max(-1,self.right_stick_y),1) * 16384 + 16384)
        wAxisZRot = int(min(max(0,self.right_trigger),1) * 32767)
        # Auxilary axises
        wThrottle = int(min(max(0,self.throttle),1) * 32767)
        wRudder = int(min(max(-1,self.rudder),1) * 16384 + 16384)
        wAileron = int(min(max(-1,self.aileron),1) * 16384 + 16384)
        wSlider = int(min(max(0,self.slider),1) * 32767)
        wDial = int(min(max(0,self.dial),1) * 32767)
        wWheel = int(min(max(0,self.wheel),1) * 32767)
        wAxisVX = int(min(max(-1,self.vx),1) * 16384 + 16384)
        wAxisVY = int(min(max(-1,self.vy),1) * 16384 + 16384)
        wAxisVZ = int(min(max(0,self.vz),1) * 32767)
        wAxisVBRX = int(min(max(-1,self.vbrx),1) * 16384 + 16384)
        wAxisVBRY = int(min(max(-1,self.vbry),1) * 16384 + 16384)
        wAxisVBRZ = int(min(max(0,self.vbrz),1) * 32767)
        # 8 Buttons
        lButtons = self.button_bitmask
        # Hat switches
        bHats = self.bHats
        bHatsEx1 = self.bHatsEx1
        bHatsEx2 = self.bHatsEx2
        bHatsEx3 = self.bHatsEx3

        """
        typedef struct _JOYSTICK_POSITION
        {
            BYTE    bDevice; // Index of device. 1-based
            LONG    wThrottle;
            LONG    wRudder;
            LONG    wAileron;
            LONG    wAxisX;
            LONG    wAxisY;
            LONG    wAxisZ;
            LONG    wAxisXRot;
            LONG    wAxisYRot;
            LONG    wAxisZRot;
            LONG    wSlider;
            LONG    wDial;
            LONG    wWheel;
            LONG    wAxisVX;
            LONG    wAxisVY;
            LONG    wAxisVZ;
            LONG    wAxisVBRX;
            LONG    wAxisVBRY;
            LONG    wAxisVBRZ;
            LONG    lButtons;   // 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed
            DWORD   bHats;      // Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
                        DWORD   bHatsEx1;   // 16-bit of continuous HAT switch
                        DWORD   bHatsEx2;   // 16-bit of continuous HAT switch
                        DWORD   bHatsEx3;   // 16-bit of continuous HAT switch
        } JOYSTICK_POSITION, *PJOYSTICK_POSITION;
        """
        joyPosFormat = "BlllllllllllllllllllIIII"
        joyState = struct.pack( joyPosFormat, self.idx, wThrottle, wRudder,
                                   wAileron, wAxisX, wAxisY, wAxisZ, wAxisXRot, wAxisYRot,
                                   wAxisZRot, wSlider, wDial, wWheel, wAxisVX, wAxisVY, wAxisVZ,
                                   wAxisVBRX, wAxisVBRY, wAxisVBRZ, lButtons, bHats, bHatsEx1, bHatsEx2, bHatsEx3 )
        return self.dll.UpdateVJD( self.idx, joyState)

if __name__ == '__main__':
    import math
    try:
        vj = vJoy()
        vj.open()
        while True:
            vj.sticks(left_stick_x=1,left_stick_y=math.sin(time.time()))
    finally:
        vj.close()
