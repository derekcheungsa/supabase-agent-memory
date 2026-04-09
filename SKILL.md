---
name: supabase-memory
description: Save and recall agent memories permanently using Supabase with semantic
  search. Use this skill when you learn something important about the user — preferences,
  facts, research results, or task outcomes. Use save_memory to persist information,
  use recall_memory before complex tasks to retrieve relevant context from long-term memory.
---

# Supabase Memory

Persist agent memories to Supabase Postgres with pgvector semantic search. Memories survive restarts, redeployments, and are accessible from any device.

## Setup (run once after installing)

```bash
bash /data/.openclaw/skills/supabase-memory/scripts/setup.sh
```

## Save a Memory

```bash
python3 /data/.openclaw/skills/supabase-memory/scripts/memory.py save "<content>" "<category>"
```

Categories: `fact` | `preference` | `task_result` | `research`

Examples:
```bash
python3 /data/.openclaw/skills/supabase-memory/scripts/memory.py save "User wants competitor reports every Monday at 9am" "preference"
python3 /data/.openclaw/skills/supabase-memory/scripts/memory.py save "Competitor dropped pricing by 20% in March" "research"
```

## Recall Memories

```bash
python3 /data/.openclaw/skills/supabase-memory/scripts/memory.py recall "<query>"
```

Examples:
```bash
python3 /data/.openclaw/skills/supabase-memory/scripts/memory.py recall "what are the user's reporting preferences?"
python3 /data/.openclaw/skills/supabase-memory/scripts/memory.py recall "what do I know about competitor pricing?"
```

## When to Use

- User shares a preference → `save_memory`, category `preference`
- Research task completed → `save_memory`, category `research`
- Important task result → `save_memory`, category `task_result`
- User states a fact about themselves or their business → `save_memory`, category `fact`
- Before any complex or multi-step task → run `recall_memory` first to load relevant context
- User asks what you remember → `recall_memory` with their topic

## Required Environment Variables

- `SUPABASE_URL` — your Supabase project URL
- `SUPABASE_KEY` — your Supabase anon/service key
- `OPENAI_API_KEY` — used for generating text embeddings

## Supabase Setup

Run these SQL statements once in your Supabase SQL Editor before using this skill:

```sql
create extension if not exists vector;

create table agent_memories (
  id         uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  content    text not null,
  embedding  vector(1536),
  category   text,
  importance int default 5
);

create index on agent_memories
using hnsw (embedding vector_cosine_ops);

create or replace function match_memories(
  query_embedding vector(1536),
  match_count     int default 5
)
returns table (id uuid, content text, category text, similarity float)
language sql as $$
  select id, content, category,
    1 - (embedding <=> query_embedding) as similarity
  from agent_memories
  order by embedding <=> query_embedding
  limit match_count;
$$;
```
