import os
import sys
import shutil
import subprocess
from pathlib import Path

# Resolve FFmpeg binary (prefer system ffmpeg, fallback to imageio_ffmpeg)
def find_ffmpeg():
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"

FFMPEG_BIN = find_ffmpeg()

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
AUDIO_DIR = ASSETS_DIR / "audio"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / ".temp"

# Target Specification: 9:16 Vertical Video (1080x1920) for Smartphone / TikTok / Shorts
WIDTH = 1080
HEIGHT = 1920
FPS = 30

# 7 Scenes Total: 7 + 8 + 8 + 8 + 9 + 10 + 8 = 58 Seconds
SCENES = [
    {
        "id": "scene1",
        "file": "scene1.png",
        "duration": 7,
        "motion": "zoom_in",
        "title": "DAY 0: TOTAL DISCONNECT"
    },
    {
        "id": "scene2",
        "file": "scene2.png",
        "duration": 8,
        "motion": "pan_right",
        "title": "DAY 3: $10T FINANCIAL FREEZE"
    },
    {
        "id": "scene3",
        "file": "scene3.png",
        "duration": 8,
        "motion": "zoom_out",
        "title": "DAY 7: SUPPLY CHAINS COLLAPSE"
    },
    {
        "id": "scene4",
        "file": "scene4.png",
        "duration": 8,
        "motion": "pan_down",
        "title": "DAY 14: POWER GRIDS DIE"
    },
    {
        "id": "scene5",
        "file": "scene5.png",
        "duration": 9,
        "motion": "zoom_in",
        "title": "DAY 21: CASH & ANALOGUE SURVIVAL"
    },
    {
        "id": "scene6",
        "file": "scene6.png",
        "duration": 10,
        "motion": "zoom_out",
        "title": "DAY 30: $2 TRILLION ECONOMIC VOID"
    },
    {
        "id": "scene7",
        "file": "scene7.png",
        "duration": 8,
        "motion": "zoom_in",
        "title": "COULD YOU SURVIVE 30 DAYS?"
    }
]

def ensure_directories():
    for d in [IMAGES_DIR, AUDIO_DIR, OUTPUT_DIR, TEMP_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def create_placeholder_image(filepath, text, color="1a1a2e"):
    """Creates a high-contrast placeholder image if the user hasn't generated the real image yet."""
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "lavfi",
        "-i", f"color=c=0x{color}:s={WIDTH}x{HEIGHT}:d=1",
        "-vf", f"drawtext=text='{text}':fontsize=56:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=black@0.6:boxborderw=20",
        "-vframes", "1",
        str(filepath)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def get_motion_filter(motion_type, duration):
    total_frames = duration * FPS
    if motion_type == "zoom_in":
        # Slow cinematic zoom from 1.0x to 1.35x
        return f"zoompan=z='min(zoom+0.0012,1.35)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion_type == "zoom_out":
        # Cinematic pull-back from 1.35x to 1.0x
        return f"zoompan=z='if(lte(zoom,1.0),1.35,max(1.001,zoom-0.0012))':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion_type == "pan_right":
        # Cinematic horizontal pan
        return f"zoompan=z=1.28:d={total_frames}:x='if(lte(on,-1),(iw-iw/zoom)/2,x+1.2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion_type == "pan_down":
        # Vertical tilt downward
        return f"zoompan=z=1.28:d={total_frames}:x='iw/2-(iw/zoom/2)':y='if(lte(on,-1),0,y+1.2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    return f"zoompan=z=1.0:d={total_frames}:s={WIDTH}x{HEIGHT}:fps={FPS}"

def render_video():
    ensure_directories()
    rendered_clips = []
    
    total_duration = sum(s["duration"] for s in SCENES)
    print(f"\n🚀 [1/3] Using FFmpeg: {FFMPEG_BIN}")
    print(f"       Preparing 7 scenes (Target Duration: {total_duration}s)...")
    
    colors = ["1a1a2e", "251f47", "1b263b", "102a43", "2c1930", "1c2826", "231b1b"]
    for i, scene in enumerate(SCENES):
        img_path = IMAGES_DIR / scene["file"]
        if not img_path.exists():
            print(f"   ℹ️  {scene['file']} not found, generating temporary placeholder...")
            display_title = scene["title"].replace("'", "")
            create_placeholder_image(img_path, f"{scene['id'].upper()}\\n\\n{display_title}", colors[i % len(colors)])

    print("\n🎬 [2/3] Rendering Ken Burns camera motion per scene...")
    for i, scene in enumerate(SCENES):
        img_path = IMAGES_DIR / scene["file"]
        clip_output = TEMP_DIR / f"clip_{i:02d}.mp4"
        motion_filter = get_motion_filter(scene["motion"], scene["duration"])
        
        # Apply motion filter + crossfade out in the final 0.5s of each clip
        filter_chain = (
            f"{motion_filter},"
            f"fade=t=out:st={scene['duration']-0.5}:d=0.5"
        )

        cmd = [
            FFMPEG_BIN, "-y",
            "-loop", "1",
            "-i", str(img_path),
            "-vf", filter_chain,
            "-t", str(scene["duration"]),
            "-c:v", "libx264",
            "-preset", "fast",
            "-pix_fmt", "yuv420p",
            str(clip_output)
        ]
        print(f"   🎥 Rendering Scene {i+1}/{len(SCENES)}: {scene['file']} [{scene['motion']}] ({scene['duration']}s)...")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        rendered_clips.append(clip_output)

    print("\n🎞️ [3/3] Concatenating scenes into final vertical video...")
    concat_file = TEMP_DIR / "concat_list.txt"
    with open(concat_file, "w") as f:
        for clip in rendered_clips:
            f.write(f"file '{clip.as_posix()}'\n")

    final_output = OUTPUT_DIR / "what_if_internet_blackout_58s.mp4"
    audio_path = AUDIO_DIR / "voiceover.mp3"
    
    cmd_concat = [
        FFMPEG_BIN, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
    ]

    if audio_path.exists():
        print(f"   🎙️ Merging voiceover.mp3 ({audio_path})...")
        cmd_concat.extend(["-i", str(audio_path), "-c:a", "aac", "-shortest"])
    else:
        print("   ℹ️ No voiceover.mp3 found in assets/audio/ (video rendered mute).")

    cmd_concat.extend([
        "-c:v", "copy",
        str(final_output)
    ])

    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"\n✨ SUCCESS! 58-second 9:16 'What If' motion video created:")
    print(f"   📍 Output: {final_output}\n")

if __name__ == "__main__":
    try:
        render_video()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error executing FFmpeg: {e}", file=sys.stderr)
        sys.exit(1)
