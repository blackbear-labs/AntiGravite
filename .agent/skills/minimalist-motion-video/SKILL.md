---
name: minimalist-motion-video
description: >-
  Generates viral 2D minimalist motion graphics videos (9:16 vertical, Anthem / Linear / After Effects style)
  for any topic ("What If", tech explainers, science, finance). Automatically creates 2D vector UI cards,
  synthesizes neural voiceovers (EN/ID), designs kinetic ASS subtitles with neon keyword highlights,
  layers suspense electronic sub-bass audio, and renders smooth MP4 motion videos via FFmpeg.
---

# Minimalist 2D Motion Graphics Video Generator Skill

This skill teaches the agent how to generate **100% 2D Minimalist Motion Graphics Videos** in 9:16 smartphone vertical format (TikTok, YouTube Shorts, Reels), inspired by the **Anthem, Linear, and SaaS Motion Design** aesthetic.

---

## 🎨 Visual Aesthetic & Design Rules
1. **Background:** Clean matte dark (`#0B0D11`) with subtle dot-matrix tech grid.
2. **Central Glass Cards:** Rounded containers with 2px neon borders and HUD tech corner brackets (`[ + ]`).
3. **Pills & Status Badges:** Glowing pill indicators (e.g. `● CRITICAL INCIDENT // 00:00:00`).
4. **Typography:** Crisp, bold Sans-Serif kinetic titles with telemetry dividers (`---`).
5. **Data & Metrics:** Large high-contrast stat numbers (e.g. `0.00 TB/s`, `-98.4%`, `-$2.1 TRILLION`) paired with accent progress bars.
6. **Color Themes per Scene:**
   - `red`: Crisis, danger, shutdown, errors (`#FF3344`)
   - `yellow`: Warnings, financial freeze, caution (`#FFD700`)
   - `cyan`: Telemetry, logistics, tech data, networks (`#00E5FF`)
   - `purple`: Macroeconomy, global metrics, mystery (`#BD00FF`)
   - `green`: Restoration, online status, positive CTA (`#00FF66`)

---

## 🚀 How to Generate a Video for Any New Topic

When the user asks for a video on a new topic (e.g., *"What if oxygen disappeared for 5 seconds?"* or *"What if gravity dropped by 50%?"*):

### Step 1: Breakdown the Topic into 6 to 12 Kinetic Scenes
For each scene, define:
- `theme`: `"red"`, `"cyan"`, `"yellow"`, `"purple"`, or `"green"`
- `badge`: Status tag (e.g., `DAY 01 // ATMOSPHERE`)
- `heading`: 2-line punchy title in uppercase (e.g., `OXYGEN LEVELS\\nZERO PERCENT`)
- `stat_label`: Metric name (e.g., `GLOBAL AIR PRESSURE`)
- `stat_val`: Metric value (e.g., `-100.0 %` or `0.00 PSI`)
- `duration`: 4.0 to 5.0 seconds
- `motion`: `"snap_in"`, `"pull_out"`, `"subtle_drift"`, or `"pulse"`
- `vo`: 1 concise sentence of voiceover

### Step 2: Write Synchronized Kinetic Subtitles (`.ass`)
Write short subtitle events (2 lines max) with color-coded tags:
- `{RED}` for danger/shutdown
- `{YELLOW}` for warnings/amounts
- `{CYAN}` for data/protocols
- `{GREEN}` for recovery/questions
- `{WHITE}` for base narration

### Step 3: Run the Motion Engine Script
Save the configuration dictionary and run `render_minimalist_motion.py`:

```python
from render_minimalist_motion import generate_minimalist_video

config = {
    "lang": "en", # or "id" for Indonesian voiceover
    "scenes": [
        # ... list of scene dictionaries
    ],
    "subtitles": [
        # (start_time, end_time, "Line 1", "Line 2 with {COLOR}TAGS{WHITE}")
    ]
}

generate_minimalist_video(config, "output/my_new_topic_video.mp4")
```

Or run the CLI directly:
```bash
python render_minimalist_motion.py --out output/my_topic.mp4
```

---

## 🎧 Audio Engineering Architecture
The engine automatically synthesizes and mixes 2 distinct layers:
1. **Neural Voiceover:** Fast, authoritative voice (+16% rate) via `edge-tts` (`en-US-ChristopherNeural` for English, `id-ID-ArdiNeural` for Indonesian).
2. **Suspense Electronic Sub-Bass Drone:** Synthesized at 55Hz (sub-bass) + 110Hz (harmonic) with 120BPM rhythmic pulse mixed at -18dB under the narration.

---

## 🛠️ File References
- Engine Script: `render_minimalist_motion.py`
- Output Folder: `output/`
