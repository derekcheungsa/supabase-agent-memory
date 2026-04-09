#!/usr/bin/env python3
"""
Local test script for the supabase-memory skill.
Loads credentials from .env file in the skill root directory.

Usage:
    python3 test.py
"""

import sys
import os
from pathlib import Path

# Load .env from skill root (one level up from scripts/)
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ[key.strip()] = value.strip()  # force override system env

# Import skill functions
sys.path.insert(0, str(Path(__file__).parent))
from memory import save_memory, recall_memory

print("=== Supabase Memory Skill - Local Test ===\n")

# 1. Save some test memories
print("Saving test memories...")
save_memory("User runs an AI automation YouTube channel focused on agents", "fact")
save_memory("User prefers short videos under 15 minutes", "preference")
save_memory("User has a 5-video Supabase sponsorship deal", "fact")
save_memory("Competitor channels rarely cover Python-based AI agents", "research")

print()

# 2. Recall by meaning — not just keyword match
print("Recalling: 'what does the user create for work?'")
recall_memory("what does the user create for work?")

print()

print("Recalling: 'how long should videos be?'")
recall_memory("how long should videos be?")

print()

print("Recalling: 'what sponsorships does the user have?'")
recall_memory("what sponsorships does the user have?")

print()
print("=== Test complete. Check your Supabase Table Editor to see the rows. ===")
