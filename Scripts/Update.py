import json
import requests
import os
import time
from Functions import discord, changelog

print("open old Lists")
brw = json.load(open(f"Brandweer.json", encoding="utf8"))
# amb = json.load(open(f"Ambulance.json", encoding="utf8"))
# kaz = json.load(open(f"Kazernes.json", encoding="utf8"))

print("Get new lists")
hulpdienstvoertuigenbenelux = requests.get("https://hulpdienstvoertuigenbenelux.nl/fetch-sheet?region=NL").json()

hulpdiensten_mapped = []

for x in hulpdienstvoertuigenbenelux["values"]:
    if len(x) < 3:
        print(x)
        print("Skipping based on array size")
        continue
    if x[0] == "-":
        print(x[0])
        print("skipping based on kazerne")
        continue
    if x[0] == "":
        print(x[0])
        print("skipping based on kazerne")
        continue
    if x[1] == "":
        print(x[1])
        print("skipping based on roepnummer")
        continue
    if x[1] == "Roepnummer":
        print(x[1])
        print("skipping based on roepnummer")
        continue
    if len(x) < 7:
        print(x)
        continue
    if not "brandweer" in str(x[6]).lower():
        print(x[6])
        print("skipping based on not brandweer")
        continue


    mapped = {
        "Regio": str(x[7]).zfill(2),
        "Kazerne": x[0],
        "Roepnummer": x[1],
        "Afkorting": x[2],
        "TypeVoertuig": x[3],
        "Kenteken": x[4],
    }

    hulpdiensten_mapped.append(mapped)

brw_new = hulpdiensten_mapped

print("Check brandweer")
for x in brw_new:
    if next((False for y in brw if y["Roepnummer"] == x["Roepnummer"]), True):
        #discord.webhook(f'{x["Roepnummer"]} has been added ```{x}```')
        changelog.update_changelog(f'Added {x["Roepnummer"]}')
        time.sleep(0.001)
        continue
    old = [z for z in brw if z["Roepnummer"]==x["Roepnummer"]]
    if not old[0] == x:
        discord.webhook(f"Entry Changed:\n ```{old[0]}```\nHas been changed to: ```{x}```")
        changelog.update_changelog(f'Updated {x["Roepnummer"]}')
        time.sleep(0.001)
        continue

for x in brw:
    if next((False for y in brw_new if y["Roepnummer"] == x["Roepnummer"]), True):
        discord.webhook(f'{x["Roepnummer"]} has been removed ```{x}```')
        changelog.update_changelog(f'Removed {x["Roepnummer"]}')
        time.sleep(0.001)
        continue

# print("Check ambulance")
# for x in amb_new:
#     if next((False for y in amb if y["Roepnummer"] == x["Roepnummer"]), True):
#         discord.webhook(f'{x["Roepnummer"]} has been added ```{x}```')
#         changelog.update_changelog(f'Added {x["Roepnummer"]}')
#         time.sleep(0.001)
#         continue
#     old = [z for z in amb if z["Roepnummer"]==x["Roepnummer"]]
#     if not old[0] == x:
#         discord.webhook(f"Entry Changed:\n ```{old[0]}```\nHas been changed to: ```{x}```")
#         changelog.update_changelog(f'Updated {x["Roepnummer"]}')
#         time.sleep(0.001)
#         continue

# for x in amb:
#     if next((False for y in amb_new if y["Roepnummer"] == x["Roepnummer"]), True):
#         discord.webhook(f'{x["Roepnummer"]} has been removed ```{x}```')
#         changelog.update_changelog(f'Removed {x["Roepnummer"]}')
#         time.sleep(0.001)
#         continue

# print("Check kazerne")
# for x in kaz_new:
#     if next((False for y in kaz if y["Regio"] == x["Regio"] and y["Kazerne naam"] == x["Kazerne naam"]), True):
#         discord.webhook(f'{x["Regio"]}-{x["Kazerne naam"]} has been added ```{x}```')
#         changelog.update_changelog(f'Added {x["Regio"]}-{x["Kazerne naam"]}')
#         time.sleep(0.001)
#         continue
#     old = [z for z in kaz if z["Regio"]==x["Regio"] and z["Kazerne naam"] == x["Kazerne naam"]]
#     if not old[0] == x:
#         discord.webhook(f"Entry Changed:\n ```{old[0]}```\nHas been changed to: ```{x}```")
#         changelog.update_changelog(f'Updated {x["Regio"]}-{x["Kazerne naam"]}')
#         time.sleep(0.001)
#         continue

# for x in kaz:
#     if next((False for y in kaz_new if y["Regio"] == x["Regio"] and y["Kazerne naam"] == x["Kazerne naam"]), True):
#         discord.webhook(f'{x["Regio"]}-{x["Kazerne naam"]} has been removed ```{x}```')
#         changelog.update_changelog(f'Removed {x["Regio"]}-{x["Kazerne naam"]}')
#         time.sleep(0.001)
#         continue

print("save the new lists")

with open(f'Brandweer.json', 'w+') as outfile_brw:
    json.dump(brw_new, outfile_brw, indent=4)

# with open(f'Ambulance.json', 'w+') as outfile_amb:
#     json.dump(amb_new, outfile_amb, indent=4)

# with open(f'Kazernes.json', 'w+') as outfile_kaz:
#     json.dump(kaz_new, outfile_kaz, indent=4)
