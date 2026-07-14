"""PostgreSQL + pgvector connection and schema management."""
import psycopg2
from psycopg2.extensions import AsIs, register_adapter
from psycopg2.extras import DictCursor

from .config import (
    PG_HOST,
    PG_PORT,
    PG_NAME,
    PG_USER,
    PG_PASSWORD,
    EMBED_DIM,
)


class Vector(list):
    """A list that psycopg2 serializes as a pgvector literal."""


def _adapt_vector(vec):
    inner = ",".join(str(float(x)) for x in vec)
    return AsIs("'[%s]'" % inner)


register_adapter(Vector, _adapt_vector)


def get_conn():
    """Return a new psycopg2 connection with DictCursor."""
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_NAME,
        user=PG_USER,
        password=PG_PASSWORD,
        cursor_factory=DictCursor,
    )


def init_db():
    """Create the vector extension and memories table if they do not exist."""
    conn = get_conn()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS memories (
            id          SERIAL PRIMARY KEY,
            user_id    TEXT NOT NULL,
            session_id TEXT,
            content    TEXT NOT NULL,
            summary    TEXT,
            mem_type   TEXT DEFAULT 'fact',
            embedding  vector({EMBED_DIM}),
            created_at TIMESTAMPTZ DEFAULT now()
        );
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_mem_user ON memories(user_id);")
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_mem_user_session "
        "ON memories(user_id, session_id);"
    )
    cur.execute(
        f"CREATE INDEX IF NOT EXISTS idx_mem_embed ON memories "
        f"USING ivfflat (embedding vector_cosine_ops) WITH (lists = 10);"
    )
    cur.close()
    conn.close()
