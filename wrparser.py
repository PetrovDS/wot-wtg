from bs4 import BeautifulSoup
import requests as req
from os import system
from time import time
from tqdm import tqdm
import pandas as pd
import struct
import json
import sys
import os

maps = pd.read_csv("data/assets/maps.csv")
tanks = pd.read_csv("data/assets/tanks.csv")




#for i_tank, tank in enumerate(wr_tanks):
i_tank = 0
tank = sys.argv[1]

if True:
    for i_map, map_ in enumerate(maps):
        player = None
        for team in [1, 2]:
            timer = time()
            df = pd.DataFrame(columns=['map', 'mode', 'team', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7',
                                       't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17',
                                       't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27',
                                       't28', 't29', 'x0', 'y0', 'x15', 'y15', 'x30', 'y30', 'x45', 'y45',
                                       'x60', 'y60'])
            page = 0
            links = []
            while page != 10:
                page += 1
                try:
                    html = BeautifulSoup(req.get(
                        f"http://wotreplays.ru/site/index/version/87,86,85,84,83,82,81,80,79,78,77,76,75,74,73,71,72,70,69,68,64,67,66,65,63,62,61,60,59,58,56,55,54,53,52,51,50,49,48,45,46,44,43,42,41,40,38,22,37,36,35,34,33,31,30,29,28,27,26,25,24,23,21,19,17,16,14,13,7,6,5,4,1,2,3,18,47,20,32,39,57/battle_type/1/tank/{tank}/ace/1/respawn/{team}/map/{map_}/sort/uploaded_at.desc/page/{page}").text, 'lxml')
                    page_links = [el.get("href")
                                  for el in html.find_all(class_="btn_l-grey")[:-1]]
                except:
                    break

                if len(page_links) == 0 or (page != 1 and links[0] == page_links[0]):
                    break

                links += page_links

            print(
                f"{i_tank+1}/{len(wr_tanks)}, {i_map+1}/{len(maps)}, {team}/2, replays: {len(links)}")

            for link in tqdm(links):
                replay_path = f"tmp/replay{tank}.wotreplay"
                open(replay_path,
                     'wb').write(req.get("http://wotreplays.ru"+link).content)

                with open(replay_path, "rb") as replay_file:
                    replay = replay_file.read()

                if replay.find(b'404 Not Found') != -1:
                    continue

                json_list = []
                try:
                    obj_count = struct.unpack("I", replay[4:8])[0]
                    pos = 8
                    for i in range(obj_count):
                        json_size = struct.unpack("I", replay[pos:pos+4])[0]
                        json_start = pos + 4
                        json_end = json_size + pos + 4
                        json_list.append(json.loads(
                            replay[json_start:json_end]))
                        pos = json_end
                except:
                    continue

                player_name = json_list[0]['playerName']
                map_name = json_list[0]['mapName']
                mode = json_list[0]['gameplayID']
                player_ID = [int(i) for i in json_list[0]["vehicles"]
                             if json_list[0]["vehicles"][i]["name"] == player_name][0]
                player = [{
                    "id": "t0",
                    "veh": json_list[0]["vehicles"][str(player_ID)]["vehicleType"][json_list[0]["vehicles"][str(player_ID)]["vehicleType"].find(":")+1:],
                    "team": json_list[0]["vehicles"][str(player_ID)]["team"]
                }]
                players = [{
                    "veh": json_list[0]["vehicles"][i]["vehicleType"][json_list[0]["vehicles"][i]["vehicleType"].find(":")+1:],
                    "team": json_list[0]["vehicles"][i]["team"]
                } for i in json_list[0]["vehicles"] if json_list[0]["vehicles"][i]["name"] != player_name]

                tmp_sys = system(
                    f".\\main.exe -out tmp\\replay{tank}.dat tmp\\replay{tank}.wotreplay > tmp\\log{tank}.tmp")

                packets = []
                cur = 0
                flag = True
                start_time = None
                coords = [[] for i in range(5)]

                with open(f"tmp/replay{tank}.dat", "rb") as data:
                    while True:
                        b = data.read(8)
                        if not b:
                            break
                        pack_size, pack_type = struct.unpack("II", b)
                        if pack_type == 10 and pack_size == 45:
                            data.seek(data.tell() - 8)
                            pack_0a = struct.unpack(
                                "IIfIIfffffffff?", data.read(12 + pack_size))
                            if player_ID == pack_0a[3]:
                                if flag:
                                    x, z, y = pack_0a[5:8]
                                    flag = False
                                if (abs(x - pack_0a[5]) > .01) and (abs(y - pack_0a[7]) > .01) and (start_time is None):
                                    start_time = pack_0a[2]
                                if start_time is not None:
                                    if not coords[0]:
                                        coords[0] = pack_0a[5:8:2]
                                    elif start_time + 15 < pack_0a[2] and not coords[1]:
                                        coords[1] = pack_0a[5:8:2]
                                    elif start_time + 30 < pack_0a[2] and not coords[2]:
                                        coords[2] = pack_0a[5:8:2]
                                    elif start_time + 45 < pack_0a[2] and not coords[3]:
                                        coords[3] = pack_0a[5:8:2]
                                    elif start_time + 60 < pack_0a[2] and not coords[4]:
                                        coords[4] = pack_0a[5:8:2]
                                        break
                                x, z, y = pack_0a[5:8]
                        else:
                            data.seek(data.tell() + pack_size + 4)
                coords = [j for i in coords for j in i]

                try:
                    veh = pd.DataFrame(players).sort_values(by="team").veh
                    veh.index = ["t"+str(i) for i in range(1, 30)]
                    battle = pd.concat([
                        pd.Series([link, map_name, mode, player[0]["team"]], index=[
                                  "link", "map", "g_mode", "team"]),
                        pd.DataFrame(player).set_index("id").veh,
                        veh,
                        pd.Series(map(int, coords), index=[
                                  i+str(j) for j in range(0, 61, 15) for i in "xy"])
                    ])

                    df = pd.concat([df, pd.DataFrame(battle).T])
                except:
                    pass
            if player is not None:
                csv_name = "data/"+player[0]["veh"]+"#" + \
                    map_name+"#"+str(player[0]["team"])+".csv"
                df.to_csv(csv_name)
            else:
                csv_name = ""
            print(csv_name, len(df), "боёв.",
                  "| Время:", time() - timer, "сек")
print("Done")
os.system("title Done")
