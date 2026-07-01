import time
import uuid

from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

EMAIL = "24ds2000033@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-vaih3o.example.com"

app = FastAPI()


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()

        # Reject preflight from any non-allowed origin
        if request.method == "OPTIONS":
            origin = request.headers.get("origin")
            if origin != ALLOWED_ORIGIN:
                response = Response(status_code=403)
            else:
                response = await call_next(request)
        else:
            response = await call_next(request)

        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{time.perf_counter()-start:.6f}"

        return response


app.add_middleware(RequestMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)
