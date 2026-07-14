"""Core memory operations: remember, recall, list, delete, forget."""
from .config import DEFAULT_TOP_K, DEFAULT_THRESHOLD
from .db import get_conn, Vector
from .embed import embed
from .summarize import summarize

_COLS = "id,user_id,session_id,content,summary,mem_type,created_at"


def _row_to_dict(row):
    return {k: (str(row[k]) if k == "created_at" else row[k]) for k in row.keys()}


def remember(user_id, content, session_id=None, mem_type="fact"):
    summary = summarize(content)
    vec = Vector(embed(content))
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO memories (user_id, session_id, content, summary, mem_type, embedding)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, created_at
        """,
        (user_id, session_id, content, summary, mem_type, vec),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {"id": row["id"], "created_at": str(row["created_at"])}


def recall(user_id, query, session_id=None, top_k=None, threshold=None):
    top_k = top_k or DEFAULT_TOP_K
    threshold = threshold if threshold is not None else DEFAULT_THRESHOLD
    qvec = Vector(embed(query))
    conn = get_conn()
    cur = conn.cursor()
    if session_id:
        cur.execute(
            f"""
            SELECT {_COLS}, 1 - (embedding <=> %s) AS score
            FROM memories
            WHERE user_id = %s AND session_id = %s
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            (qvec, user_id, session_id, qvec, top_k),
        )
    else:
        cur.execute(
            f"""
            SELECT {_COLS}, 1 - (embedding <=> %s) AS score
            FROM memories
            WHERE user_id = %s
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            (qvec, user_id, qvec, top_k),
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    out = []
    for r in rows:
        if r["score"] < threshold:
            continue
        d = _row_to_dict(r)
        out.append(d)
    return out


def list_memories(user_id, session_id=None, limit=50):
    conn = get_conn()
    cur = conn.cursor()
    if session_id:
        cur.execute(
            f"SELECT {_COLS} FROM memories "
            "WHERE user_id = %s AND session_id = %s "
            "ORDER BY created_at DESC LIMIT %s",
            (user_id, session_id, limit),
        )
    else:
        cur.execute(
            f"SELECT {_COLS} FROM memories WHERE user_id = %s "
            "ORDER BY created_at DESC LIMIT %s",
            (user_id, limit),
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def delete_memory(memory_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM memories WHERE id = %s RETURNING id", (memory_id,))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return row is not None


def forget_user(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM memories WHERE user_id = %s", (user_id,))
    n = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return n
