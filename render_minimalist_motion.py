#!/usr/bin/env python3
"""
Minimalist 2D Motion Graphics Video Generator Engine
Inspired by Anthem, After Effects, Linear, and SaaS Explainer Aesthetics.
Renders 9:16 (1080x1920) vertical videos with 2D vector UI cards, kinetic typography, and layered audio.
"""

import os
import sys
import argparse
import asyncio
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# External dependencies
try:
    import edge_tts
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts"], check=True)
    import edge_tts

try:
    import imageio_ffmpeg
    FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"

WIDTH = 1080
HEIGHT = 1920
FPS = 30

def get_font(size, bold=True):
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

def render_vector_card_pil(filepath, badge_text, main_title, stat_label, stat_val, color_theme="cyan"):
    """
    Renders an ultra-clean 2D minimalist motion graphic card (1080x1920)
    Inspired by Anthem / Linear / Minimalist Motion Graphics.
    """
    themes = {
        "cyan": {"accent": (0, 229, 255), "badge_bg": (0, 43, 54), "border": (0, 229, 255, 120)},
        "red": {"accent": (255, 51, 68), "badge_bg": (58, 11, 16), "border": (255, 51, 68, 120)},
        "green": {"accent": (0, 255, 102), "badge_bg": (10, 43, 20), "border": (0, 255, 102, 120)},
        "yellow": {"accent": (255, 215, 0), "badge_bg": (51, 43, 0), "border": (255, 215, 0, 120)},
        "purple": {"accent": (189, 0, 255), "badge_bg": (40, 0, 54), "border": (189, 0, 255, 120)},
    }
    t = themes.get(color_theme, themes["cyan"])
    
    # 1. Base dark matte background
    img = Image.new("RGBA", (WIDTH, HEIGHT), color=(11, 13, 17, 255))
    draw = ImageDraw.Draw(img)

    # 2. Subtle tech dot grid
    for x in range(60, 1020, 60):
        for y in range(80, 1840, 60):
            draw.point((x, y), fill=(26, 31, 42))

    # 3. Main Central Glass Container (Width: 920, Height: 1120)
    card_x0, card_y0 = 80, 400
    card_x1, card_y1 = 1000, 1520
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=36, fill=(18, 22, 30, 240), outline=t["accent"], width=2)

    # Corner brackets for HUD / motion design aesthetic
    b_len = 30
    draw.line([(card_x0 - 8, card_y0 - 8), (card_x0 + b_len, card_y0 - 8)], fill=t["accent"], width=3)
    draw.line([(card_x0 - 8, card_y0 - 8), (card_x0 - 8, card_y0 + b_len)], fill=t["accent"], width=3)
    draw.line([(card_x1 + 8, card_y1 + 8), (card_x1 - b_len, card_y1 + 8)], fill=t["accent"], width=3)
    draw.line([(card_x1 + 8, card_y1 + 8), (card_x1 + 8, card_y1 - b_len)], fill=t["accent"], width=3)

    # 4. Status Badge Pill
    badge_x, badge_y = 130, 460
    badge_w, badge_h = 440, 60
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=16, fill=t["badge_bg"], outline=t["accent"], width=1)
    
    # Pulsing status dot
    draw.ellipse([badge_x + 22, badge_y + 22, badge_x + 38, badge_y + 38], fill=t["accent"])
    font_badge = get_font(26, bold=True)
    draw.text((badge_x + 50, badge_y + 14), badge_text, font=font_badge, fill=t["accent"])

    # 5. Main Heading Title (Kinetic Typography)
    font_title = get_font(52, bold=True)
    lines = main_title.split("\\n")
    cur_y = 580
    for line in lines:
        draw.text((130, cur_y), line, font=font_title, fill=(255, 255, 255))
        cur_y += 66

    # 6. Minimalist Divider line
    draw.line([(130, 750), (950, 750)], fill=(38, 44, 58), width=2)

    # 7. Metric / Data Display Card
    box_x0, box_y0 = 130, 810
    box_x1, box_y1 = 950, 1140
    draw.rounded_rectangle([box_x0, box_y0, box_x1, box_y1], radius=24, fill=(13, 16, 22), outline=(32, 38, 50), width=2)

    font_stat_label = get_font(30, bold=False)
    draw.text((170, 850), stat_label.upper(), font=font_stat_label, fill=(136, 146, 176))

    font_stat_val = get_font(72, bold=True)
    draw.text((170, 910), stat_val, font=font_stat_val, fill=t["accent"])

    # Progress Bar Track & Fill
    bar_x0, bar_y0 = 170, 1040
    bar_x1, bar_y1 = 910, 1056
    draw.rounded_rectangle([bar_x0, bar_y0, bar_x1, bar_y1], radius=8, fill=(28, 33, 44))
    draw.rounded_rectangle([bar_x0, bar_y0, bar_x0 + 540, bar_y1], radius=8, fill=t["accent"])

    # 8. Bottom Telemetry Metadata
    font_meta = get_font(22, bold=False)
    draw.text((130, 1440), "ANTHEM MOTION ENGINE // 2D VECTOR SPEC", font=font_meta, fill=(70, 80, 100))
    draw.text((800, 1440), "60 FPS // HD", font=font_meta, fill=(70, 80, 100))

    img.convert("RGB").save(str(filepath), quality=95)

