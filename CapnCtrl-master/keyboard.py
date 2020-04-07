#https://gist.github.com/chriskiehl/2906125
#Giant dictonary to hold key name and VK value
VK_CODE = {'backspace':0x08,
           'tab':0x09,
           'clear':0x0C,
           'enter':0x0D,
           'shift':0x10,
           'ctrl':0x11,
           'alt':0x12,
           'pause':0x13,
           'caps_lock':0x14,
           'esc':0x1B,
           'spacebar':0x20,
           'page_up':0x21,
           'page_down':0x22,
           'end':0x23,
           'home':0x24,
           'left_arrow':0x25,
           'up_arrow':0x26,
           'right_arrow':0x27,
           'down_arrow':0x28,
           'select':0x29,
           'print':0x2A,
           'execute':0x2B,
           'print_screen':0x2C,
           'ins':0x2D,
           'del':0x2E,
           'help':0x2F,
           '0':0x30,
           '1':0x31,
           '2':0x32,
           '3':0x33,
           '4':0x34,
           '5':0x35,
           '6':0x36,
           '7':0x37,
           '8':0x38,
           '9':0x39,
           'a':0x41,
           'b':0x42,
           'c':0x43,
           'd':0x44,
           'e':0x45,
           'f':0x46,
           'g':0x47,
           'h':0x48,
           'i':0x49,
           'j':0x4A,
           'k':0x4B,
           'l':0x4C,
           'm':0x4D,
           'n':0x4E,
           'o':0x4F,
           'p':0x50,
           'q':0x51,
           'r':0x52,
           's':0x53,
           't':0x54,
           'u':0x55,
           'v':0x56,
           'w':0x57,
           'x':0x58,
           'y':0x59,
           'z':0x5A,
           'numpad_0':0x60,
           'numpad_1':0x61,
           'numpad_2':0x62,
           'numpad_3':0x63,
           'numpad_4':0x64,
           'numpad_5':0x65,
           'numpad_6':0x66,
           'numpad_7':0x67,
           'numpad_8':0x68,
           'numpad_9':0x69,
           'multiply_key':0x6A,
           'add_key':0x6B,
           'separator_key':0x6C,
           'subtract_key':0x6D,
           'decimal_key':0x6E,
           'divide_key':0x6F,
           'F1':0x70,
           'F2':0x71,
           'F3':0x72,
           'F4':0x73,
           'F5':0x74,
           'F6':0x75,
           'F7':0x76,
           'F8':0x77,
           'F9':0x78,
           'F10':0x79,
           'F11':0x7A,
           'F12':0x7B,
           'F13':0x7C,
           'F14':0x7D,
           'F15':0x7E,
           'F16':0x7F,
           'F17':0x80,
           'F18':0x81,
           'F19':0x82,
           'F20':0x83,
           'F21':0x84,
           'F22':0x85,
           'F23':0x86,
           'F24':0x87,
           'num_lock':0x90,
           'scroll_lock':0x91,
           'left_shift':0xA0,
           'right_shift':0xA1,
           'left_control':0xA2,
           'right_control':0xA3,
           'left_menu':0xA4,
           'right_menu':0xA5,
           'browser_back':0xA6,
           'browser_forward':0xA7,
           'browser_refresh':0xA8,
           'browser_stop':0xA9,
           'browser_search':0xAA,
           'browser_favorites':0xAB,
           'browser_start_and_home':0xAC,
           'volume_mute':0xAD,
           'volume_down':0xAE,
           'volume_up':0xAF,
           'next_track':0xB0,
           'previous_track':0xB1,
           'stop_media':0xB2,
           'play/pause_media':0xB3,
           'mail':0xB4,
           'select_media':0xB5,
           'start_application_1':0xB6,
           'start_application_2':0xB7,
           'attn_key':0xF6,
           'crsel_key':0xF7,
           'exsel_key':0xF8,
           'play_key':0xFA,
           'zoom_key':0xFB,
           'clear_key':0xFE,
           '+':0xBB,
           ',':0xBC,
           '-':0xBD,
           '.':0xBE,
           '/':0xBF,
           '`':0xC0,
           ';':0xBA,
           '[':0xDB,
           '\\':0xDC,
           ']':0xDD,
           "'":0xDE,
           '`':0xC0}



