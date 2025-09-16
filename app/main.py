
from fastapi import APIRouter, HTTPException,FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import routes_auth, routes_predict
from app.middleware.loggingMiddleware import LoggingMiddleware
from app.core.exceptions import register_exception_handlers

app =  FastAPI(title="Car Price Prediction API", version="1.0.0")

app.add_middleware(LoggingMiddleware)

app.include_router(routes_auth.router,  tags=["Authentication"])
app.include_router(routes_predict.router,  tags=["Prediction"])

Instrumentator().instrument(app).expose(app).expose(app)
register_exception_handlers(app)
