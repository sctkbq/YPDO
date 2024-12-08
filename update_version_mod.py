import json

with open("config/config.json") as f:
    config = json.load(f)

with open("version-mod/settings.json") as f:
    version_mod_settings = json.load(f)

if config["version"]["android"]["clientVersion"] == version_mod_settings["target_client_version"]:
    version_mod_settings["target_version"] = config["version"]["android"]["resVersion"]
    with open("version-mod/settings.json", "w") as f:
        json.dump(version_mod_settings, f, indent=4)
