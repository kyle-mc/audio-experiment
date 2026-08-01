import os
from gtts import gTTS
from pydub import AudioSegment
import eyed3

# Game speed factor (1.7 in-game seconds for each real-time second)
GAME_SPEED = 1.7

scout_rush = {
    0: "Scout rush",        # 0 minutes 0 seconds
    25: "Villager 4 to Sheep",      # 0 minutes 25 seconds
    50: "Villager 5 to Sheep",      # 0 minutes 50 seconds
    75: "Villager 6 to Sheep",      # 1 minute 15 seconds
    100: "Villager 7 to Wood",      # 1 minute 40 seconds
    125: "Villager 8 to Wood",      # 2 minutes 5 seconds
    150: "Villager 9 to Boar",      # 2 minutes 30 seconds
    175: "Villager 10 to Boar",     # 2 minutes 55 seconds
    200: "Villager 11 to Boar",     # 3 minutes 20 seconds
    225: "Villager 12 to Boar",     # 3 minutes 45 seconds
    250: "Villager 13 to House and Berries",  # 4 minutes 10 seconds
    275: "Villager 14 to Berries",  # 4 minutes 35 seconds
    300: "Villager 15 to Berries",  # 5 minutes 0 seconds
    325: "Villager 16 to Berries",    # 5 minutes 25 seconds
    350: "Villager 17 to Boar",    # 5 minutes 50 seconds
    375: "Villager 18 to Boar",     # 6 minutes 15 seconds
    400: "Villager 19 to Wood",     # 6 minutes 40 seconds
    425: "Research Loom",           # 7 minutes 5 seconds
    450: "Click to Feudal. 9 on wood. 10 on food.",         # 7 minutes 30 seconds
    555: "Build a Stable. Research techs. Build farms.", # 9 minutes 15 seconds
    580: "Villager 20 to Straggler Trees",  # 9 minutes 40 seconds
    605: "Villager 21 to Farms",  # 10 minutes 5 seconds
    630: "Villager 22 to Farms",     # 10 minutes 30 seconds
    655: "Villager 23 to Farms",     # 10 minutes 55 seconds
    680: "Villager 24 to Farms",     # 11 minutes 20 seconds
    705: "Villager 25 to Farms",    # 11 minutes 45 seconds
    730: "Villager 26 to Farms",    # 12 minutes 10 seconds
    755: "Villager 27 to Farms",    # 12 minutes 35 seconds
    780: "Villager 28 to Gold",     # 13 minutes 0 seconds
    805: "Villager 29 to Gold",     # 13 minutes 25 seconds
    830: "Villager 30 to Gold",    # 13 minutes 50 seconds
    855: "Villager 31 to Farms",    # 14 minutes 15 seconds
    880: "Villager 32 to Farms. Build a blacksmith.",    # 14 minutes 40 seconds
    905: "Villager 33 to Farms",    # 15 minutes 5 seconds
    930: "Villager 34 to Farms",    # 15 minutes 30 seconds
    955: "Villager 35 to Farms",    # 15 minutes 55 seconds
    980: "Villager 36 to Farms"     # 16 minutes 20 seconds
}

