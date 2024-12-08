from ak_level_mod import AKLevelMod

boss_level_mod = AKLevelMod()

boss_level_mod.add_enemy(
    "gamedata/levels/obt/main",
    "level_main_00-01",
    "enemy_1502_crowns",
    2
)
boss_level_mod.add_enemy(
    "gamedata/levels/obt/main",
    "level_main_00-01",
    "enemy_1504_cqbw",
    2
)
boss_level_mod.add_enemy(
    "gamedata/levels/obt/main",
    "level_main_00-01",
    "enemy_1500_skulsr",
    2
)
boss_level_mod.add_enemy(
    "gamedata/levels/obt/main",
    "level_main_00-01",
    "enemy_1501_demonk",
    2
)

level = boss_level_mod.load_level(
    "gamedata/levels/common",
    "level_hard_07-04"
)

for i in level["waves"]:
    for j in i["fragments"]:
        for k in j["actions"]:
            if k["key"] == "enemy_1081_sotisd_2":
                k["key"] = "enemy_1506_patrt"

boss_level_mod.save_level(
    "gamedata/levels/common",
    "level_hard_07-04",
    level
)

boss_level_mod.save()
