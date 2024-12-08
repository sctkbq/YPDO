
import subprocess
import os
import shutil
import stat

import json

import requests

with open("config/config.json") as f:
    config = json.load(f)

mode = config["server"]["mode"]

if mode == "cn":
    repo_name = "Kengxxiao/ArknightsGameData"
    i, j, k = "https://github.com/Kengxxiao/ArknightsGameData.git", "zh_CN", "data"
    target_res_version = config["version"]["android"]["resVersion"]
    target_client_version = config["version"]["android"]["clientVersion"]

    l = "cn"
else:
    repo_name = "Kengxxiao/ArknightsGameData_YoStar"
    i, j, k = "https://github.com/Kengxxiao/ArknightsGameData_YoStar.git", "en_US", "data-global"
    target_res_version = config["versionGlobal"]["android"]["resVersion"]
    target_client_version = config["versionGlobal"]["android"]["clientVersion"]

    l = "global"

r = requests.get(
    f"https://api.github.com/search/commits?q=repo:{repo_name}+{
        target_client_version}+{target_res_version}&sort=author-date&order=desc"
).json()

found = False

for item in r["items"]:
    commit_message = item["commit"]["message"]
    if commit_message.find(target_client_version) != -1 and commit_message.find(target_res_version) != -1:
        found = True
        commit_hash = item["sha"]
        break

if not found:
    print("error, target version not found")
    exit(1)

print("hash:", commit_hash)

os.makedirs("tmp", exist_ok=True)

subprocess.run(["git", "init"], cwd="tmp")

subprocess.run(
    [
        "git", "fetch",
        "--depth=1", i, commit_hash
    ],
    cwd="tmp"
)


subprocess.run(
    [
        "git", "checkout", commit_hash
    ], cwd="tmp"
)

with open(f"tmp/{j}/gamedata/[uc]lua/GlobalConfig.lua") as f:
    s = f.read()


funcVer = s.partition(
    'CUR_FUNC_VER'
)[-1].partition('"')[-1].partition('"')[0]


if os.path.isdir(f"tmp/{j}/gamedata/excel/"):
    shutil.rmtree(f"{k}/excel")
    shutil.move(f"tmp/{j}/gamedata/excel/", k)


def rmtree_onerror(function, path, excinfo):
    os.chmod(path, stat.S_IWUSR)
    function(path)


shutil.rmtree("tmp/", onerror=rmtree_onerror)


old_funcVer = config["networkConfig"][l]["content"]["funcVer"]


if funcVer != old_funcVer:
    config["networkConfig"][l]["content"]["funcVer"] = funcVer
    config["networkConfig"][l]["content"]["configs"][funcVer] = config["networkConfig"][l]["content"]["configs"][old_funcVer]
    del config["networkConfig"][l]["content"]["configs"][old_funcVer]

    with open("config/config.json", "w") as f:
        json.dump(config, f, indent=4)