survivalist_gpt_men_at_arms_archers = {
    0: "Men-at-Arms Archers",  # 0 minutes 0 seconds
    25: "Villager 4 to Sheep",  # 0 minutes 25 seconds
    50: "Villager 5 to Sheep",  # 0 minutes 50 seconds
    75: "Villager 6 to Sheep",  # 1 minute 15 seconds
    100: "Villager 7 to Wood",  # 1 minute 40 seconds
    125: "Villager 8 to Wood",  # 2 minutes 5 seconds
    150: "Villager 9 to Wood",  # 2 minutes 30 seconds
    175: "Villager 10 to Wood",  # 2 minutes 55 seconds
    200: "Villager 11 to Boar",  # 3 minutes 20 seconds
    225: "Villager 12 to Build two houses, then Berries",  # 3 minutes 45 seconds
    250: "Villager 13 to Berries",  # 4 minutes 10 seconds
    275: "Villager 14 to Berries",  # 4 minutes 35 seconds
    300: "Villager 15 to Berries",  # 5 minutes 0 seconds
    325: "Villager 16 to Berries",  # 5 minutes 25 seconds
    350: "Villager 17 to Berries",  # 5 minutes 50 seconds
    375: "Villager 18 to Build Barracks",  # 6 minutes 15 seconds
    400: "Villager 19 to Gold",  # 6 minutes 40 seconds
    425: "Villager 20 to Gold",  # 7 minutes 5 seconds
    450: "Villager 21 to Farms",  # 7 minutes 30 seconds
    475: "Research Loom",  # 7 minutes 55 seconds
    500: "Click to Feudal",  # 8 minutes 20 seconds
    630: "Research Men-at-Arms upgrade",  # 10 minutes 30 seconds
    655: "Research Double Bit Axe",  # 10 minutes 55 seconds
    680: "Villager 22 to Farms",  # 11 minutes 20 seconds
    705: "Build two Farms",  # 11 minutes 45 seconds
    730: "Build Blacksmith",  # 12 minutes 10 seconds
    755: "Research Fletching",  # 12 minutes 35 seconds
    780: "Build Archery Range",  # 13 minutes 0 seconds
    805: "Villager 23 to Wood",  # 13 minutes 25 seconds
    830: "Build Market",  # 13 minutes 50 seconds
    855: "Click to Castle",  # 14 minutes 15 seconds
}

maa_archers_build_order_gpt = {
    0: "Feudal Age Build",  # 0 minutes 0 seconds
    25: "Villager 4 to Sheep",  # 0 minutes 25 seconds
    50: "Villager 5 to Sheep",  # 0 minutes 50 seconds
    75: "Villager 6 to Sheep",  # 1 minute 15 seconds
    100: "Villager 7 to Wood",  # 1 minute 40 seconds
    125: "Villager 8 to Wood",  # 2 minutes 5 seconds
    150: "Villager 9 to Wood",  # 2 minutes 30 seconds
    175: "Villager 10 to Wood",  # 2 minutes 55 seconds
    200: "Villager 11 to Boar",  # 3 minutes 20 seconds
    225: "Villager 12 to Build two houses, then Berries",  # 3 minutes 45 seconds
    250: "Villager 13 to Berries",  # 4 minutes 10 seconds
    275: "Villager 14 to Berries",  # 4 minutes 35 seconds
    300: "Villager 15 to Berries",  # 5 minutes 0 seconds
    325: "Villager 16 to Berries",  # 5 minutes 25 seconds
    350: "Villager 17 to Boar",  # 5 minutes 50 seconds
    375: "Villager 18 to Boar",  # 6 minutes 15 seconds
    400: "Villager 19 to Build Barracks, then Wood",  # 6 minutes 40 seconds
    425: "Villager 21 to Gold",  # 7 minutes 5 seconds
    450: "Villager 22 to Gold",  # 7 minutes 30 seconds // I need to give a heads up on what comes next for loom and up
    475: "Research Loom",  # 7 minutes 55 seconds
    500: "Click to Feudal Age",  # 8 minutes 20 seconds (Arrive at Feudal Age: 10 minutes 55 seconds) // need to give heads up on what's next in feudal
}

feudal_age_tower_build_order_gpt = {
    0: "Tower Rush",  # 0 minutes 0 seconds
    25: "Villager 4 to Sheep",  # 0 minutes 25 seconds
    50: "Villager 5 to Sheep",  # 0 minutes 50 seconds
    75: "Villager 6 to Sheep",  # 1 minute 15 seconds
    100: "Villager 7 to Wood",  # 1 minute 40 seconds
    125: "Villager 8 to Wood",  # 2 minutes 5 seconds
    150: "Villager 9 to Boar",  # 2 minutes 30 seconds
    175: "Villager 10 to Boar",  # 2 minutes 55 seconds
    200: "Villager 11 to Berries",  # 3 minutes 20 seconds
    225: "Villager 12 to Berries",  # 3 minutes 45 seconds
    250: "Villager 13 to Sheep",  # 4 minutes 10 seconds
    275: "Villager 14 to Sheep",  # 4 minutes 35 seconds
    300: "Villager 15 to Sheep",  # 5 minutes 0 seconds
    325: "Villager 16 to Sheep",  # 5 minutes 25 seconds
    350: "Villager 17 to Sheep",  # 5 minutes 50 seconds // I need to give a heads up on what comes next for loom and up
    375: "Research Loom",  # 6 minutes 15 seconds
    400: "Click to Feudal Age",  # 6 minutes 40 seconds (Arrive at Feudal Age: 9 minutes 10 seconds) // need to give heads up on what's next in feudal
    500: "Send 4 villagers from food to build towers",
    510: "Send 4 villagers from food to stone",
}

