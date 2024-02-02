#!/usr/bin/python
import subprocess
import sys
import os
import json

Dir = os.getcwd()

param = sys.argv

WorldDir = param[1]
Id = param[2]
PlayerName = param[3]
Option = param[4]


print(Dir)

Level_sav2json = ["python", f"{Dir}\\convert.py", "--force", "--minify-json", f"{WorldDir}\\Level.sav"]
Level_json2sav = ["python", f"{Dir}\\convert.py", "--force", "--minify-json", f"{WorldDir}\\Level.sav.json"]

ServerPlayerUUID = f"{Id[:8].lower()}-0000-0000-0000-000000000000"
UnicodePlayerName = ascii(PlayerName)[1:-1]

if Id[-24:] == "000000000000000000000000":
  if Option == "local2server":
    PlayerFileBefore = f"{WorldDir}\\Players\\00000000000000000000000000000001.sav"
    PlayerFileAfter = f"{WorldDir}\\Players\\{Id}.sav"

    if os.path.isfile(PlayerFileAfter):
      os.remove(PlayerFileAfter)

    Player_sav2json = ["python", f"{Dir}\\convert.py", "--force", "--minify-json", PlayerFileBefore]
    Player_json2sav = ["python", f"{Dir}\\convert.py", "--force", "--minify-json", f"{PlayerFileBefore}.json"]

    subprocess.call(Level_sav2json)
    subprocess.call(Player_sav2json)

    with open(f"{PlayerFileBefore}.json", "r", encoding="utf8") as f:
      PlayerData = f.read()
    PlayerData = PlayerData.replace("00000000-0000-0000-0000-000000000001", ServerPlayerUUID)
    with open(f"{PlayerFileBefore}.json", "w", encoding="utf8") as f:
      f.write(PlayerData)
    subprocess.call(Player_json2sav)
    os.rename(PlayerFileBefore, PlayerFileAfter)
    
    with open(f"{WorldDir}\\Level.sav.json", "r", encoding="utf8") as f:
      LevelData = json.load(f)
    PlayerDatas = LevelData["properties"]["worldSaveData"]["value"]["CharacterSaveParameterMap"]["value"]
    for i in range(len(PlayerDatas)):
      PlayerDataName = PlayerDatas[i]["value"]["RawData"]["value"]["object"]["SaveParameter"]["value"]["NickName"]["value"]
      if PlayerDataName == PlayerName:
        PlayerDatas[i]["key"]["PlayerUId"]["value"] = ServerPlayerUUID
        PlayerDataUUID = PlayerDatas[i]["key"]["InstanceId"]["value"]
        break

    GroupDatas = LevelData["properties"]["worldSaveData"]["value"]["GroupSaveDataMap"]["value"]
    for j in range(len(GroupDatas)):
      GroupIDs = GroupDatas[j]["value"]["RawData"]["value"]["individual_character_handle_ids"]
      for k in range(len(GroupIDs)):
        if GroupIDs[k]["instance_id"] == PlayerDataUUID:
          GroupPlayers = GroupDatas[j]["value"]["RawData"]["value"]
          GroupIDs[k]["guid"] = ServerPlayerUUID
          break
    
    GroupPlayerDatas = GroupPlayers["players"]
    for l in range(len(GroupPlayerDatas)):
      if GroupPlayerDatas[l]["player_info"]["player_name"] == PlayerName:
        GroupPlayerDatas[l]["player_uid"] = ServerPlayerUUID
        break
    
    with open(f"{WorldDir}\\Level.sav.json", "wt", encoding="utf8") as f:
      json.dump(LevelData, f)

    subprocess.call(Level_json2sav)

    os.remove(f"{WorldDir}\\Level.sav.json")
    os.remove(f"{PlayerFileBefore}.json")

    print("Success")
    


  if Option == "server2local":
    PlayerFileBefore = f"{WorldDir}\\Players\\{Id}.sav"
    PlayerFileAfter = f"{WorldDir}\\Players\\00000000000000000000000000000001.sav"

    if os.path.isfile(PlayerFileAfter):
      os.remove(PlayerFileAfter)

    Player_sav2json = ["python", f"{Dir}\\convert.py", "--force", "--minify-json", PlayerFileBefore]
    Player_json2sav = ["python", f"{Dir}\\convert.py", "--force", "--minify-json", f"{PlayerFileBefore}.json"]

    subprocess.call(Level_sav2json)
    subprocess.call(Player_sav2json)

    with open(f"{PlayerFileBefore}.json", "r", encoding="utf8") as f:
      PlayerData = f.read()
    PlayerData = PlayerData.replace(ServerPlayerUUID, "00000000-0000-0000-0000-000000000001")
    with open(f"{PlayerFileBefore}.json", "w", encoding="utf8") as f:
      f.write(PlayerData)
    subprocess.call(Player_json2sav)
    os.rename(PlayerFileBefore, PlayerFileAfter)
    
    with open(f"{WorldDir}\\Level.sav.json", "r", encoding="utf8") as f:
      LevelData = json.load(f)
    PlayerDatas = LevelData["properties"]["worldSaveData"]["value"]["CharacterSaveParameterMap"]["value"]
    for i in range(len(PlayerDatas)):
      PlayerDataName = PlayerDatas[i]["value"]["RawData"]["value"]["object"]["SaveParameter"]["value"]["NickName"]["value"]
      if PlayerDataName == PlayerName:
        PlayerDatas[i]["key"]["PlayerUId"]["value"] = "00000000-0000-0000-0000-000000000001"
        PlayerDataUUID = PlayerDatas[i]["key"]["InstanceId"]["value"]
        break

    GroupDatas = LevelData["properties"]["worldSaveData"]["value"]["GroupSaveDataMap"]["value"]
    for j in range(len(GroupDatas)):
      GroupIDs = GroupDatas[j]["value"]["RawData"]["value"]["individual_character_handle_ids"]
      for k in range(len(GroupIDs)):
        if GroupIDs[k]["instance_id"] == PlayerDataUUID:
          GroupPlayers = GroupDatas[j]["value"]["RawData"]["value"]
          GroupIDs[k]["guid"] = "00000000-0000-0000-0000-000000000001"
          break
    
    GroupPlayerDatas = GroupPlayers["players"]
    for l in range(len(GroupPlayerDatas)):
      if GroupPlayerDatas[l]["player_info"]["player_name"] == PlayerName:
        GroupPlayerDatas[l]["player_uid"] = "00000000-0000-0000-0000-000000000001"
        break
    
    with open(f"{WorldDir}\\Level.sav.json", "wt", encoding="utf8") as f:
      json.dump(LevelData, f)

    subprocess.call(Level_json2sav)

    os.remove(f"{WorldDir}\\Level.sav.json")
    os.remove(f"{PlayerFileBefore}.json")

    print("Success")