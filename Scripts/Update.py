import json
import requests
import os
import time
from Functions import discord, changelog


def get_key(x):
    roepnummer = str(x["Roepnummer"]).strip().lower()

    # Fallback key als roepnummer "geen" is
    if roepnummer == "geen" || roepnummer == "onbekend":
        return f'{x["Kazerne"]}_{x["TypeVoertuig"]}_{x["Kenteken"]}'

    return roepnummer


print("open old Lists")
brw = json.load(open(f"Brandweer.json", encoding="utf8"))

print("Get new lists")
hulpdienstvoertuigenbenelux = requests.get(
    "https://hulpdienstvoertuigenbenelux.nl/fetch-sheet?region=NL"
).json()

hulpdiensten_mapped = []

for x in hulpdienstvoertuigenbenelux["values"]:
    if len(x) < 3:
        print(x)
        print("Skipping based on array size")
        continue

    if x[0] == "-" or x[0] == "":
        print(x[0])
        print("skipping based on kazerne")
        continue

    if x[1] == "" or x[1] == "Roepnummer":
        print(x[1])
        print("skipping based on roepnummer header/leeg")
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

# ➕ NIEUWE + GEWIJZIGDE
for x in brw_new:
    if next((False for y in brw if get_key(y) == get_key(x)), True):
        # Nieuw voertuig
        discord.webhook(f'Nieuw voertuig:\n```{x}```')
        changelog.update_changelog(f'Added {x["Roepnummer"]}')
        time.sleep(0.001)
        continue

    old = [z for z in brw if get_key(z) == get_key(x)]

    if not old[0] == x:
        discord.webhook(
            f"Entry Changed:\n```{old[0]}```\nHas been changed to:\n```{x}```"
        )
        changelog.update_changelog(f'Updated {x["Roepnummer"]}')
        time.sleep(0.001)
        continue

# ➖ VERWIJDERDE
for x in brw:
    if next((False for y in brw_new if get_key(y) == get_key(x)), True):
        discord.webhook(f'Verwijderd voertuig:\n```{x}```')
        changelog.update_changelog(f'Removed {x["Roepnummer"]}')
        time.sleep(0.001)
        continue


print("save the new lists")

with open(f'Brandweer.json', 'w+', encoding="utf8") as outfile_brw:
    json.dump(brw_new, outfile_brw, indent=4, ensure_ascii=False)