SCAN_CODE = {'esc':0x01,
            '1':0x02,
            '2':0x03,
            '3':0x04,
            '4':0x05,
            '5':0x06,
            '6':0x07,
            '7':0x08,
            '8':0x09,
            '9':0x0a,
            '0':0x0b,
            '-':0x0c,    # - on main keyboard
            '=':0x0d,
            'backspace':0x0e,    # backspace
            'tab':0x0f,
            'q':0x10,
            'w':0x11,
            'e':0x12,
            'r':0x13,
            't':0x14,
            'y':0x15,
            'u':0x16,
            'i':0x17,
            'o':0x18,
            'p':0x19,
            '[':0x1a,
            ']':0x1b,
            'enter':0x1c,    # enter on main keyboard
            'left_control':0x1d,
            'a':0x1e,
            's':0x1f,
            'd':0x20,
            'f':0x21,
            'g':0x22,
            'h':0x23,
            'j':0x24,
            'k':0x25,
            'l':0x26,
            ';':0x27,
            "'":0x28,
            'grave':0x29,    # accent grave
            'left_shift':0x2a,
            '\\':0x2b,
            'z':0x2c,
            'x':0x2d,
            'c':0x2e,
            'v':0x2f,
            'b':0x30,
            'n':0x31,
            'm':0x32,
            ',':0x33,
            '.':0x34,    # . on main keyboard
            '/':0x35,    # / on main keyboard
            'right_shift':0x36,
            'numpad_*':0x37,    # * on numeric keypad
            'left_menu':0x38,    # left alt
            'space':0x39,
            'caps_lock':0x3a,
            'f1':0x3b,
            'f2':0x3c,
            'f3':0x3d,
            'f4':0x3e,
            'f5':0x3f,
            'f6':0x40,
            'f7':0x41,
            'f8':0x42,
            'f9':0x43,
            'f1':0x44,
            'num_lock':0x45,
            'scroll_lock':0x46,    # scroll lock
            'numpad_7':0x47,
            'numpad_8':0x48,
            'numpad_9':0x49,
            'numpad_-':0x4a,    # - on numeric keypad_
            'numpad_4':0x4b,
            'numpad_5':0x4c,
            'numpad_6':0x4d,
            'numpad_+':0x4e,    # + on numeric keypad
            'numpad_1':0x4f,
            'numpad_2':0x50,
            'numpad_3':0x51,
            'numpad_0':0x52,
            'numpad_.':0x53,    # . on numeric keypad
            'oem_102':0x56,    # <> or \| on rt 102-key keyboard (non-u.s.)
            'f11':0x57,
            'f1':0x58,
            'f1':0x64,    #                     (nec pc98)
            'f14':0x65,    #                     (nec pc98)
            'f15':0x66,    #                     (nec pc98)
            'kana':0x70,    # (japanese keyboard)
            'abnt_c1':0x73,    # /? on brazilian keyboard
            'convert':0x79,    # (japanese keyboard)
            'noconvert':0x7b,    # (japanese keyboard)
            'yen':0x7d,    # (japanese keyboard)
            'abnt_c2':0x7e,    # numpad . on brazilian keyboard
            'numpad_=':0x8d,    # = on numeric keypad (nec pc98)
            'previous_track':0x90,    # previous track (dik_circumflex on japanese keyboard)
            'at':0x91,    #                     (nec pc98)
            ':':0x92,    #                     (nec pc98)
            '_':0x93,    #                     (nec pc98)
            'kanji':0x94,    # (japanese keyboard)
            'stop':0x95,    #                     (nec pc98)
            'ax':0x96,    #                     (japan ax)
            'unlabeled':0x97,    #                        (j3100)
            'next_track':0x99,    # next track
            'numpad_enter':0x9c,    # enter on numeric keypad
            'right_control':0x9d,
            'volume_mute':0xa0,    # mute
            'calculator':0xa1,    # calculator
            'play/pause_media':0xa2,    # play / pause
            'stop_media':0xa4,    # media stop
            'volume_down':0xae,    # volume -
            'volume_up':0xb0,    # volume +
            'webhome':0xb2,    # web home
            'numpad_,':0xb3,    # , on numeric keypad (nec pc98)
            'numpad_/':0xb5,    # / on numeric keypad
            'sysrq':0xb7,
            'right_menu':0xb8,    # right alt
            'pause':0xc5,    # pause
            'home':0xc7,    # home on arrow keypad
            'up_arrow':0xc8,    # uparrow on arrow keypad
            'page_down':0xc9,    # pgup on arrow keypad
            'left_arrow':0xcb,    # leftarrow on arrow keypad
            'right_arrow':0xcd,    # rightarrow on arrow keypad
            'end':0xcf,    # end on arrow keypad
            'down_arrow':0xd0,    # downarrow on arrow keypad
            'page_down':0xd1,    # pgdn on arrow keypad
            'insert':0xd2,    # insert on arrow keypad
            'del':0xd3,    # delete on arrow keypad
            'left_win':0xdb,    # left windows key
            'right_win':0xdc,    # right windows key
            'apps':0xdd,    # appmenu key
            'power':0xde,    # system power
            'sleep':0xdf,    # system sleep
            'wake':0xe3,    # system wake
            'browser_search':0xe5,    # browser_ search
            'browser_favorites':0xe6,    # browser_ favorites
            'browser_refresh':0xe7,    # browser_ refresh
            'browser_stop':0xe8,    # browser_ stop
            'browser_forward':0xe9,    # browser_ forward
            'browser_back':0xea,    # web back
            'mycomputer':0xeb,    # my computer
            'mail':0xec,    # mail
            'select_media':0xed}    # media select


#SendInput = ctypes.windll.user32.SendInput

import ctypes
import time

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]



def _key_down(*args):
    for i in args:
        hexKeyCode = SCAN_CODE[i.lower()]
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def _key_up(*args):
    for i in args:
        hexKeyCode = SCAN_CODE[i.lower()]
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
        x = Input( ctypes.c_ulong(1), ii_ )
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def _key_press(*args,hold_time=0):
    _key_down(*args)
    time.sleep(0.05)
    _key_up(*args)
