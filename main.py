
import os
import json
import asyncio
import urllib.request
import urllib.error

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
    input: str = ""

@app.get("/")
def home():
    return {
        "status": "online",
        "name": "Python Studio 3.0"
    }

def execute_python(code, user_input):
    api_key = os.getenv("ONLINECOMPILER_API_KEY")

    if not api_key:
        raise Exception("API key is missing on Render.")

    payload = json.dumps({
        "compiler": "python-3.14",
        "code": code,
        "input": user_input,
        "time_limit": 30
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.onlinecompiler.io/api/run-code-sync/",
        data=payload,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=40) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise Exception(f"OnlineCompiler error {error.code}: {details}")

@app.post("/run")
async def run_script(request: ScriptRequest):
    if len(request.code.encode("utf-8")) > 100000:
        raise HTTPException(413, "Script too large")

    try:
        result = await asyncio.to_thread(
            execute_python,
            request.code,
            request.input
        )

        return {
            "output": result.get("output", ""),
            "error": result.get("error", ""),
            "status": result.get("status", ""),
            "exit_code": result.get("exit_code")
        }

    except Exception as error:
        raise HTTPException(502, str(error))
