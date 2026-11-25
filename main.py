
import io
import sys
import os
import uuid
import ast
import subprocess
import tempfile
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Python Studio 3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScriptRequest(BaseModel):
    code: str

@app.get("/")
def home():
    return {
        "status": "online",
        "name": "Python Studio 3.0"
    }

@app.post("/run")
async def run_script(request: ScriptRequest):
    if not isinstance(request.code, str):
        raise HTTPException(400, "Invalid script")

    if len(request.code.encode("utf-8")) > 100000:
        raise HTTPException(413, "Script too large")

    try:
        ast.parse(request.code)
    except SyntaxError as exc:
        raise HTTPException(400, f"Syntax error: {exc}")

    return {
        "output": "",
        "error": "Python execution is not enabled yet. A secure isolated runtime must be configured first."
    }
