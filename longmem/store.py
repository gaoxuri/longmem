"""Core memory operations: remember, recall, list, delete, forget."""
from .config import DEFAULT_TOP_K, DEFAULT_THRESHOLD
from .db import get_conn, Vector
from .embed import embed
from .summarize import summarize

_COLS = "id,user_id,session_id,content,summary,mem_type,ttl_seconds,created_at"

# Only return memories that have not expired (ttl_seconds since creation).
_NOT_EXPIRED = "(ttl_seconds IS NULL OR created_at + ttl_seconds * INTERVAL '1 second' > now())"


def _row_to_dict(row):
    return {k: (str(row[k]) if k == "created_at" else row[k]) for k in row.keys()}


def remember(user_id, content, session_id=None, mem_type="fact", ttl_seconds=None):
    summary = summarize(content)
    vec = Vector(embed(content))
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO memories (user_id, session_id, content, summary, mem_type, ttl_seconds, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id, created_at
        """,
        (user_id, session_id, content, summary, mem_type, ttl_seconds, vec),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return {"id": row["id"], "created_at": str(row["created_at"])}


def batch_remember(items):
    """items: list of (user_id, content, session_id, mem_type, ttl_seconds)."""
    return [
        remember(uid, content, sid, mtype, ttl)
        for (uid, content, sid, mtype, ttl) in items
    ]


def recall(user_id, query, session_id=None, top_k=None, threshold=None,
           type_filter=None, recency_bias=0.0):
    """Retrieve memories by similarity.

    type_filter  : only return memories of this mem_type
    recency_bias : 0..1, blend cosine score with a recency factor so that
                   fresher memories rank higher when scores are close.
                   final = (1 - bias) * cosine + bias * recency
    """
    top_k = top_k or DEFAULT_TOP_K
    threshold = threshold if threshold is not None else DEFAULT_THRESHOLD
    qvec = Vector(embed(query))
    conn = get_conn()
    cur = conn.cursor()
    sql_type = "AND mem_type = %s " if type_filter else ""
    params = [qvec, user_id, qvec, top_k]
    if type_filter:
        params.insert(2, type_filter)
    if session_id:
        cur.execute(
            f"""
            SELECT {_COLS}, 1 - (embedding <=> %s) AS score
            FROM memories
            WHERE user_id = %s AND session_id = %s {sql_type}AND {_NOT_EXPIRED}
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            params,
        )
    else:
        cur.execute(
            f"""
            SELECT {_COLS}, 1 - (embedding <=> %s) AS score
            FROM memories
            WHERE user_id = %s {sql_type}AND {_NOT_EXPIRED}
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            params,
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    out = []
    now = None
    for r in rows:
        if r["score"] < threshold:
            continue
        d = _row_to_dict(r)
        if recency_bias and recency_bias > 0:
            if now is None:
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
            age_days = max(0.0, (now - r["created_at"]).total_seconds() / 86400.0)
            recency = 1.0 / (1.0 + age_days)
            d["score"] = round((1 - recency_bias) * r["score"] + recency_bias * recency, 6)
        out.append(d)

    if recency_bias and recency_bias > 0:
        out.sort(key=lambda x: x["score"], reverse=True)
    return out


def list_memories(user_id, session_id=None, limit=50):
    conn = get_conn()
    cur = conn.cursor()
    if session_id:
        cur.execute(
            f"SELECT {_COLS} FROM memories "
            "WHERE user_id = %s AND session_id = %s AND {_NOT_EXPIRED} "
            "ORDER BY created_at DESC LIMIT %s".format(_NOT_EXPIRED=_NOT_EXPIRED),
            (user_id, session_id, limit),
        )
    else:
        cur.execute(
            f"SELECT {_COLS} FROM memories WHERE user_id = %s AND {_NOT_EXPIRED} "
            "ORDER BY created_at DESC LIMIT %s".format(_NOT_EXPIRED=_NOT_EXPIRED),
            (user_id, limit),
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def update_memory(memory_id, content=None, mem_type=None, ttl_seconds=None):
    """Patch a memory. Re-embedding happens only when content changes."""
    conn = get_conn()
    cur = conn.cursor()
    if content is not None:
        summary = summarize(content)
        vec = Vector(embed(content))
        cur.execute(
            """
            UPDATE memories
               SET content = %s, summary = %s, embedding = %s,
                   mem_type = COALESCE(%s, mem_type),
                   ttl_seconds = %s
             WHERE id = %s
            """,
            (content, summary, vec, mem_type, ttl_seconds, memory_id),
        )
    else:
        cur.execute(
            """
            UPDATE memories
               SET mem_type = COALESCE(%s, mem_type),
                   ttl_seconds = %s
             WHERE id = %s
            """,
            (mem_type, ttl_seconds, memory_id),
        )
    n = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return n > 0


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


def purge_expired():
    """Hard-delete memories whose TTL has elapsed. Returns number removed."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM memories WHERE NOT {_NOT_EXPIRED}")
    n = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    return n
