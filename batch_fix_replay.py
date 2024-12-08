import json

with open("data/excel/uniequip_table.json", encoding="utf-8") as f:
    uniequip_table = json.load(f)

char_inst_id_to_first_uniequip = {}

for i in uniequip_table["charEquip"]:
    char_id = i
    char_inst_id = int(char_id.split('_')[1])
    char_inst_id_to_first_uniequip[char_inst_id] = uniequip_table["charEquip"][i][0]

with open("data/user/battleReplays.json") as f:
    battleReplays = json.load(f)

for i in battleReplays["saved"]:
    for j in battleReplays["saved"][i]:
        for k in battleReplays["saved"][i][j]["journal"]["squad"]:
            if not k["uniequipId"] and k["charInstId"] in char_inst_id_to_first_uniequip:
                k["uniequipId"] = char_inst_id_to_first_uniequip[k["charInstId"]]

with open("data/user/battleReplays.json", "w") as f:
    json.dump(battleReplays, f, indent=4)