hybrid_maps = { # https://www.youtube.com/watch?v=5KBobgUFNdw
    # Intro
        0: "Hybrid Maps",
        6: "20 vils plus loom",
        12: "3 fishing ships",
    # 6 -> Sheep
        25: "To Sheep",
        50: "To Sheep", 
        75: "To Sheep. Rally on wood.",
    # 7 -> Wood / Dock
        100: "To Wood",
        125: "To Wood",  
        150: "To Wood",  
        175: "To Wood. Rally on fish.",  
        200: "Villager 11 build Dock. Rally on wood.",  
        215: "Build 3 fishing ships",
        225: "To Wood.",
        233: "Build 3 fishing ships",
        250: "To Wood", 
        275: "To Wood. Rally on food.",  
    # Food for Feudal
        300: "To Food",  
        325: "To Food",  
        350: "To Food",
        375: "To Food",
        400: "To Food. Queue loom.",
        425: "Villager 20 to Food. Research Loom.",
    # Click Up / Fight for Water
        435: "Send vil to build second dock.",
        450: "Click Feudal Age",
        457: "13 on wood. 4 to gold.",
        467: "Fishing ships provide food. Nothing under TC.",
        580: "Research Double Bit Axe. Build two fire ships",
}

fast_castle_knights = {
    0: "Fast castle knights",            # 0 minutes 0 seconds
    25: "Villager 4 to Sheep",  # 0 minutes 25 seconds
    50: "Villager 5 to Sheep",  # 0 minutes 50 seconds
    75: "Villager 6 to Sheep",  # 1 minute 15 seconds
    100: "Villager 7 to Wood",  # 1 minute 40 seconds
    125: "Villager 8 to Wood",  # 2 minutes 5 seconds
    150: "Villager 9 to Wood",  # 2 minutes 30 seconds
    175: "Villager 10 to Wood", # 2 minutes 55 seconds
    200: "Villager 11 to Boar", # 3 minutes 20 seconds
    225: "Villager 12 to Build two houses, then Berries", # 3 minutes 45 seconds
    250: "Villager 13 to Berries", # 4 minutes 10 seconds
    275: "Villager 14 to Berries", # 4 minutes 35 seconds
    300: "Villager 15 to Berries", # 5 minutes 0 seconds
    325: "Villager 16 to Berries", # 5 minutes 25 seconds
    350: "Villager 17 to Farms", # 5 minutes 50 seconds
    375: "Villager 18 to Farms", # 6 minutes 15 seconds
    400: "Villager 19 to Lumber camp and wood", # 6 minutes 40 seconds
    425: "Villager 20 to Wood", # 7 minutes 5 seconds
    450: "Villager 21 to Wood", # 7 minutes 30 seconds
    475: "Villager 22 to Build house, then Wood", # 7 minutes 55 seconds
    500: "Villager 23 to Wood", # 8 minutes 20 seconds
    525: "Villager 24 to Wood", # 8 minutes 45 seconds
    550: "Villager 25 to Gold", # 9 minutes 10 seconds
    575: "Villager 26 to Gold", # 9 minutes 35 seconds
    600: "Villager 27 to Gold", # 10 minutes 0 seconds
    625: "Click to Feudal",     # 10 minutes 25 seconds
    675: "Build a Barracks",    # ~ 11 minutes
    755: "Build a Stable and build a Blacksmith", # 12 minutes 35 seconds
    780: "Villager 28 to Gold", # 13 minutes
    805: "Villager 29 to Gold", # 13 minutes 25 seconds
    830: "Click to Castle",     # 13 minutes 50 seconds
}

