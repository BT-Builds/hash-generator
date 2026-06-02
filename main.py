import os
import hashlib
from datetime import datetime
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from mangum import Mangum
from collections import defaultdict
import time

app = FastAPI(
    title="Hash Generator API",
    description="Generate cryptographic hashes via HTTP API",
    version="1.0.0"
)

API_KEYS = set(filter(None, os.environ.get("API_KEYS", "free-demo-key").split(",")))
RATE_LIMIT = int(os.environ.get("RATE_LIMIT_PER_MIN", "60"))
_req_counts = defaultdict(list)

def auth(x_api_key: str = Header(default="free-demo-key")):
    if x_api_key not in API_KEYS:
        raise HTTPException(401, "Invalid API key")
    now = time.time()
    window = [t for t in _req_counts[x_api_key] if now - t < 60]
    window.append(now)
    _req_counts[x_api_key] = window
    if len(window) > RATE_LIMIT:
        raise HTTPException(429, f"Rate limit: {RATE_LIMIT} req/min")

class HashRequest(BaseModel):
    text: str
    algorithms: list[str] | None = ["sha256"]

class HashResponse(BaseModel):
    input: str
    hashes: dict[str, str]

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/hash", response_model=HashResponse)
def generate_hash(request: HashRequest, api_key: str = Depends(auth)):
    text = request.text
    algorithms = request.algorithms or ["sha256"]
    
    valid_algorithms = ["md5", "sha1", "sha256", "sha384", "sha512"]
    for algo in algorithms:
        if algo not in valid_algorithms:
            raise HTTPException(400, f"Invalid algorithm. Must be one of: {valid_algorithms}")
    
    hashes = {}
    for algo in algorithms:
        h = hashlib.new(algo)
        h.update(text.encode('utf-8'))
        hashes[algo] = h.hexdigest()
    
    return HashResponse(input=text, hashes=hashes)

handler = Mangum(app)