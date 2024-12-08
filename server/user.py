import json

import requests
from flask import request

from constants import USER_JSON_PATH, RLV2_JSON_PATH, SANDBOX_JSON_PATH
from utils import read_json, write_json

from faketime import time

from datetime import datetime

from sandbox import addEnemyRush

from quest import load_assist_units


def userCheckIn():

    data = request.data
    data = {
        "result": 0,
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    return data


def userChangeSecretary():

    data = request.data
    request_data = request.get_json()
    charInstId = request_data["charInstId"]
    skinId = request_data["skinId"]
    data = {
        "playerDataDelta": {
            "modified": {
                "status": {
                    "secretary": "",
                    "secretarySkinId": "",
                }
            },
            "deleted": {}
        }
    }

    secretary = skinId.split("@")[0] if "@" in skinId else skinId.split("#")[0]
    data["playerDataDelta"]["modified"]["status"]["secretary"] = secretary
    data["playerDataDelta"]["modified"]["status"]["secretarySkinId"] = skinId

    saved_data = read_json(USER_JSON_PATH)
    saved_data["user"]["status"]["secretary"] = secretary
    saved_data["user"]["status"]["secretarySkinId"] = skinId
    write_json(saved_data, USER_JSON_PATH)

    return data


def userLogin():

    data = request.data
    data = {
        "accessToken": "1",
        "birth": None,
        "channelId": "",
        "isAuthenticate": True,
        "isLatestUserAgreement": True,
        "isMinor": False,
        "needAuthenticate": False,
        "result": 0,
        "token": "abcd",
        "yostar_username": "Doctorate@doctorate.com",
        "yostar_uid": "1",
        "uid": "1"
    }

    return data


def userOAuth2V1Grant():

    data = request.data
    data = {
        "data": {
            "code": "abcd",
            "uid": "1"
        },
        "msg": "OK",
        "status": 0
    }

    return data


def userV1NeedCloudAuth():

    data = request.data
    data = {
        "msg": "OK",
        "status": 0
    }

    return data


def userV1getToken():

    data = request.data
    data = {
        "channelUid": "1",
        "error": "",
        "extension": json.dumps({
            "isMinor": False,
            "isAuthenticate": True
        }),
        "isGuest": 0,
        "result": 0,
        "token": "abcd",
        "uid": "1"
    }

    return data


def userAuth():

    data = request.data
    data = {
        "isAuthenticate": True,
        "isGuest": False,
        "isLatestUserAgreement": True,
        "isMinor": False,
        "needAuthenticate": False,
        "uid": "1"
    }

    return data


def userChangeAvatar():

    data = request.data
    avatar = request.get_json()

    saved_data = read_json(USER_JSON_PATH)
    saved_data["user"]["status"]["avatar"] = avatar
    write_json(saved_data, USER_JSON_PATH)

    data = {
        "playerDataDelta": {
            "deleted": {},
            "modified": {
                "status": {
                    "avatar": avatar
                }
            }
        }
    }

    return data


def appGetSettings():

    data = request.data
    data = requests.get(
        "https://passport.arknights.global/app/getSettings").json()
    return data


def appGetCode():

    data = request.data
    data = requests.get("https://passport.arknights.global/app/getCode").json()
    return data


def userYostarCreatelogin():

    data = request.data
    data = {
        "isNew": 0,
        "result": 0,
        "token": "1",
        "uid": "1",
        "yostar_uid": "1",
        "yostar_username": "Doctorate@doctorate.com"
    }

    return data


def userAgreement():

    data = request.data
    data = {
        "data": [
            r"¯\_(ツ)_/¯"
        ],
        "version": "4.0.0"
    }

    return data


def auth_v1_token_by_phone_password():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "token": "doctorate"
        }
    }


def info_v1_basic():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "hgId": "1",
            "phone": "doctorate",
            "email": "doctorate",
            "identityNum": "doctorate",
            "identityName": "doctorate",
            "isMinor": False,
            "isLatestUserAgreement": True
        }
    }


def oauth2_v2_grant():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "code": "doctorate",
            "uid": "1"
        }
    }


