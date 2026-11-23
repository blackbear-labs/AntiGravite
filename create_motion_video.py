import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
AUDIO_DIR = ASSETS_DIR / "audio"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / ".temp"

# Format Output: 9:16 Vertical Video (Shorts / Reels / TikTok)
WIDTH = 1080
HEIGHT = 1920
FPS = 30

SCENES = [
    {
        "id": "scene1",
        "file": "scene1.png",
        "duration": 5,
        "motion": "zoom_in",
        "caption": "HARI KE-0: SIGNAL LOST"
    },
    {
        "id": "scene2",
        "file": "scene2.png",
        "duration": 7,
        "motion": "pan_right",
        "caption": "HARI KE-3: PERBANKAN LUMPUH"
    },
    {
        "id": "scene3",
        "file": "scene3.png",
        "duration": 8,
        "motion": "zoom_out",
        "caption": "MINGGU KE-2: RANTAI PASOKAN RUNTUH"
    },
    {
        "id": "scene4",
        "file": "scene4.png",
        "duration": 8,
        "motion": "pan_down",
        "caption": "MINGGU KE-3: BLACKOUT TOTAL"
    },
    {
        "id": "scene5",
        "file": "scene5.png",
        "duration": 7,
        "motion": "zoom_in",
        "caption": "SANGGUPKAH KAMU BERTAHAN?"
    }
]

def ensure_directories():
    for d in [IMAGES_DIR, AUDIO_DIR, OUTPUT_DIR, TEMP_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def create_placeholder_image(filepath, text, color="333333"):
    """Membuat placeholder image menggunakan FFmpeg jika user belum menaruh gambar asli"""
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=0x{color}:s={WIDTH}x{HEIGHT}:d=1",
        "-vf", f"drawtext=text='{text}':fontsize=64:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
        "-vframes", "1",
        str(filepath)
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

def get_motion_filter(motion_type, duration):
    total_frames = duration * FPS
    if motion_type == "zoom_in":
        return f"zoompan=z='min(zoom+0.0015,1.35)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion_type == "zoom_out":
        return f"zoompan=z='if(lte(zoom,1.0),1.35,max(1.001,zoom-0.0015))':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion_type == "pan_right":
        return f"zoompan=z=1.25:d={total_frames}:x='if(lte(on,-1),(iw-iw/zoom)/2,x+1.5)':y='ih/2-(ih/zoom/2)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    elif motion_type == "pan_down":
        return f"zoompan=z=1.25:d={total_frames}:x='iw/2-(iw/zoom/2)':y='if(lte(on,-1),0,y+1.5)':s={WIDTH}x{HEIGHT}:fps={FPS}"
    return f"zoompan=z=1.0:d={total_frames}:s={WIDTH}x{HEIGHT}:fps={FPS}"

def render_video():
    ensure_directories()
    rendered_clips = []
    
    print("\n🚀 [1/3] Menyiapkan asset gambar...")
    colors = ["1a1a2e", "222831", "162447", "0f3460", "1f4068"]
    for i, scene in enumerate(SCENES):
        img_path = IMAGES_DIR / scene["file"]
        if not img_path.exists():
            print(f"   ℹ️  {scene['file']} belum ada, membuat placeholder sementara...")
            create_placeholder_image(img_path, f"{scene['id']}\\n({scene['motion']})", colors[i % len(colors)])

    print("\n🎬 [2/3] Memproses efek kamera motion (Ken Burns) per scene...")
    for i, scene in enumerate(SCENES):
        img_path = IMAGES_DIR / scene["file"]
        clip_output = TEMP_DIR / f"clip_{i:02d}.mp4"
        motion_filter = get_motion_filter(scene["motion"], scene["duration"])
        
        # Tambahkan caption & efek fade out di akhir scene
        filter_chain = (
            f"{motion_filter},"
            f"fade=t=out:st={scene['duration']-0.5}:d=0.5"
        )

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(img_path),
            "-vf", filter_chain,
            "-t", str(scene["duration"]),
            "-c:v", "libx264",
            "-preset", "fast",
            "-pix_fmt", "yuv420p",
            str(clip_output)
        ]
        print(f"   🎥 Merender Scene {i+1}/{len(SCENES)}: {scene['file']} [{scene['motion']}] ({scene['duration']}s)...")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        rendered_clips.append(clip_output)

    print("\n🎞️ [3/3] Menggabungkan semua klip menjadi video final...")
    concat_file = TEMP_DIR / "concat_list.txt"
    with open(concat_file, "w") as f:
        for clip in rendered_clips:
            f.write(f"file '{clip.as_posix()}'\n")

    final_output = OUTPUT_DIR / "final_what_if_video.mp4"
    audio_path = AUDIO_DIR / "voiceover.mp3"
    
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
    ]

    if audio_path.exists():
        print("   🎙️ Menggabungkan audio voiceover.mp3...")
        cmd_concat.extend(["-i", str(audio_path), "-c:a", "aac", "-shortest"])
    else:
        print("   ℹ️ Audio voiceover.mp3 belum disediakan (video akan dibuat tanpa audio).")

    cmd_concat.extend([
        "-c:v", "copy",
        str(final_output)
    ])

    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"\n✨ SUKSES! Video motion 'What If' berhasil dibuat:")
    print(f"   📍 Lokasi: {final_output}\n")

if __name__ == "__main__":
    try:
        render_video()
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error saat menjalankan FFmpeg: {e}", file=sys.stderr)
        sys.exit(1)
