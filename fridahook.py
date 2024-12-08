import sys
from base64 import b64decode

import frida
import json

import os

import time

ADB_PATH = "platform-tools\\adb.exe"
if not os.path.isfile(ADB_PATH):
    ADB_PATH = "adb.exe"

with open("config/config.json") as f:
    config = json.load(f)

server = config["server"]
HOST = server["host"]
PORT = server["port"]
MODE = server["mode"]
NO_PROXY = server["noProxy"]
ACTIVITY_MIN_START_TS = config["userConfig"]["activityMinStartTs"]
ACTIVITY_MAX_START_TS = config["userConfig"]["activityMaxStartTs"]
VISION = config["userConfig"]["vision"]

GADGET = server["gadget"]

def on_message(message, data):
    print("[%s] => %s" % (message, data))

def main():
    os.system(f'"{ADB_PATH}" wait-for-device')
    for i in range(30):
        try:
            device = frida.get_usb_device(timeout=1)
            if GADGET:
                os.system(f'"{ADB_PATH}" reverse tcp:{PORT} tcp:{PORT}')
                session = device.attach("Gadget")

            elif MODE == "cn":
                pid = device.spawn(
                    b64decode('Y29tLmh5cGVyZ3J5cGguYXJrbmlnaHRz').decode())
                device.resume(pid)
                session = device.attach(pid)

            elif MODE == "global":
                pid = device.spawn(
                    b64decode('Y29tLllvU3RhckVOLkFya25pZ2h0cw==').decode())
                device.resume(pid)
                session = device.attach(pid, realm="emulated")
                java_session = device.attach(pid)
            break
        except Exception:
            time.sleep(1.0)

    with open("_.js", encoding="utf-8") as f:
        s = f.read()

    s = s.replace(
        "@@@DOCTORATE_HOST@@@", "NO_PROXY" if NO_PROXY else HOST, 1
    ).replace(
        "@@@DOCTORATE_PORT@@@", str(PORT), 1
    ).replace(
        "@@@DOCTORATE_ACTIVITY_MIN_START_TS@@@", str(ACTIVITY_MIN_START_TS), 1
    ).replace(
        "@@@DOCTORATE_ACTIVITY_MAX_START_TS@@@", str(ACTIVITY_MAX_START_TS), 1
    )

    script = session.create_script(s)
    script.on('message', on_message)
    script.load()
    if not GADGET and MODE == "global":
        java_script = java_session.create_script(s)
        java_script.on('message', on_message)
        java_script.load()
    if VISION:
        with open("vision.js", encoding="utf-8") as f:
            s = f.read()
        vision_script = session.create_script(s)
        vision_script.load()
    input("Press enter to exit...")
    session.detach()
    if not GADGET and MODE == "global":
        java_session.detach()

if __name__ == '__main__':
    main()
