import os
import sys
import shutil
import subprocess
from pathlib import Path

# Resolve FFmpeg executable
def find_ffmpeg():
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"

FFMPEG = find_ffmpeg()

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
AUDIO_DIR = ASSETS_DIR / "audio"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / ".temp_viral"

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# 14 Rapid Scenes timed precisely to match 58.8s voiceover
SCENES = [
    {"img": "scene1.png", "dur": 4.2, "motion": "snap_zoom_in", "crop": "center", "title": "DAY 0: ZERO BYTES"},
    {"img": "scene1.png", "dur": 3.8, "motion": "pan_left", "crop": "top", "title": "NO SIGNAL ANYWHERE"},
    {"img": "scene2.png", "dur": 4.2, "motion": "shake_zoom", "crop": "center", "title": "DAY 1: BANKS COLLAPSE"},
    {"img": "scene2.png", "dur": 4.0, "motion": "snap_zoom_in", "crop": "bottom", "title": "ATMs: $0.00 BALANCE"},
    {"img": "scene3.png", "dur": 4.0, "motion": "slow_drift", "crop": "center", "title": "DAY 5: LOGISTICS HALTED"},
    {"img": "scene3.png", "dur": 4.0, "motion": "snap_zoom_out", "crop": "bottom", "title": "DAY 7: STORES RANSACKED"},
    {"img": "scene4.png", "dur": 4.0, "motion": "tilt_down", "crop": "center", "title": "DAY 14: POWER GRIDS DIE"},
    {"img": "scene4.png", "dur": 4.2, "motion": "slow_creep_in", "crop": "top", "title": "CITIES IN DARKNESS"},
    {"img": "scene5.png", "dur": 4.4, "motion": "slow_creep_in", "crop": "center", "title": "DAY 21: 50 YEARS BACK"},
    {"img": "scene5.png", "dur": 4.2, "motion": "pan_right", "crop": "bottom", "title": "CASH & FUEL ONLY"},
    {"img": "scene6.png", "dur": 4.4, "motion": "snap_zoom_out", "crop": "center", "title": "DAY 30: $2 TRILLION GONE"},
    {"img": "scene6.png", "dur": 4.0, "motion": "pan_left", "crop": "top", "title": "DIGITAL JOBS ERASED"},
    {"img": "scene7.png", "dur": 4.4, "motion": "snap_zoom_in", "crop": "center", "title": "SIGNAL RESTORED: ONLINE"},
    {"img": "scene7.png", "dur": 5.0, "motion": "pulse_zoom", "crop": "center", "title": "COULD YOU SURVIVE?"}
]