def app_v1_config():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "antiAddiction": {
                "minorPeriodEnd": 21,
                "minorPeriodStart": 20
            },
            "payment": [
                {
                    "key": "alipay",
                    "recommend": True
                },
                {
                    "key": "wechat",
                    "recommend": False
                },
                {
                    "key": "pcredit",
                    "recommend": False
                }
            ],
            "customerServiceUrl": "https://chat.hypergryph.com/chat/h5/v2/index.html",
            "cancelDeactivateUrl": "https://user.hypergryph.com/cancellation",
            "agreementUrl": {
                "game": "https://user.hypergryph.com/protocol/plain/ak/index",
                "unbind": "https://user.hypergryph.com/protocol/plain/ak/cancellation",
                "account": "https://user.hypergryph.com/protocol/plain/index",
                "privacy": "https://user.hypergryph.com/protocol/plain/privacy",
                "register": "https://user.hypergryph.com/protocol/plain/registration",
                "updateOverview": "https://user.hypergryph.com/protocol/plain/overview_of_changes",
                "childrenPrivacy": "https://user.hypergryph.com/protocol/plain/children_privacy"
            },
            "app": {
                "enablePayment": True,
                "enableAutoLogin": False,
                "enableAuthenticate": True,
                "enableAntiAddiction": True,
                "wechatAppId": "",
                "alipayAppId": "",
                "oneLoginAppId": "",
                "enablePaidApp": False,
                "appName": "明日方舟",
                "appAmount": 600
            }
        }
    }


def general_v1_server_time():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "serverTime": int(time()),
            "isHoliday": False
        }
    }


def user_changeResume():
    return {
        "playerDataDelta": {
            "modified": {
                "status": {
                    "resume": request.get_json()["resume"]
                }
            },
            "deleted": {}
        }
    }


def social_getSortListInfo():
    if request.get_json()["type"]:
        return {"result": [], "playerDataDelta": {"modified": {}, "deleted": {}}}
    request_data = request.get_json()
    command = request_data["param"]["nickName"]
    message = datetime.fromtimestamp(
        time()
    ).isoformat(timespec="seconds") + " - "
    playerDataDelta = {
        "modified": {},
        "deleted": {}
    }
    flag = False

    command_parts = command.split()
    if len(command_parts) > 0:
        if command_parts[0] == "rlv2":
            if len(command_parts) > 1:
                if command_parts[1] == "hp":
                    if len(command_parts) > 2:
                        hp = -1
                        try:
                            hp = int(command_parts[2])
                        except Exception:
                            pass
                        if hp != -1:
                            flag = True
                            rlv2 = read_json(RLV2_JSON_PATH)
                            rlv2["player"]["property"]["hp"]["current"] = hp
                            write_json(rlv2, RLV2_JSON_PATH)
                            playerDataDelta["modified"]["rlv2"] = {
                                "current": rlv2
                            }
                if command_parts[1] == "gold":
                    if len(command_parts) > 2:
                        gold = -1
                        try:
                            gold = int(command_parts[2])
                        except Exception:
                            pass
                        if gold != -1:
                            flag = True
                            rlv2 = read_json(RLV2_JSON_PATH)
                            rlv2["player"]["property"]["gold"] = gold
                            write_json(rlv2, RLV2_JSON_PATH)
                            playerDataDelta["modified"]["rlv2"] = {
                                "current": rlv2
                            }
                if command_parts[1] == "mutation":
                    if len(command_parts) > 3:
                        char_buff = None
                        try:
                            char_buff = [
                                f"rogue_2_mutation_{i}" for i in command_parts[3].split(',') if i
                            ]
                        except Exception:
                            pass
                        if char_buff is not None:
                            flag = True
                            rlv2 = read_json(RLV2_JSON_PATH)
                            for i, j in list(rlv2["troop"]["chars"].items())[::-1]:
                                if command_parts[2] in j["charId"]:
                                    j["charBuff"] = char_buff
                                    write_json(rlv2, RLV2_JSON_PATH)
                                    playerDataDelta["modified"]["rlv2"] = {
                                        "current": rlv2
                                    }
                                    break
                if command_parts[1] == "virtue":
                    if len(command_parts) > 2:
                        squad_buff = None
                        try:
                            squad_buff = [
                                f"rogue_2_virtue_{i}" for i in command_parts[2].split(',') if i
                            ]
                        except Exception:
                            pass
                        if squad_buff is not None:
                            flag = True
                            rlv2 = read_json(RLV2_JSON_PATH)
                            rlv2["buff"]["squadBuff"] = squad_buff
                            write_json(rlv2, RLV2_JSON_PATH)
                            playerDataDelta["modified"]["rlv2"] = {
                                "current": rlv2
                            }
        if command_parts[0] == "sandbox":
            if len(command_parts) > 1:
                if command_parts[1] == "season":
                    if len(command_parts) > 2:
                        season = -1
                        try:
                            season = int(command_parts[2])
                        except Exception:
                            pass
                        if season != -1:
                            flag = True
                            sandbox = read_json(SANDBOX_JSON_PATH)
                            sandbox["template"]["SANDBOX_V2"]["sandbox_1"]["main"]["map"]["season"]["type"] = season
                            write_json(sandbox, SANDBOX_JSON_PATH)
                            playerDataDelta["modified"]["sandboxPerm"] = sandbox
                if command_parts[1] == "rush":
                    if len(command_parts) > 3:
                        node_id = command_parts[2]
                        enemy_id = command_parts[3]
                        flag = True
                        sandbox = read_json(SANDBOX_JSON_PATH)
                        addEnemyRush(sandbox, node_id, enemy_id)
                        write_json(sandbox, SANDBOX_JSON_PATH)
                        playerDataDelta["modified"]["sandboxPerm"] = sandbox
    if flag:
        message += command
    else:
        message += "unknown command"
    return {
        "result": [
            {
                "level": 120,
                "uid": message
            }
        ],
        "playerDataDelta": playerDataDelta
    }


