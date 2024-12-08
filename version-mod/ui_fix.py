import UnityPy
import subprocess
from zipfile import ZipFile
import os
import json
import shutil
import requests
import bson
from UnityPy.files import SerializedFile
import random
from UnityPy.enums import TextureFormat

from asset_download import download_asset_bundle

with open("settings.json") as f:
    settings = json.load(f)

legacy_source_versions = settings["legacy_source_versions"]
legacy_activities = settings["legacy_activities"]
source_versions = settings["source_versions"]
target_version = settings["target_version"]


all_source_versions = source_versions

all_versions = all_source_versions+[target_version]

for source_version in all_versions:
    download_asset_bundle(source_version, "arts_ui_stage_[uc]homeentry.dat")

envs = {}
abs = {}
for source_version in all_versions:
    env = UnityPy.load(f"{source_version}/arts/ui/stage/[uc]homeentry.ab")
    envs[source_version] = env
    for i in env.file.files:
        file = env.file.files[i]
        if isinstance(file, SerializedFile):
            abs[source_version] = file


objs = {}
for source_version in all_versions:
    ab = abs[source_version]
    objs[source_version] = {}
    for i in ab.objects:
        obj = ab.objects[i]
        if obj.container and obj.container.startswith("assets/torappu/dynamicassets/arts/ui/stage/[uc]homeentry/"):
            if obj.type.name == "Texture2D":
                data = obj.read()
                data.image_data = data.image_data  # !!! HACK !!!
                data.save()  # !!! HACK !!!
            if obj.container not in objs[source_version]:
                objs[source_version][obj.container] = {}
            objs[source_version][obj.container][obj.type.name] = obj


def get_new_texture_and_sprite():
    env = UnityPy.load(f"{target_version}/arts/ui/stage/[uc]homeentry.ab")
    for i in env.file.files:
        file = env.file.files[i]
        if isinstance(file, SerializedFile):
            template_container_name = "assets/torappu/dynamicassets/arts/ui/stage/[uc]homeentry/main_0.png"
            texture_path_id = objs[target_version][template_container_name]["Texture2D"].path_id
            sprite_path_id = objs[target_version][template_container_name]["Sprite"].path_id
            texture_obj = file.objects[texture_path_id]
            sprite_obj = file.objects[sprite_path_id]
            return texture_obj, sprite_obj


def get_new_path_id():
    return random.randint(-(2 ** 31), 2 ** 31 - 1)


for i in os.listdir("legacy_ui"):
    i_name = os.path.splitext(i)[0]
    if "FAKE" not in objs:
        objs["FAKE"] = {}
    container_name = f"assets/torappu/dynamicassets/arts/ui/stage/[uc]homeentry/{
        i}"

    texture_obj, sprite_obj = get_new_texture_and_sprite()
    texture_obj_path_id = get_new_path_id()
    sprite_obj_path_id = get_new_path_id()

    texture_obj.path_id = texture_obj_path_id
    sprite_obj.path_id = sprite_obj_path_id

    texture_obj_data = texture_obj.read()
    texture_obj_data.m_Name = i_name
    texture_obj_data.m_TextureFormat = TextureFormat.RGBA32
    texture_obj_data.image = f"legacy_ui/{i}"
    texture_obj_data.save()

    sprite_obj_tree = sprite_obj.read_typetree()
    sprite_obj_tree["m_Name"] = i_name
    sprite_obj_tree["m_RD"]["texture"]["m_PathID"] = texture_obj_path_id
    sprite_obj.save_typetree(sprite_obj_tree)

    objs["FAKE"][container_name] = {
        "Texture2D": texture_obj,
        "Sprite": sprite_obj
    }


mods = []

for source_version in reversed(all_source_versions+["FAKE"]):
    for i in objs[source_version]:
        if i not in objs[target_version]:
            mods.append((source_version, i))
            objs[target_version][i] = objs[source_version][i]

target_ab = abs[target_version]

for i in target_ab.objects:
    obj = target_ab.objects[i]
    if obj.type.name == "MonoBehaviour":
        target_hub_obj = obj
    elif obj.type.name == "AssetBundle":
        target_ab_obj = obj

target_hub_tree = target_hub_obj.read_typetree()
target_ab_tree = target_ab_obj.read_typetree()

preload_table_size = len(target_ab_tree["m_PreloadTable"])

for source_version, i in mods:
    preload_index = preload_table_size
    preload_size = len(objs[source_version][i])
    preload_table_size += preload_size
    for j in objs[source_version][i]:
        obj = objs[source_version][i][j]
        target_ab.objects[obj.path_id] = obj
        target_ab_tree["m_PreloadTable"].append(
            {
                "m_FileID": 0,
                "m_PathID": obj.path_id
            }
        )
        target_ab_tree["m_Container"].append(
            [
                i,
                {
                    "preloadIndex": preload_index,
                    "preloadSize": preload_size,
                    "asset": {
                        "m_FileID": 0,
                        "m_PathID": obj.path_id
                    }
                }
            ]
        )
    name = os.path.splitext(os.path.basename(i))[0]
    target_hub_tree["_keys"].append(
        name
    )
    target_hub_tree["_values"].append(
        f"Arts/UI/Stage/[UC]HomeEntry/{name}"
    )

os.makedirs("tmp", exist_ok=True)
with open("tmp/hub.json", "w") as f:
    json.dump(target_hub_tree, f, indent=4)
with open("tmp/ab.json", "w") as f:
    json.dump(target_ab_tree, f, indent=4)

target_hub_obj.save_typetree(target_hub_tree)
target_ab_obj.save_typetree(target_ab_tree)

target_ab.objects = dict(sorted(target_ab.objects.items()))  # !!! HACK !!!

target_env = envs[target_version]
with open("tmp/[uc]homeentry.ab", "wb") as f:
    f.write(target_env.file.save())


os.makedirs("mod", exist_ok=True)
with ZipFile("mod/mod_ui_fix.dat", "w") as f:
    f.write("tmp/[uc]homeentry.ab", "arts/ui/stage/[uc]homeentry.ab")