one_range_archers = {
    0: "One Range Archers",  # 0 minutes 0 seconds
    25: "To Sheep",
    50: "To Sheep",
    75: "To Sheep",
    100: "To Wood",
    125: "To Wood",
    150: "To Wood",
    175: "To Wood",
    200: "Villager 11 takes Boar",
    225: "Two houses, then Berries",
    250: "To Food",
    275: "To Food",
    300: "To Food",
    325: "To Food",
    350: "To Food",
    375: "To Food",
    400: "To Food. 19 plus loom",
    425: "To Food. Loom researching.",
    450: "Click to Feudal Age",
    465: "Nine on wood.",
    580: "Research DB Axe. Build Range.",
    595: "Mining camp. 4 on gold.",
    610: "Horse Collar.",
}

two_range_archers = {
    0: "Two Range Archers",  # 0 minutes 0 seconds
    25: "To Sheep", # Villager 4
    50: "To Sheep", # Villager 5
    75: "To Sheep", # Villager 6
    100: "To Wood", # Villager 7
    125: "To Wood", # Villager 8
    150: "To Wood", # Villager 9
    175: "To Wood", # Villager 10
    200: "Villager 11 takes Boar", # Villager 11
    225: "Two houses, then Berries", # Villager 12
    250: "To Food", # Villager 13
    275: "To Food", # Villager 14
    300: "To Food", # Villager 15
    325: "To Food", # Villager 16
    350: "To Food", # Villager 17
    375: "To Food", # Villager 18
    400: "To Food", # Villager 19
    425: "To Wood", # Villager 20
    450: "To Wood. 19 plus loom", # Villager 21
    475: "To Wood. Loom researching.", # Loom
    500: "Click to Feudal Age",
    515: "11 on wood.",
    630: "Research DB Axe. Build Two Ranges.",
    650: "Mining camp. 7 to gold.",
    670: "Blacksmith at 9 on food.",
    690: "Fletching before moving out.",
}

FILE_NAME = "two_range_archers.mp3"
COVER_ART_PATH = "C:/Users/Kyle/Dev/aoe2-audio/cover_art/two_range_archers.png"

def create_build_order(input_folder="audio",
                       output_file=FILE_NAME,
                       text_entries=two_range_archers):
    os.makedirs(input_folder, exist_ok=True)

    # 1) Generate the silent base track
    full_track = AudioSegment.silent(duration=980 * 1000)

    # 2) Overlay each TTS segment at the right in-game timestamp
    for ts, text in text_entries.items():
        tts = gTTS(text)
        tmp = os.path.join(input_folder, f"{ts}.mp3")
        tts.save(tmp)

        clip = AudioSegment.from_mp3(tmp)
        pos = int((ts / GAME_SPEED) * 1000)
        full_track = full_track.overlay(clip, position=pos)

        os.remove(tmp)

    # 3) Export combined MP3
    full_track.export(output_file, format="mp3")
    print(f"[✓] Audio exported to {output_file}")

    # 4) Load via eyed3 and set metadata + cover art
    audiofile = eyed3.load(output_file)
    if audiofile.tag is None:
        audiofile.initTag()

    # You can customize these:
    audiofile.tag.title = "AOE2 Two Range Archers Build Order"
    audiofile.tag.artist = "Generated by gTTS + pydub"
    audiofile.tag.album = "AOE2 Audio Guides"
    audiofile.tag.comments.set("Timestamps adjusted for in-game speed")

    # Embed cover art
    with open(COVER_ART_PATH, "rb") as img:
        audiofile.tag.images.set(
            3,                    # 3 = front cover
            img.read(),
            "image/png"          # or "image/jpeg" if your image is JPG
        )


    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
    print(f"[✓] Cover art and metadata embedded.")

if __name__ == "__main__":
    create_build_order()