SUBTITLE_TIMINGS = [
    (0.0, 4.2, "Imagine waking up right now...", "and the entire global internet is {Y}COMPLETELY DEAD{W}."),
    (4.2, 8.0, "No messages. No social media.", "Total {R}DIGITAL BLACKOUT{W}."),
    (8.0, 12.2, "Within twenty-four hours,", "the global financial system {Y}FREEZES{W}."),
    (12.2, 16.2, "Credit cards are useless plastic,", "and ATMs flash {R}SYSTEM ERROR{W}."),
    (16.2, 20.2, "By day five,", "automated shipping ports {Y}GRIND TO A HALT{W}."),
    (20.2, 24.2, "Supermarket shelves are ransacked", "as {R}PANIC BUYING{W} erupts."),
    (24.2, 28.2, "Week two: Power grids fail,", "triggering {Y}MASSIVE ROLLING BLACKOUTS{W}."),
    (28.2, 32.4, "Entire world capitals plunge", "into {R}PITCH-BLACK DARKNESS{W}."),
    (32.4, 36.8, "By day twenty-one,", "human society {Y}REGRESSES 50 YEARS{W}."),
    (36.8, 41.0, "Physical cash, fuel, and food", "are the {Y}ONLY CURRENCY LEFT{W}."),
    (41.0, 45.4, "By day thirty,", "{R}$2 TRILLION{W} in wealth is vaporized."),
    (45.4, 49.4, "Millions of digital careers", "cease to exist {R}FOREVER{W}."),
    (49.4, 53.8, "Then... without warning,", "the signal abruptly {G}BURSTS BACK ONLINE{W}."),
    (53.8, 58.8, "Civilization barely survived.", "{Y}COULD YOU?{W} Drop your thoughts below.")
]

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_ass_subtitles(filepath):
    """Generates viral 2025 style ASS subtitles with high-contrast outline and keyword colors"""
    header = f"""[Script Info]
Title: Viral What If Subtitles
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ViralMain,Arial Black,54,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,1,0,0,0,100,100,2,0,1,8,4,2,60,60,380,1
Style: HookBadge,Arial Black,40,&H0000FFFF,&H000000FF,&H00000000,&HB0000000,1,0,0,0,100,100,3,0,1,6,3,8,60,60,200,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for start, end, l1, l2 in SUBTITLE_TIMINGS:
        t_start = format_ass_time(start)
        t_end = format_ass_time(end)
        
        # Replace color tags
        text = f"{l1}\\N{l2}"
        text = text.replace("{Y}", "{\\c&H00D7FF&}") # Neon Yellow
        text = text.replace("{R}", "{\\c&H0033FF&}") # Warning Red
        text = text.replace("{G}", "{\\c&H00FF66&}") # Neon Green
        text = text.replace("{W}", "{\\c&HFFFFFF&}") # White
        
        events.append(f"Dialogue: 0,{t_start},{t_end},ViralMain,,0,0,0,,{text}")
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))
    print(f"✅ Generated ASS Subtitles: {filepath}")

def get_viral_motion_filter(motion, duration):
    total_frames = int(duration * FPS)
    # High-impact motions
    if motion == "snap_zoom_in":
        # Fast punch-in from 1.05 to 1.35
        return f"zoompan=z='min(zoom+0.0025,1.38)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion == "snap_zoom_out":
        # Pull-back
        return f"zoompan=z='if(lte(zoom,1.05),1.38,max(1.05,zoom-0.0025))':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion == "shake_zoom":
        # Camera tremor + zoom
        return f"zoompan=z='min(zoom+0.002,1.3)':d={total_frames}:x='iw/2-(iw/zoom/2)+sin(on*3)*8':y='ih/2-(ih/zoom/2)+cos(on*4)*8':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion == "pan_left":
        return f"zoompan=z=1.28:d={total_frames}:x='if(lte(on,-1),iw-iw/zoom,max(0,x-2.2))':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion == "pan_right":
        return f"zoompan=z=1.28:d={total_frames}:x='if(lte(on,-1),0,min(iw-iw/zoom,x+2.2))':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion == "tilt_down":
        return f"zoompan=z=1.25:d={total_frames}:x='iw/2-(iw/zoom/2)':y='if(lte(on,-1),0,min(ih-ih/zoom,y+2.0))':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion == "pulse_zoom":
        # Heartbeat pulse zoom
        return f"zoompan=z='1.18+0.06*sin(2*PI*on/20)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    else: # slow_creep_in / default
        return f"zoompan=z='min(zoom+0.0012,1.25)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"

def render_viral_video():
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n🔥 STEP 1: Generating 2025-Style Kinetic Subtitles (.ass)...")
    ass_file = TEMP_DIR / "subtitles.ass"
    generate_ass_subtitles(ass_file)
    
    print("\n🎬 STEP 2: Rendering 14 High-Pacing Camera Cuts (Ken Burns + Vignette)...")
    rendered_clips = []
    
    for i, sc in enumerate(SCENES):
        clip_path = TEMP_DIR / f"cut_{i:02d}.mp4"
        img_path = IMAGES_DIR / sc["img"]
        motion_f = get_viral_motion_filter(sc["motion"], sc["dur"])
        
        # Dark vignette + high contrast color grading for apocalyptic mood
        grading = "vignette=PI/4,eq=contrast=1.12:brightness=-0.02:saturation=1.08"
        filter_str = f"{motion_f},{grading}"

        cmd = [
            FFMPEG, "-y",
            "-loop", "1",
            "-i", str(img_path),
            "-vf", filter_str,
            "-t", str(sc["dur"]),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-pix_fmt", "yuv420p",
            str(clip_path)
        ]
        print(f"   ⚡ Cut {i+1:02d}/14: {sc['img']} [{sc['motion']}] ({sc['dur']}s)...")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        rendered_clips.append(clip_path)

    print("\n🎞️ STEP 3: Concatenating 14 Cuts...")
    concat_list = TEMP_DIR / "concat_cuts.txt"
    with open(concat_list, "w") as f:
        for c in rendered_clips:
            f.write(f"file '{c.as_posix()}'\n")

    video_only = TEMP_DIR / "visual_stitched.mp4"
    cmd_cat = [
        FFMPEG, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c:v", "copy",
        str(video_only)
    ]
    subprocess.run(cmd_cat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print("\n🎵 STEP 4: Synthesizing Cinematic Suspense BGM & Sound Design...")
    # Generate 59s dark tension sub-bass drone with pulsing heartbeat
    bgm_file = TEMP_DIR / "cinematic_drone.wav"
    cmd_bgm = [
        FFMPEG, "-y",
        "-f", "lavfi",
        "-i", "aevalsrc=sin(2*PI*52*t)*0.25*(1+0.35*sin(2*PI*1.6*t)) + sin(2*PI*104*t)*0.12*(1+0.35*cos(2*PI*1.6*t)):s=44100:d=59",
        "-c:a", "pcm_s16le",
        str(bgm_file)
    ]
    subprocess.run(cmd_bgm, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    print("\n✨ STEP 5: Burn-in Subtitles & Audio Multi-track Mixing...")
    vo_path = AUDIO_DIR / "viral_voiceover.mp3"
    final_output = OUTPUT_DIR / "viral_what_if_58s_coba_bayangin_style.mp4"

    # Burn subtitles and mix voiceover (loud, crisp) + BGM (subtle tension -18dB)
    # Using forward slashes for ASS file path in FFmpeg filter
    ass_path_escaped = str(ass_file).replace("\\", "/").replace(":", "\\:")
    
    cmd_final = [
        FFMPEG, "-y",
        "-i", str(video_only),
        "-i", str(vo_path),
        "-i", str(bgm_file),
        "-filter_complex", (
            f"[0:v]subtitles='{ass_path_escaped}'[v_out];"
            f"[1:a]volume=1.0[a_vo];"
            f"[2:a]volume=0.22[a_bgm];"
            f"[a_vo][a_bgm]amix=inputs=2:duration=first:dropout_transition=2[a_out]"
        ),
        "-map", "[v_out]",
        "-map", "[a_out]",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(final_output)
    ]

    subprocess.run(cmd_final, check=True)
    print(f"\n🎉 ALL DONE! The viral 2025 'What If' motion video is ready:")
    print(f"   📍 File: {final_output}\n")

if __name__ == "__main__":
    try:
        render_viral_video()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during rendering: {e}", file=sys.stderr)
        sys.exit(1)
