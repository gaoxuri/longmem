"""FastAPI application exposing the memory HTTP API."""
import uvicorn

from fastapi import FastAPI

from .config import SERVICE_HOST, SERVICE_PORT
from .models import RememberReq, RecallReq, BatchRememberReq, UpdateReq
from .store import remember, recall, list_memories, update_memory, delete_memory, forget_user, purge_expired, batch_remember

app = FastAPI(title="LongMem — AI Long-term Memory Middleware", version="0.2.1")


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/remember")
def api_remember(req: RememberReq):
    res = remember(req.user_id, req.content, req.session_id, req.mem_type, req.ttl_seconds)
    return {"ok": True, **res}


@app.post("/remember/batch")
def api_remember_batch(req: BatchRememberReq):
    items = [
        (i.user_id, i.content, i.session_id, i.mem_type, i.ttl_seconds)
        for i in req.items
    ]
    res = batch_remember(items)
    return {"ok": True, "count": len(res), "ids": [r["id"] for r in res]}


@app.post("/recall")
def api_recall(req: RecallReq):
    results = recall(req.user_id, req.query, req.session_id, req.top_k, req.threshold)
    return {"ok": True, "count": len(results), "results": results}


@app.get("/memories")
def api_list(user_id: str, session_id: str = None, limit: int = 50):
    return {"ok": True, "results": list_memories(user_id, session_id, limit)}


@app.put("/memory/{memory_id}")
def api_update(memory_id: int, req: UpdateReq):
    return {"ok": update_memory(memory_id, req.content, req.mem_type, req.ttl_seconds)}


@app.delete("/memory/{memory_id}")
def api_delete(memory_id: int):
    return {"ok": delete_memory(memory_id)}


@app.post("/forget")
def api_forget(req: dict):
    user_id = req.get("user_id")
    if not user_id:
        return {"ok": False, "error": "user_id required"}
    return {"ok": True, "deleted": forget_user(user_id)}


@app.post("/forget/expired")
def api_purge_expired():
    return {"ok": True, "deleted": purge_expired()}


def main():
    uvicorn.run(app, host=SERVICE_HOST, port=SERVICE_PORT)


if __name__ == "__main__":
    main()
