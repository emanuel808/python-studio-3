
import asyncio
import io
import sys
import os
import uuid
from contextlib import redirect_stdout, redirect_stderr

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
    return {"status": "online", "name": "Python Studio 3.0"}

@app.post("/run")
async def run_script(request: ScriptRequest):
    if len(request.code) > 100000:
        raise HTTPException(413, "Script too large")

    output = io.StringIO()
    error = None

    def execute():
        namespace = {"__name__": "__main__"}
        with redirect_stdout(output), redirect_stderr(output):
            exec(compile(request.code, "script.py", "exec"), namespace)

    try:
        await asyncio.wait_for(
            asyncio.to_thread(execute),
            timeout=20
        )
    except asyncio.TimeoutError:
        error = "Execution time limit exceeded"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"

    return {
        "output": output.getvalue(),
        "error": error
    }
