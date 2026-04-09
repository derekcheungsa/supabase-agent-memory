#!/usr/bin/env python3
"""
Supabase Memory Skill for OpenClaw
Saves and recalls agent memories using Supabase pgvector semantic search.

Usage:
    python3 memory.py save "<content>" [category]
    python3 memory.py recall "<query>" [limit]

Categories: fact | preference | task_result | research
"""

import sys
import os

# Packages installed to Railway volume by setup.sh
sys.path.insert(0, '/data/pylibs')

from supabase import create_client
from openai import OpenAI

# Initialise clients from environment variables
supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"]
)
openai_client = OpenAI()


def embed(text: str) -> list[float]:
    """Generate a 1536-dim embedding vector for the given text."""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def save_memory(content: str, category: str = "fact") -> None:
    """Embed content and store it in Supabase agent_memories table."""
    supabase.table("agent_memories").insert({
        "content": content,
        "embedding": embed(content),
        "category": category
    }).execute()
    print(f"Memory saved [{category}]: {content[:80]}")


def recall_memory(query: str, limit: int = 5) -> None:
    """Search agent_memories semantically and print the top matches."""
    result = supabase.rpc("match_memories", {
        "query_embedding": embed(query),
        "match_count": limit
    }).execute()

    if result.data:
        for r in result.data:
            similarity = round(r.get("similarity", 0), 3)
            print(f"[{r['category']}] (similarity: {similarity}) {r['content']}")
    else:
        print("No relevant memories found.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "save":
        content = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else "fact"
        save_memory(content, category)

    elif cmd == "recall":
        query = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        recall_memory(query, limit)

    else:
        print(f"Unknown command: {cmd}")
        print("Usage: python3 memory.py save|recall ...")
        sys.exit(1)
