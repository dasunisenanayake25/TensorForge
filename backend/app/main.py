from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import health, predict, jobs
from app.config import UnauthorizedException

app = FastAPI(title="TensorForge 2.0 API")

# Custom Error Handlers to match OpenAPI ErrorResponse Schema

@app.exception_handler(UnauthorizedException)
async def unauthorized_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=401,
        content={"error": {"code": "unauthorized", "message": "Missing or invalid API key"}},
        headers={"WWW-Authenticate": "Bearer"}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for err in exc.errors():
        detail = {
            "field": str(err["loc"][-1]),
            "issue": err["msg"]
        }
        # Add index for batch requests
        if len(err["loc"]) >= 3 and err["loc"][1] == "tickets" and isinstance(err["loc"][2], int):
            detail["index"] = err["loc"][2]
        details.append(detail)
        
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "message": "Request failed validation.", "details": details}}
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Mapping common HTTP status codes to custom error schema
    code_map = {404: "not_found", 409: "job_not_ready", 410: "job_expired", 413: "payload_too_large", 415: "unsupported_media_type", 422: "validation_error", 429: "too_many_jobs"}
    error_code = code_map.get(exc.status_code, "error")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": error_code, "message": str(exc.detail)}}
    )


# Include all routers
app.include_router(health.router)
app.include_router(predict.router)
app.include_router(jobs.router)