async def generate_voiceover(script_text, output_path, lang="en"):
    voice = "en-US-ChristopherNeural" if lang == "en" else "id-ID-ArdiNeural"
    rate = "+16%"
    communicate = edge_tts.Communicate(script_text, voice, rate=rate)
    await communicate.save(str(output_path))
    print(f"🎙️ Voiceover generated ({voice}) -> {output_path}")

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_ass_subtitles(filepath, subtitles):
    """Creates modern kinetic typography subtitles with highlight keywords"""
    header = f"""[Script Info]
Title: Minimalist Motion Subtitles
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: MinimalistText,Arial Black,50,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,2,0,1,6,3,2,60,60,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for start, end, l1, l2 in subtitles:
        t_start = format_ass_time(start)
        t_end = format_ass_time(end)
        
        text = f"{l1}\\N{l2}"
        text = text.replace("{CYAN}", "{\\c&H00E5FF&}")
        text = text.replace("{YELLOW}", "{\\c&H00D7FF&}")
        text = text.replace("{RED}", "{\\c&H0033FF&}")
        text = text.replace("{GREEN}", "{\\c&H00FF66&}")
        text = text.replace("{PURPLE}", "{\\c&H00FF00BD&}")
        text = text.replace("{WHITE}", "{\\c&HFFFFFF&}")
        
        events.append(f"Dialogue: 0,{t_start},{t_end},MinimalistText,,0,0,0,,{text}")
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))
    print(f"📝 Subtitles created -> {filepath}")

def render_motion_clip(img_path, output_path, duration, motion_type="snap_in"):
    total_frames = int(duration * FPS)
    if motion_type == "snap_in":
        # Snappy cubic-like acceleration into card
        motion_f = f"zoompan=z='min(zoom+0.0022,1.35)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion_type == "pull_out":
        motion_f = f"zoompan=z='if(lte(zoom,1.0),1.35,max(1.0,zoom-0.0022))':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion_type == "subtle_drift":
        motion_f = f"zoompan=z=1.18:d={total_frames}:x='if(lte(on,-1),0,min(iw-iw/zoom,x+1.5))':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    else:
        motion_f = f"zoompan=z='1.12+0.04*sin(2*PI*on/25)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"

    cmd = [
        FFMPEG_BIN, "-y",
        "-loop", "1",
        "-i", str(img_path),
        "-vf", motion_f,
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def generate_minimalist_video(config, output_file):
    work_dir = Path("./.temp_motion_engine")
    work_dir.mkdir(parents=True, exist_ok=True)
    cards_dir = work_dir / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n🚀 [1/5] Generating 2D Minimalist Vector UI Cards (Pillow Vector Engine)...")
    rendered_clips = []
    
    for i, sc in enumerate(config["scenes"]):
        card_img = cards_dir / f"card_{i:02d}.png"
        clip_vid = work_dir / f"clip_{i:02d}.mp4"
        
        render_vector_card_pil(
            card_img,
            badge_text=sc["badge"],
            main_title=sc["heading"],
            stat_label=sc["stat_label"],
            stat_val=sc["stat_val"],
            color_theme=sc["theme"]
        )
        
        render_motion_clip(card_img, clip_vid, sc["duration"], sc["motion"])
        rendered_clips.append(clip_vid)
        print(f"   ✨ Scene {i+1:02d}/{len(config['scenes'])}: [{sc['theme'].upper()}] {sc['heading'].replace(chr(92)+'n', ' ')}...")

    print("\n🎞️ [2/5] Stitching scene clips...")
    concat_txt = work_dir / "concat.txt"
    with open(concat_txt, "w") as f:
        for c in rendered_clips:
            f.write(f"file '{c.resolve().as_posix()}'\n")

    stitched_video = work_dir / "stitched_raw.mp4"
    cmd_cat = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c:v", "copy",
        str(stitched_video)
    ]
    subprocess.run(cmd_cat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print("\n🎙️ [3/5] Generating Audio Voiceover...")
    vo_file = work_dir / "voiceover.mp3"
    full_vo_text = " ".join([sc["vo"] for sc in config["scenes"]])
    asyncio.run(generate_voiceover(full_vo_text, vo_file, lang=config.get("lang", "en")))

    print("\n🎵 [4/5] Synthesizing Minimalist Electronic Suspense BGM...")
    bgm_file = work_dir / "minimal_synth_bgm.wav"
    total_dur = sum(s["duration"] for s in config["scenes"])
    
    # Modern deep pulse synth (55Hz sub + 110Hz harmonic with 120BPM pulse)
    cmd_bgm = [
        FFMPEG_BIN, "-y",
        "-f", "lavfi",
        "-i", f"aevalsrc=sin(2*PI*55*t)*0.22*(1+0.4*sin(2*PI*2.0*t)) + sin(2*PI*110*t)*0.1*(1+0.4*cos(2*PI*2.0*t)):s=44100:d={total_dur+2}",
        "-c:a", "pcm_s16le",
        str(bgm_file)
    ]
    subprocess.run(cmd_bgm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print("\n✨ [5/5] Burning Subtitles & Final Multi-Track Audio Master...")
    ass_file = work_dir / "subtitles.ass"
    generate_ass_subtitles(ass_file, config["subtitles"])
    
    ass_escaped = str(ass_file).replace("\\", "/").replace(":", "\\:")
    cmd_final = [
        FFMPEG_BIN, "-y",
        "-i", str(stitched_video),
        "-i", str(vo_file),
        "-i", str(bgm_file),
        "-filter_complex", (
            f"[0:v]subtitles='{ass_escaped}'[v_out];"
            f"[1:a]volume=1.0[a_vo];"
            f"[2:a]volume=0.20[a_bgm];"
            f"[a_vo][a_bgm]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
        ),
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "19",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_file)
    ]
    subprocess.run(cmd_final, check=True)
    print(f"\n🎉 SUCCESS! Minimalist Motion Video rendered:")
    print(f"   📍 Location: {output_file}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minimalist 2D Motion Graphics Video Generator")
    parser.add_argument("--demo", action="store_true", help="Render demo What-If video")
    parser.add_argument("--out", type=str, default="minimalist_motion_video.mp4", help="Output MP4 path")
    args = parser.parse_args()

    DEMO_CONFIG = {
        "lang": "en",
        "scenes": [
            {
                "duration": 4.5,
                "motion": "snap_in",
                "theme": "red",
                "badge": "CRITICAL INCIDENT // 00:00:00",
                "heading": "GLOBAL NETWORK\\nTERMINATION",
                "stat_label": "INTERNET TRAFFIC THROUGHPUT",
                "stat_val": "0.00 TB/s",
                "vo": "What happens if every single internet connection on Earth instantly goes offline?"
            },
            {
                "duration": 4.5,
                "motion": "pull_out",
                "theme": "yellow",
                "badge": "DAY 01 // FINANCIAL GRIDLOCK",
                "heading": "BANKING PROTOCOLS\\nFROZEN",
                "stat_label": "CARD TRANSACTIONS REJECTED",
                "stat_val": "100.0 %",
                "vo": "Day one: Every digital banking network completely freezes. Cards are useless."
            },
            {
                "duration": 4.5,
                "motion": "snap_in",
                "theme": "cyan",
                "badge": "DAY 07 // SUPPLY CHAIN",
                "heading": "LOGISTICS & PORTS\\nHALTED",
                "stat_label": "GLOBAL CARGO CONTAINER FLOW",
                "stat_val": "-98.4 %",
                "vo": "Day seven: Automated ports and supply chains halt without GPS and digital telemetry."
            },
            {
                "duration": 4.5,
                "motion": "subtle_drift",
                "theme": "red",
                "badge": "DAY 14 // INFRASTRUCTURE",
                "heading": "POWER SUBSTATIONS\\nFAILURE",
                "stat_label": "METROPOLITAN GRID STATUS",
                "stat_val": "BLACKOUT",
                "vo": "Week two: Power grids collapse under automated supervisory failure."
            },
            {
                "duration": 4.5,
                "motion": "snap_in",
                "theme": "purple",
                "badge": "DAY 30 // MACROECONOMY",
                "heading": "GLOBAL WEALTH\\nEVAPORATION",
                "stat_label": "ESTIMATED GDP WIPEOUT",
                "stat_val": "-$2.1 TRILLION",
                "vo": "By day thirty, over two trillion dollars in global GDP simply vanishes."
            },
            {
                "duration": 5.0,
                "motion": "pulse",
                "theme": "green",
                "badge": "FINAL STATUS // RECONNECTED",
                "heading": "COULD YOU SURVIVE\\n30 DAYS?",
                "stat_label": "COMMUNITY QUESTION",
                "stat_val": "COMMENT BELOW",
                "vo": "The network returns. But could you survive thirty days? Drop your answer below."
            }
        ],
        "subtitles": [
            (0.0, 4.5, "What happens if every single connection", "instantly goes {RED}OFFLINE?{WHITE}"),
            (4.5, 9.0, "Day one: Digital banking networks", "are completely {YELLOW}FROZEN.{WHITE}"),
            (9.0, 13.5, "Day seven: Global shipping ports", "drop by {CYAN}98.4 PERCENT.{WHITE}"),
            (13.5, 18.0, "Week two: Power grids fail,", "plunging cities into {RED}BLACKOUT.{WHITE}"),
            (18.0, 22.5, "By day thirty,", "{PURPLE}$2.1 TRILLION{WHITE} in GDP evaporates."),
            (22.5, 27.5, "The network returns.", "{GREEN}COULD YOU SURVIVE?{WHITE} Comment below.")
        ]
    }

    output_path = Path(args.out)
    generate_minimalist_video(DEMO_CONFIG, output_path)
