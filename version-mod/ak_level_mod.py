import UnityPy
import subprocess
from zipfile import ZipFile
import os
import json
import shutil
import requests
import bson

from asset_download import download_asset_bundle

with open("settings.json") as f:
    settings = json.load(f)

target_version = settings["target_version"]


os.makedirs("tmp", exist_ok=True)
os.makedirs("mod", exist_ok=True)

if shutil.which("flatc") is None:
    flatc_url = "https://github.com/google/flatbuffers/releases/download/v23.5.26/Windows.flatc.binary.zip"
    r = requests.get(
        "https://api.github.com/repos/google/flatbuffers/releases/latest"
    )
    s = r.json()
    for i in s["assets"]:
        if i["name"].find("flatc") != -1 and i["name"].endswith(".zip") and i["name"].find("Windows") != -1:
            flatc_url = i["browser_download_url"]
            break
    flatc_file_name = os.path.basename(flatc_url)
    if not os.path.exists(flatc_file_name):
        print("Download:", flatc_file_name)
        subprocess.run(
            [
                "curl", "-L", "-O", flatc_url
            ]
        )
    print("Use:", flatc_file_name)
    with ZipFile(flatc_file_name) as f:
        f.extractall()


class AKLevelMod:
    def __init__(self) -> None:
        self.envs = {}
        self.levels = {}

    def load_level(self, asset_bundle_path, level_name):
        if asset_bundle_path not in self.envs:
            asset_bundle_name = asset_bundle_path.replace(
                '/', '_'
            ).replace(
                '#', "__"
            )+".dat"
            download_asset_bundle(target_version, asset_bundle_name)
            self.envs[asset_bundle_path] = UnityPy.load(
                f"{target_version}/{asset_bundle_path}.ab"
            )

            os.makedirs(f"tmp/{asset_bundle_path}", exist_ok=True)
        env = self.envs[asset_bundle_path]
        if (asset_bundle_path, level_name) not in self.levels:
            level_found = False
            for obj in env.objects:
                if obj.type.name == "TextAsset":
                    data = obj.read()
                    if data.name == level_name:
                        level_found = True
                        self.levels[(asset_bundle_path, level_name)] = data
                        break
            if not level_found:
                raise Exception
            data = self.levels[(asset_bundle_path, level_name)]
            with open(f"tmp/{asset_bundle_path}/{level_name}.old", "wb") as f:
                f.write(bytes(data.script)[128:])
            subprocess.run(
                [
                    "flatc",
                    "--json", "--raw-binary",
                    "-o", f"tmp/{asset_bundle_path}",
                    "--strict-json", "--natural-utf8",
                    "fbs/target_version/prts___levels.fbs",
                    "--",
                    f"tmp/{asset_bundle_path}/{level_name}.old"
                ]
            )
        with open(f"tmp/{asset_bundle_path}/{level_name}.json") as f:
            level = json.load(f)
        return level

    def save_level(self, asset_bundle_path, level_name, level):
        with open(f"tmp/{asset_bundle_path}/{level_name}.json", "w") as f:
            json.dump(level, f, indent=4)

    def clear_level(self, asset_bundle_path, level_name):
        level = self.load_level(asset_bundle_path, level_name)
        level["waves"] = [
            {
                "maxTimeWaitingForNextWave": -1.0,
                "fragments": []
            }
        ]
        self.save_level(asset_bundle_path, level_name, level)

    def add_enemy(self, asset_bundle_path, level_name, enemy_id, route_index=0, pre_delay=3.0):
        level = self.load_level(asset_bundle_path, level_name)

        enemy_db = set()
        for elem in level["enemyDbRefs"]:
            enemy_db.add(elem["id"])
        if enemy_id not in enemy_db:
            level["enemyDbRefs"].append(
                {
                    "useDb": True,
                    "id": enemy_id
                }
            )

        level["waves"][-1]["fragments"].append(
            {
                "preDelay": pre_delay,
                "actions": [
                    {
                        "managedByScheduler": True,
                        "key": enemy_id,
                        "count": 1,
                        "interval": 1.0,
                        "routeIndex": route_index,
                        "autoPreviewRoute": True,
                        "autoDisplayEnemyInfo": True
                    }
                ]
            }

        )

        self.save_level(asset_bundle_path, level_name, level)

    def save(self):
        for asset_bundle_path, level_name in self.levels:
            subprocess.run(
                [
                    "flatc",
                    "--binary",
                    "-o", f"tmp/{asset_bundle_path}",
                    "--strict-json", "--natural-utf8",
                    "fbs/target_version/prts___levels.fbs",
                    f"tmp/{asset_bundle_path}/{level_name}.json"
                ]
            )
            data = self.levels[(asset_bundle_path, level_name)]
            with open(f"tmp/{asset_bundle_path}/{level_name}.bin", "rb") as f:
                data.script = bytes(128) + f.read()
            data.save()
        for asset_bundle_path in self.envs:
            env = self.envs[asset_bundle_path]
            with open(f"tmp/{asset_bundle_path}.ab", "wb") as f:
                f.write(env.file.save())

        with ZipFile("mod/level_mod.dat", "w") as f:
            for asset_bundle_path in self.envs:
                f.write(
                    f"tmp/{asset_bundle_path}.ab",
                    f"{asset_bundle_path}.ab"
                )
