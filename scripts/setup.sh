#!/bin/bash
# Supabase Memory Skill — dependency installer
# Installs Python packages to /data/pylibs on the Railway persistent volume.
# Run once after installing this skill.

set -e

PYLIBS="/data/pylibs"

echo "Installing Supabase memory skill dependencies to $PYLIBS..."

mkdir -p "$PYLIBS"
pip3 install supabase openai --target="$PYLIBS" --quiet

echo "Done. Dependencies installed to $PYLIBS"
echo "Test with: python3 /data/.openclaw/skills/supabase-memory/scripts/memory.py"
