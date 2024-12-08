import json
import frida

excluded_activity_id_set = set(["act25side", "act33side"])

with open("data/excel/activity_table.json", encoding="utf-8") as f:
    activity_table = json.load(f)
    activity_list = []
    for i in activity_table["basicInfo"]:
        if (i.endswith("side") and i not in excluded_activity_id_set) or i == "act1r6sre" or i.endswith("bossrush"):
            startTime = activity_table["basicInfo"][i]["startTime"]
            if startTime < 1678161600:
                continue
            activity_name = activity_table["basicInfo"][i]["name"]
            activity_id = activity_table["basicInfo"][i]["id"]
            activity_list.append((activity_name, activity_id))

device = frida.get_usb_device(timeout=1)

session = device.attach("arknights")

with open("activity_picker_dynamic.js", encoding="utf-8") as f:
    s = f.read()

script = session.create_script(s)
script.load()

while True:
    print("--------------------------------")
    for i, activity in enumerate(activity_list):
        print(f"[{i}]", activity[0])
    while True:
        try:
            idxs = [
                int(i)
                for i in input("Please select multiple activities, separated by white space characters: ").split()
            ]
            if max(idxs) >= len(activity_list) or min(idxs) < 0:
                raise Exception("Invalid index provided.")
            break
        except Exception as e:
            print(e)
    print(*[activity_list[idx][0] for idx in idxs], "selected.")
    script.post(','.join([activity_list[idx][1] for idx in idxs]))
