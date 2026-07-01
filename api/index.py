import time
import uuid
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, Response

EMAIL = "24ds2000033@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-vaih3o.example.com"

app = FastAPI()


@app.middleware("http")
async def request_middleware(request: Request, call_next):
    start = time.perf_counter()

    origin = request.headers.get("origin")

    # Handle CORS preflight ourselves
    if request.method == "OPTIONS":
        if origin == ALLOWED_ORIGIN:
            response = Response(status_code=200)
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            response.headers["Vary"] = "Origin"
        else:
            # Reject other origins with NO ACAO header
            response = Response(status_code=403)
    else:
        response = await call_next(request)

        # Only add ACAO for the allowed origin
        if origin == ALLOWED_ORIGIN:
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Vary"] = "Origin"

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"

    return response


@app.get("/stats")
async def stats(values: str = Query(...)):
    try:
        nums = [int(x.strip()) for x in values.split(",") if x.strip()]
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": "values must contain comma-separated integers"},
        )

    if not nums:
        return JSONResponse(
            status_code=400,
            content={"error": "values cannot be empty"},
        )

    total = sum(nums)

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / len(nums),
    }


@app.get("/")
async def root():
    return {"status": "ok"}
