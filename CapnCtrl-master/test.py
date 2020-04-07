import time
from capnctrl import cap, ctrl

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
    print(len(keys))