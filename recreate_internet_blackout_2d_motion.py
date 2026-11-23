#!/usr/bin/env python3
"""
Recreating 'What If the Global Internet Completely Shut Down for 1 Month?'
in 100% 2D Minimalist Motion Graphics (Anthem / After Effects / Linear Style).
Total Runtime: ~55 Seconds | 9:16 Vertical Smartphone Format (1080x1920)
"""

import sys
from pathlib import Path
from render_minimalist_motion import generate_minimalist_video

CONFIG = {
    "lang": "en",
    "scenes": [
        {
            "duration": 4.5,
            "motion": "snap_in",
            "theme": "red",
            "badge": "DAY 00 // SIGNAL TERMINATION",
            "heading": "GLOBAL NETWORK\\nDISCONNECT",
            "stat_label": "INTERNET TRAFFIC THROUGHPUT",
            "stat_val": "0.00 TB/s",
            "vo": "What if at this exact second, every single byte of internet on Earth vanished for thirty full days?"
        },
        {
            "duration": 4.5,
            "motion": "pull_out",
            "theme": "cyan",
            "badge": "DAY 00 // DIGITAL SILENCE",
            "heading": "4.8 BILLION DEVICES\\nOFFLINE",
            "stat_label": "COMMUNICATION PROTOCOL STATUS",
            "stat_val": "ZERO PACKETS",
            "vo": "No messages. No cloud services. Total instantaneous digital silence across the planet."
        },
        {
            "duration": 4.5,
            "motion": "snap_in",
            "theme": "yellow",
            "badge": "DAY 01 // FINANCIAL GRIDLOCK",
            "heading": "BANKING PROTOCOLS\\nFROZEN",
            "stat_label": "DIGITAL CARD TRANSACTIONS",
            "stat_val": "100.0% FAILED",
            "vo": "Within twenty-four hours, the global financial system freezes. Credit cards are useless plastic."
        },
        {
            "duration": 4.5,
            "motion": "subtle_drift",
            "theme": "red",
            "badge": "DAY 03 // LIQUIDITY COLLAPSE",
            "heading": "ATMs FLASH RED\\nSYSTEM HALTED",
            "stat_label": "GLOBAL CASH RESERVES ACCESSIBLE",
            "stat_val": "< 5.0 %",
            "vo": "ATMs flash system errors. Digital bank balances literally cease to be accessible."
        },
        {
            "duration": 4.5,
            "motion": "snap_in",
            "theme": "cyan",
            "badge": "DAY 07 // SUPPLY CHAIN",
            "heading": "GLOBAL PORTS & GPS\\nDEADLOCK",
            "stat_label": "AUTOMATED CONTAINER CARGO FLOW",
            "stat_val": "-98.4 %",
            "vo": "By day seven, global supply chains stall without GPS routing and automated container logistics."
        },
        {
            "duration": 4.5,
            "motion": "pull_out",
            "theme": "red",
            "badge": "DAY 10 // FOOD SECURITY",
            "heading": "SUPERMARKETS\\nRANSACKED",
            "stat_label": "RETAIL INVENTORY DEPLETION",
            "stat_val": "48 HOURS TO 0%",
            "vo": "Supermarket shelves empty in forty-eight hours as nationwide panic buying erupts."
        },
        {
            "duration": 4.5,
            "motion": "snap_in",
            "theme": "red",
            "badge": "DAY 14 // ENERGY INFRASTRUCTURE",
            "heading": "POWER SUBSTATIONS\\nBLACKOUT",
            "stat_label": "METROPOLITAN GRIDS DOWN",
            "stat_val": "140+ METROPOLISES",
            "vo": "Week two: Supervisory SCADA networks fail, plunging major global cities into total blackout."
        },
        {
            "duration": 4.5,
            "motion": "subtle_drift",
            "theme": "yellow",
            "badge": "DAY 18 // CIVILIAN DISPATCH",
            "heading": "EMERGENCY PROTOCOLS\\nCOMPROMISED",
            "stat_label": "DISPATCH COMMUNICATION RELIANCE",
            "stat_val": "ANALOGUE ONLY",
            "vo": "Emergency services struggle to respond without digital dispatch systems and cellular networks."
        },
        {
            "duration": 4.5,
            "motion": "snap_in",
            "theme": "purple",
            "badge": "DAY 21 // SOCIETAL REGRESSION",
            "heading": "CIVILIZATION REVERTS\\nFIFTY YEARS",
            "stat_label": "PRIMARY EXCHANGE CURRENCY",
            "stat_val": "CASH & BARTER",
            "vo": "By day twenty-one, society regresses fifty years. Physical cash and fuel become the only currency."
        },
        {
            "duration": 4.5,
            "motion": "pull_out",
            "theme": "purple",
            "badge": "DAY 28 // MACROECONOMIC VOID",
            "heading": "GLOBAL WEALTH\\nEVAPORATION",
            "stat_label": "ESTIMATED GDP WIPEOUT",
            "stat_val": "-$2.1 TRILLION",
            "vo": "By day thirty, over two trillion dollars in global wealth is vaporized, and millions of digital careers erased."
        },
        {
            "duration": 5.0,
            "motion": "snap_in",
            "theme": "green",
            "badge": "DAY 30 // THE RESTORATION",
            "heading": "SYSTEM REBOOT\\n100% ONLINE",
            "stat_label": "NETWORK TELEMETRY LATENCY",
            "stat_val": "18ms // RESTORED",
            "vo": "Then... with a single click, the signal abruptly bursts back online across the globe."
        },
        {
            "duration": 5.5,
            "motion": "pulse",
            "theme": "green",
            "badge": "FINAL AUDIT // QUESTION",
            "heading": "COULD YOU SURVIVE\\n30 DAYS?",
            "stat_label": "AUDIENCE POLL",
            "stat_val": "DROP ANSWER BELOW",
            "vo": "Civilization barely survived. But honestly, could you survive thirty days? Drop your answer below."
        }
    ],
    "subtitles": [
        (0.0, 4.5, "What if at this exact second,", "the entire internet vanishes for {RED}30 FULL DAYS?{WHITE}"),
        (4.5, 9.0, "No messages. No cloud services.", "Total {CYAN}DIGITAL SILENCE{WHITE} across Earth."),
        (9.0, 13.5, "Within 24 hours,", "the global financial system {YELLOW}FREEZES.{WHITE}"),
        (13.5, 18.0, "ATMs flash red errors.", "Digital bank balances are {RED}INACCESSIBLE.{WHITE}"),
        (18.0, 22.5, "By day seven,", "automated shipping ports drop by {CYAN}98.4 PERCENT.{WHITE}"),
        (22.5, 27.0, "Supermarket shelves empty", "in {RED}48 HOURS{WHITE} as panic buying erupts."),
        (27.0, 31.5, "Week two: Power grids collapse,", "plunging {RED}140+ METROPOLISES{WHITE} into darkness."),
        (31.5, 36.0, "Emergency services struggle,", "relying solely on {YELLOW}ANALOGUE RADIO.{WHITE}"),
        (36.0, 40.5, "By day twenty-one,", "society regresses {PURPLE}50 YEARS BACK.{WHITE}"),
        (40.5, 45.0, "By day thirty,", "{PURPLE}$2.1 TRILLION{WHITE} in global wealth is vaporized."),
        (45.0, 50.0, "Then... with a single click,", "the signal bursts back {GREEN}100% ONLINE.{WHITE}"),
        (50.0, 55.5, "Civilization barely survived.", "{GREEN}COULD YOU SURVIVE?{WHITE} Drop your answer below.")
    ]
}

if __name__ == "__main__":
    output_path = Path("output/what_if_internet_down_minimalist_2d.mp4")
    generate_minimalist_video(CONFIG, output_path)
