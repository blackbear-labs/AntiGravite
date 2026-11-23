import asyncio
import edge_tts
from pathlib import Path

VOICE = "en-US-ChristopherNeural"
RATE = "+0%"
PITCH = "-2Hz"

TEXT = (
    "What if at this exact second, every single byte of internet on Earth vanished for thirty full days? "
    "Within seventy-two hours, the global financial system completely freezes. Credit cards are useless plastic, "
    "ATMs flash error screens, and digital banking balances literally cease to exist. "
    "By day seven, the physical world starts starving. Without GPS routing, digital inventory, and automated port logistics, "
    "cargo ships stall in oceans and supermarket shelves are stripped bare. "
    "Week two: The crisis hits our power grids. Automated supervisory control networks fail, plunging major global metropolises "
    "into rolling, pitch-black darkness. "
    "Day twenty-one: Society reverts forty years back. Physical paper cash, bartering fuel, and analogue radios become the "
    "only currency that matters as emergency services struggle to respond without dispatch software. "
    "By day thirty, over two trillion dollars in global GDP is evaporated forever, hundreds of businesses are erased, "
    "and humanity realizes just how fragile modern civilization truly is. "
    "Then... with a single click, the signal returns. But tell me honestly: could you survive thirty days without the internet? "
    "Drop your answer in the comments."
)

OUTPUT_FILE = Path(__file__).resolve().parent / "assets" / "audio" / "voiceover.mp3"

async def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    print(f"Generating voiceover with voice: {VOICE}...")
    communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(str(OUTPUT_FILE))
    print(f"Voiceover successfully saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
