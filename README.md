# Supabase Agent Memory

Persist agent memories to Supabase Postgres with pgvector semantic search. Memories survive restarts, redeployments, and are accessible from any device.

## Features

- **Semantic Search** — Retrieve memories using natural language queries via pgvector cosine similarity
- **Categories** — Organize memories as `fact`, `preference`, `task_result`, or `research`
- **Permanent Storage** — Survives agent restarts and redeployments
- **Cross-Device** — Accessible from any device connected to your Supabase project

## Prerequisites

- Supabase project with pgvector extension enabled
- Python 3.10+
- OpenAI API key (for generating embeddings)

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/derekcheungsa/supabase-agent-memory.git
cd supabase-agent-memory
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Fill in your values:
# SUPABASE_URL=your_supabase_project_url
# SUPABASE_KEY=your_supabase_anon_or_service_key
# OPENAI_API_KEY=your_openai_api_key
```

### 3. Run the Supabase setup script

Open your Supabase SQL Editor and run:

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

## Usage

### Save a Memory

```bash
python3 scripts/memory.py save "<content>" "<category>"
```

**Categories:** `fact` | `preference` | `task_result` | `research`

**Examples:**
```bash
python3 scripts/memory.py save "User wants competitor reports every Monday at 9am" "preference"
python3 scripts/memory.py save "Competitor dropped pricing by 20% in March" "research"
python3 scripts/memory.py save "User prefers concise responses under 3 sentences" "preference"
```

### Recall Memories

```bash
python3 scripts/memory.py recall "<query>"
```

**Examples:**
```bash
python3 scripts/memory.py recall "what are the user's reporting preferences?"
python3 scripts/memory.py recall "what do I know about competitor pricing?"
```

## When to Use

| Situation | Command |
|-----------|---------|
| User shares a preference | `save` with category `preference` |
| Research task completed | `save` with category `research` |
| Important task result | `save` with category `task_result` |
| User states a fact about themselves | `save` with category `fact` |
| Before a complex multi-step task | `recall` to load relevant context |
| User asks what you remember | `recall` with their topic |

## Project Structure

```
supabase-agent-memory/
├── SKILL.md           # Skill definition for Claude Code
├── README.md          # This file
├── .env.example       # Environment variable template
├── .gitignore
└── scripts/
    ├── memory.py      # Core save/recall logic
    ├── setup.sh       # Quick setup helper
    └── test.py        # Basic tests
```
