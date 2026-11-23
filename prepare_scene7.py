import subprocess
from pathlib import Path
import imageio_ffmpeg

target_dir = Path(r"C:\Users\USER\.gemini\antigravity\scratch\AntiGravite\assets\images")
s1 = target_dir / "scene1.png"
s7 = target_dir / "scene7.png"

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# Transform scene1 with intense neon green restoration look + text
filter_str = (
    "hue=h=110:s=2,"
    "eq=brightness=0.05:contrast=1.2,"
    "drawtext=text='INTERNET RESTORED':fontsize=68:fontcolor=0x00FF88:x=(w-text_w)/2:y=h*0.35:box=1:boxcolor=black@0.7:boxborderw=15,"
    "drawtext=text='SYSTEM ONLINE':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=h*0.43:box=1:boxcolor=black@0.6:boxborderw=10"
)

cmd = [
    ffmpeg_exe, "-y",
    "-i", str(s1),
    "-vf", filter_str,
    str(s7)
]
subprocess.run(cmd, check=True)
print("Successfully generated scene7.png!")