def social_searchPlayer():
    request_data = request.get_json()
    message = request_data["idList"][0]
    return {
        "players": [
            {
                "nickName": message,
                "nickNumber": "6666",
                "uid": "66666666",
                "friendNumLimit": 50,
                "serverName": "泰拉",
                "level": 120,
                "avatarId": "0",
                "avatar": {},
                "assistCharList": [
                    None
                ],
                "lastOnlineTime": 0,
                "medalBoard": {
                    "type": "EMPTY",
                    "custom": None,
                    "template": None
                },
                "skin": {
                    "selected": "nc_rhodes_default",
                    "state": {}
                }
            }
        ],
        "friendStatusList": [
            0
        ],
        "resultIdList": [
            "66666666"
        ],
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }


def social_setAssistCharList():
    return {"playerDataDelta": {"modified": {"social": request.get_json()}, "deleted": {}}}


def social_setCardShowMedal():
    request_data = request.get_json()
    return {"playerDataDelta": {"modified": {"social": {"medalBoard": {"type": request_data["type"], "template": request_data["templateGroup"]}}}, "deleted": {}}}


def medal_setCustomData():
    request_data = request.get_json()
    return {"playerDataDelta": {"modified": {"medal": {"custom": {"customs": {"1": request_data["data"]}}}}, "deleted": {}}}


def agreement_version():
    return {
        "status": 0,
        "msg": "OK",
        "data": {
            "agreementUrl": {
                "privacy": "https://user.hypergryph.com/protocol/plain/ak/privacy",
                "service": "https://user.hypergryph.com/protocol/plain/ak/service",
                "updateOverview": "https://user.hypergryph.com/protocol/plain/ak/overview_of_changes",
                "childrenPrivacy": "https://user.hypergryph.com/protocol/plain/ak/children_privacy"
            },
            "authorized": True,
            "isLatestUserAgreement": True
        }
    }

def businessCard_changeNameCardComponent():
    request_data = request.get_json()
    return {
        "playerDataDelta": {
            "modified": {
                "nameCardStyle": {
                    "componentOrder": request_data["component"]
                }
            },
            "deleted": {}
        }
    }

def businessCard_changeNameCardSkin():
    request_data = request.get_json()
    return {
        "playerDataDelta": {
            "modified": {
                "nameCardStyle": {
                    "skin": {
                        "selected": request_data["skinId"]
                    }
                }
            },
            "deleted": {}
        }
    }


def businessCard_editNameCard():
    request_data = request.get_json()
    data = {
        "playerDataDelta": {
            "modified": {
                "nameCardStyle": {}
            },
            "deleted": {}
        }
    }
    if request_data["content"]["skinId"]:
        data["playerDataDelta"]["modified"]["nameCardStyle"]["skin"] = {
            "selected": request_data["content"]["skinId"]
        }
    if request_data["content"]["component"] is not None:
        data["playerDataDelta"]["modified"]["nameCardStyle"]["componentOrder"] = request_data["content"]["component"]
    return data


def setting_perf_setLowPower():
    request_data = request.get_json()
    return {
        "playerDataDelta": {
            "modified": {
                "setting": {
                    "perf": {
                        "lowPower": request_data["newValue"]
                    }
                }
            },
            "deleted": {}
        }
    }


def businessCard_getOtherPlayerNameCard():
    request_data = request.get_json()
    uid = int(request_data["uid"])
    idx = uid - 100000000

    assist_units = load_assist_units()

    assist_unit = assist_units[idx]

    data = {
        "nameCard": {
            "nickName": "ABCDEF",
            "nickNumber": "8888",
            "uid": str(uid),
            "registerTs": 0,
            "mainStageProgress": None,
            "charCnt": 0,
            "skinCnt": 0,
            "secretary": "char_4055_bgsnow",
            "secretarySkinId": "char_4055_bgsnow#2",
            "resume": "DoctoratePy",
            "teamV2": {},
            "level": 200,
            "avatarId": "0",
            "avatar": {
                "type": "ASSISTANT",
                "id": "char_421_crow#1"
            },
            "assistCharList": [assist_unit, None, None],
            "medalBoard": {
                "type": "EMPTY",
                "custom": None,
                "template": None
            },
            "nameCardStyle": {
                "componentOrder": [
                    "module_sign",
                    "module_assist",
                    "module_medal"
                ],
                "skin": {
                    "selected": "nc_rhodes_default",
                    "state": {}
                }
            },
            "playerDataDelta": {
                "modified": {},
                "deleted": {}
            }
        }
    }
    return data


