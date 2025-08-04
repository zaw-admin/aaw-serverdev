import asyncio
import os
import time
from typing import Dict

import psutil
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .local_model import analyze_code

app = FastAPI(title="AAW Server AI")
app.mount("/static", StaticFiles(directory="static"), name="static")

ALLOWED_KEYS = [
    key for key in os.getenv("ALLOWED_KEYS", "demo-key").split(",") if key
]

active_users: Dict[str, float] = {}
concurrency_limit = int(os.getenv("MAX_CONCURRENCY", "1"))
semaphore = asyncio.Semaphore(concurrency_limit)


class CodeRequest(BaseModel):
    key: str
    code: str


class ConcurrencyRequest(BaseModel):
    limit: int


@app.post("/analyze")
async def analyze(req: CodeRequest):
    if req.key not in ALLOWED_KEYS:
        raise HTTPException(status_code=401, detail="Invalid key")
    active_users[req.key] = time.time()
    async with semaphore:
        analysis = await asyncio.to_thread(analyze_code, req.code)
    return {"analysis": analysis}


@app.post("/concurrency")
async def set_concurrency(req: ConcurrencyRequest):
    global semaphore, concurrency_limit
    concurrency_limit = max(1, req.limit)
    semaphore = asyncio.Semaphore(concurrency_limit)
    return {"limit": concurrency_limit}


@app.get("/stats")
async def stats():
    process = psutil.Process()
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    return {
        "cpu": cpu,
        "memory": memory,
        "active_users": list(active_users.keys()),
        "concurrency_limit": concurrency_limit,
        "running_tasks": process.num_threads(),
    }


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/admin", response_class=HTMLResponse)
async def admin():
    with open("static/admin.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())
