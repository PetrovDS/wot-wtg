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
wr_tanks = ['360', '385', '400', '401', '437', '450', '451', '477', '504', '508', '511', '514', '539', '574', '582', '583', '584', '585', '586', '587', '589', '590', '591', '592', '593', '594', '595', '596', '597', '598', '599', '600', '601', '602', '603', '604', '605', '607', '608', '615', '616', '617', '618', '619', '620', '621', '622', '623', '624', '625', '626', '627', '628', '629', '630', '631', '632', '633', '634', '635', '637', '638', '642', '644', '649', '651', '674', '677', '684', '692', '693', '694', '695', '696', '697', '699', '700', '701', '709', '721', '726', '742', '747', '749', '762', '763', '765', '767', '768', '771', '772', '773', '774', '775', '776', '778', '779', '780', '781', '782', '783', '784', '785', '786', '787', '788', '789', '790', '791', '766-792', '793', '794', '467-795', '796', '797', '798', '799', '800', '801', '375-802', '803', '804', '805', '806', '807', '369-808', '809', '810', '396-811', '550-812', '813', '814', '815', '816', '817', '818', '819', '820', '821', '822', '823', '824', '825', '826', '667-827', '567-828', '365-833', '834', '382-836', '386-837', '838', '368-839', '433-840', '452-841', '842', '456-843', '469-844', '845', '568-846', '569-847', '571-848', '851', '373-855', '856', '857', '378-858', '588-859', '380-860', '861', '741-862', '578-863', '441-864', '865', '363-867', '868', '870', '372-871', '670-872', '873', '874', '612-876', '403-877', '878', '879', '420-880', '881', '429-882', '484-883', '453-884', '688-885', '886', '493-887', '888', '489-889', '506-890', '891', '892', '523-893', '525-894', '526-895', '896', '898', '410-899', '900', '543-901', '902', '572-903', '904', '905', '906', '383-907', '381-908', '910', '552-911', '455-912', '473-913', '546-914', '915-916', '459-917', '918', '919', '720-920', '481-921', '922', '675-923', '518-924', '925', '494-926', '927', '499-928', '502-929', '648-930', '509-931', '932', '691-933', '703-934', '935', '527-937', '530-939', '940', '740-951', '952', '377-953', '610-954', '955', '548-956', '387-957', '958', '959', '960', '406-961', '423-962', '963', '418-964', '965', '966', '507-967', '968', '474-969', '970', '734-971', '702-972', '520-973', '974', '738-975', '976', '977', '564-978', '979', '666-980', '981', '408-982', '682-983', '984', '399-985', '541-986', '686-988', '989', '407-990', '413-991', '718-992', '993', '687-994', '442-995', '517-996', '447-997', '439-998', '457-999', '466-1000', '730-1001', '483-1002', '732-1003', '486-1004', '733-1005', '737-1006', '537-1008', '1009', '1010', '668-1011', '724-1013', '576-1014', '1015', '394-1016', '1017', '419-1018', '440-1019', '443-1020', '744-1021', '769-1022', '712-1023', '731-1024', '488-1025', '676-1026', '505-1027', '512-1028', '515-1029', '516-1030', '1031', '536-1032', '1035', '1036', '751-1037', '680-1038', '391-1039', '392-1040', '393-1041', '850-1042', '361-1043', '362-1044', '609-1045', '364-1046', '370-1048', '565-1049', '566-1050', '723-1051', '714-1053', '704-1054', '575-1055', '570-1056', '669-1057', '829-1058', '681-1059', '366-1060', '367-1061', '540-1062', '547-1063', '371-1064', '395-1065', '374-1066', '725-1067', '715-1068', '376-1069', '683-1070', '551-1071', '409-1072', '427-1073', '379-1074', '384-1075', '542-1076', '388-1077', '671-1078', '397-1079', '716-1080', '727-1081', '398-1082', '389-1083', '468-1084', '611-1085', '777-1086', '390-1087', '705-1088', '577-1089', '402-1090', '424-1091', '553-1092', '425-1093', '426-1094', '685-1095', '405-1096', '404-1097', '1098', '428-1099', '672-1100', '411-1101', '764-1102', '412-1103', '717-1104', '414-1105', '415-1106',
            '728-1107', '416-1108', '706-1109', '417-1110', '579-1111', '580-1112', '707-1113', '708-1114', '556-1115', '454-1116', '421-1117', '544-1118', '545-1119', '554-1120', '555-1121', '430-1122', '432-1123', '434-1124', '581-1125', '613-1126', '729-1127', '438-1128', '673-1129', '710-1130', '711-1131', '698-1132', '614-1133', '558-1134', '445-1135', '448-1136', '449-1138', '422-1139', '446-1140', '573-1141', '431-1142', '458-1143', '461-1144', '462-1145', '743-1146', '463-1147', '435-1148', '436-1149', '719-1150', '464-1151', '557-1152', '460-1153', '470-1154', '444-1155', '689-1156', '492-1157', '690-1158', '475-1159', '471-1160', '713-1161', '472-1162', '476-1163', '1164', '478-1165', '479-1166', '480-1167', '745-1168', '746-1169', '559-1170', '487-1171', '485-1172', '490-1173', '560-1174', '495-1175', '496-1176', '497-1177', '498-1178', '500-1179', '503-1180', '647-1181', '748-1183', '510-1184', '561-1185', '735-1186', '513-1187', '501-1188', '736-1189', '678-1190', '562-1191', '519-1192', '521-1193', '522-1194', '491-1195', '650-1196', '563-1197', '528-1198', '606-1199', '529-1200', '722-1201', '750-1202', '531-1203', '532-1204', '533-1205', '679-1207', '524-1208', '534-1210', '535-1214', '739-1217', '1218', '1219', '1220', '1221', '1222', '1223', '1224', '1225', '1182-1226', '1227', '1228', '1229', '1230', '1231', '1232', '1233', '1234', '1235', '1236', '1237', '1238', '1239', '1240', '1241', '1242', '1243', '1244', '1245', '1246', '1247', '1248', '1249', '1250', '1251', '1252', '1253', '1254', '1255', '1256', '1257', '1258', '875-1259', '1261', '1262', '1265', '1266', '1267', '1268', '1269', '1270', '1271', '1272', '1273', '1274', '1275', '1276', '1278', '1279', '1280', '1281', '1282', '1283', '1286', '1287', '1288', '1289', '1290', '1291', '1292', '1294', '1295', '1296', '1297', '1298', '1299', '1300', '1301', '1302', '1303', '1304', '1305', '1306', '1307', '1308', '1309', '1310', '1311', '1312', '1313', '1314', '1315', '1316', '1317', '1318', '1319', '1320', '1321', '1322', '1323', '1325', '1327', '1328', '1329', '1330', '1331', '1332', '1333', '1334', '1335', '1336', '1337', '1338', '1339', '1340', '1341', '1342', '1343', '1344', '1345', '1346', '1347', '1348', '1349', '1350', '1351', '1354', '1355', '1356', '1357', '1358', '1359', '1360', '1361', '1362', '1363', '1364', '1365', '1366', '1367', '1368', '1369', '1370', '1371', '1372', '1373', '1374', '1375', '1377', '1378', '1381', '1382', '1383', '1384', '1385', '1386', '1387', '1388', '1389', '1390', '1391', '1392', '1393', '1394', '1395', '1396', '1397', '1398', '1399', '1400', '1401', '1402', '1403', '1404', '1405', '1406', '1407', '1408', '1409', '1410', '1411', '1412', '1413', '1414', '1415', '1416', '1417', '1418', '1419', '1421', '1422', '1423', '1424', '1425', '1426', '1427', '1428', '1429', '1430', '1431', '1432', '1433', '1434', '1435', '1436', '1437', '1438', '1439', '1440', '1441', '1442', '1443', '1444', '1445', '1446', '1447', '1448', '1449', '1450', '1451', '1452', '1453', '1454', '1455', '1456', '1457', '1458', '1459', '1460', '1461', '1462', '1463', '1464', '1465', '1466', '1467', '1468', '1469', '1470', '1471', '1472', '1473', '1474', '1475', '1476', '1477', '1478', '1479', '1480', '1481', '1482', '1483', '1484', '1485', '1486', '1487', '1488', '1489', '1490', '1491', '1492', '1493', '1494', '1495', '1496', '1497', '1498', '1499', '1500', '1501', '1502', '1503', '1504', '1505', '1506', '1507', '1508', '1509', '1510', '1511', '1512', '1513', '1514', '1515', '1516', '1517', '1518', '1519', '1520', '1521', '1522', '1523', '1524', '1525', '1526']




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
