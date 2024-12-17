import os
import requests

from utils import read_json, write_json
from constants import CONFIG_PATH

from . import loadMods


def updateData(url):

    BASE_URL_LIST = [
        ("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata", './data'),
        ("https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata", './data-global'),
        ("https://ak-conf.hypergryph.com/config/prod/announce_meta/Android", './data/announce'),
        ("https://ark-us-static-online.yo-star.com/announce/Android", './data/announce'),
    ]

    server_config = read_json(CONFIG_PATH)

    version_redirection = server_config["assets"]["versionRedirection"]

    if version_redirection:
        mode = server_config["server"]["mode"]

        if mode == "cn":
            res_version = server_config["version"]["android"]["resVersion"]
        else:
            res_version = server_config["versionGlobal"]["android"]["resVersion"]

    for index in BASE_URL_LIST:
        if index[0] in url:
            local_dir = index[1]
            if version_redirection:
                local_dir += f"/{res_version}"
            if not os.path.isdir(local_dir):
                os.makedirs(local_dir)
            localPath = url.replace(index[0], local_dir)
            break

    if not os.path.isdir('./data/excel/'):
        os.makedirs('./data/excel/')

    if "Android/version" in url:
        data = requests.get(url).json()
        return data

#    loaded_mods = loadMods.loadMods(log=False)
#    current_url = os.path.splitext(os.path.basename(url))[0]
    current_is_mod = False
#
#    if server_config["assets"]["enableMods"]:
#        for mod in loaded_mods["name"]:
#            if current_url in mod:
#                current_is_mod = True
#                break
    
    if not current_is_mod:
        try:
            raise Exception
            data = requests.get(url).json()
            write_json(data, localPath)

        except:
            data = read_json(localPath, encoding = "utf-8")
    else:
        data = read_json(localPath, encoding = "utf-8")

    return data
