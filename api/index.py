import time
import uuid
from typing import List

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# ==========================
# CHANGE THIS
# ==========================
EMAIL = "24ds2000033@ds.study.iitm.ac.in"

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-vaih3o.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        elapsed = time.perf_counter() - start

        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{elapsed:.6f}"

        return response


app.add_middleware(ProcessTimeMiddleware)


@app.get("/stats")
async def stats(values: str = Query(...)):
    nums: List[int] = []

    for v in values.split(","):
        v = v.strip()
        if v:
            nums.append(int(v))

    count = len(nums)
    total = sum(nums)

    return {
        "email": EMAIL,
        "count": count,
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / count,
    }
