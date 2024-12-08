import json
import os


with open("data/excel/gacha_table.json", encoding="utf-8") as f:
    gacha_table = json.load(f)

for i in gacha_table["gachaPoolClient"]:
    pool_id = i["gachaPoolId"]
    if not os.path.isfile(f"data/gacha/{pool_id}.json"):
        print(pool_id)