def charRotation_createPreset():
    data = request.data
    request_data = request.get_json()

    data = {
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    saved_data = read_json(USER_JSON_PATH)

    max_preset_id = 0

    for i in saved_data["user"]["charRotation"]["preset"]:
        i = int(i)
        if max_preset_id < i:
            max_preset_id = i

    max_preset_id += 1

    new_preset = {
        "name": "DoctorateUI",
        "background": "bg_rhodes_day",
        "homeTheme": "tm_rhodes_day",
        "profile": "char_002_amiya#1",
        "profileInst": 2,
        "slots": [
                {
                    "charId": "char_002_amiya",
                    "skinId": "char_002_amiya#1"
                }
        ]
    }

    saved_data["user"]["charRotation"]["preset"][str(
        max_preset_id)] = new_preset

    write_json(saved_data, USER_JSON_PATH)

    data["playerDataDelta"]["modified"]["charRotation"] = {
        "preset": {
            str(max_preset_id): new_preset
        }
    }

    return data


def charRotation_deletePreset():
    data = request.data
    request_data = request.get_json()

    preset_id = request_data["instId"]

    data = {
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    saved_data = read_json(USER_JSON_PATH)

    del saved_data["user"]["charRotation"]["preset"][preset_id]

    write_json(saved_data, USER_JSON_PATH)

    data["playerDataDelta"]["deleted"]["charRotation"] = {
        "preset": [
            preset_id
        ]
    }

    return data


def change_old_ui_based_on_charRotation(saved_data, data):
    current_preset_id = saved_data["user"]["charRotation"]["current"]
    current_preset = saved_data["user"]["charRotation"]["preset"][current_preset_id]

    secretarySkinId = current_preset["profile"]
    secretary = secretarySkinId.partition(
        '@')[0].partition('#')[0]  # erroneous for amiya

    for i in current_preset["slots"]:
        if i["skinId"] == secretarySkinId:
            secretary = i["charId"]
            break

    saved_data["user"]["status"]["secretary"] = secretary
    saved_data["user"]["status"]["secretarySkinId"] = secretarySkinId
    saved_data["user"]["background"]["selected"] = current_preset["background"]
    saved_data["user"]["homeTheme"]["selected"] = current_preset["homeTheme"]

    data["playerDataDelta"]["modified"]["status"] = {
        "secretary": saved_data["user"]["status"]["secretary"],
        "secretarySkinId": saved_data["user"]["status"]["secretarySkinId"],
    }

    data["playerDataDelta"]["modified"]["background"] = {
        "selected": saved_data["user"]["background"]["selected"]
    }
    data["playerDataDelta"]["modified"]["homeTheme"] = {
        "selected": saved_data["user"]["homeTheme"]["selected"]
    }


def charRotation_updatePreset():
    data = request.data
    request_data = request.get_json()

    preset_id = request_data["instId"]
    preset = request_data["data"]

    deleted_preset_keys = []

    for i in preset:
        if preset[i] is None:
            deleted_preset_keys.append(i)

    for i in deleted_preset_keys:
        del preset[i]

    data = {
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    saved_data = read_json(USER_JSON_PATH)

    saved_data["user"]["charRotation"]["preset"][preset_id].update(preset)

    change_old_ui_based_on_charRotation(saved_data, data)

    write_json(saved_data, USER_JSON_PATH)

    data["playerDataDelta"]["modified"]["charRotation"] = {
        "preset": {
            preset_id: preset
        }
    }

    return data


def charRotation_setCurrent():
    data = request.data
    request_data = request.get_json()

    new_current = request_data["instId"]

    data = {
        "playerDataDelta": {
            "modified": {},
            "deleted": {}
        }
    }

    saved_data = read_json(USER_JSON_PATH)

    saved_data["user"]["charRotation"]["current"] = new_current

    change_old_ui_based_on_charRotation(saved_data, data)

    write_json(saved_data, USER_JSON_PATH)

    data["playerDataDelta"]["modified"]["charRotation"] = {
        "current": new_current
    }

    return data
