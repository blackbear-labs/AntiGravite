import asyncio
import edge_tts
from pathlib import Path
import subprocess
import imageio_ffmpeg

VOICE = "en-US-ChristopherNeural"
RATE = "+18%"
PITCH = "-1Hz"

# Concise, punchy sentences tailored for 52-54 seconds total runtime
SCRIPT_PARTS = [
    "Imagine waking up right now, and the entire global internet is completely dead. ",
    "No messages. No social media. Total digital blackout. ",
    "Within twenty-four hours, the global financial system freezes. ",
    "Credit cards are useless, and ATMs flash red error screens. ",
    "By day five, automated shipping ports grind to a halt. ",
    "Supermarket shelves are ransacked in hours as panic buying erupts. ",
    "Week two: Power grids fail, triggering massive rolling blackouts. ",
    "Entire world capitals plunge into pitch-black darkness. ",
    "By day twenty-one, society regresses fifty years. ",
    "Physical cash, fuel, and food are the only currency left. ",
    "By day thirty, two trillion dollars in global wealth is vaporized. ",
    "Millions of digital jobs cease to exist forever. ",
    "Then... without warning, the signal abruptly bursts back online. ",
    "Civilization barely survived. Could you? Drop your thoughts below."
]

FULL_TEXT = " ".join(SCRIPT_PARTS)
AUDIO_DIR = Path(__file__).resolve().parent / "assets" / "audio"
OUTPUT_FILE = AUDIO_DIR / "viral_voiceover.mp3"

async def main():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating viral voiceover (Rate: {RATE})...")
    communicate = edge_tts.Communicate(FULL_TEXT, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(str(OUTPUT_FILE))
    print(f"✅ Voiceover saved to: {OUTPUT_FILE}")
    
    # Check duration
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    res = subprocess.run([ffmpeg_exe, '-i', str(OUTPUT_FILE)], stderr=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            print(f"⏱️ {line.strip()}")

if __name__ == "__main__":
    asyncio.run(main())
