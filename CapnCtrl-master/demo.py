import time
from capnctrl import cap, ctrl

frame_num = 30
total_time = 0
print("Capturing {} frames of the desktop".format(frame_num))
time.sleep(1.5)
for i in range(0,frame_num):
    start = time.time()
    img = cap.screen()
    end = time.time()
    total_time += end - start
    print("   Fps {}".format(1/(end - start)))
print("Average FPS: {}".format(frame_num/total_time))

print("Recording mouse for 3 seconds. Move around!")
time.sleep(1.5)
start = time.time()
record = []
while time.time()-start < 3:
    pos = cap.mouse()
    print(pos)
    record += [pos]
    time.sleep(0.05)

print("Mouse playback")
time.sleep(1.5)
for pos in record:
    ctrl.mouse(pos)
    time.sleep(0.05)

print("Recording keyboard. Hit ENTER when done")
record = []
keys = cap.keyboard() #clear buffer
last_keys = []
while True:
    keys = cap.keyboard()
    if "enter" in keys:
        break
    if not last_keys == keys:
        record += [keys]
        last_keys = keys
    time.sleep(0.01)

print("keyboard playback")
for keys in record:
    ctrl.key_press(*keys)

print("Mouse click test. Copies text using a submenu(hopefully, tested in mingw)")
print("Move mouse over text and hit SPACE")
keys = cap.keyboard() #clear buffer
while not "spacebar" in cap.keyboard():
    time.sleep(0.01)
# Select text
ctrl.click_down(typ="left")
ctrl.mouse((100,0),relative=True)
ctrl.click_up(typ="left")
# Open menu
ctrl.click(typ="right")
time.sleep(0.2)
# click copy
ctrl.click(pos=(10,45),typ="left",relative=True)
print("Verify copy by pasting")
