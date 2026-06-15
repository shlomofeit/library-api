from fastapi import FastAPI, Request, Response
from database.db_connection import SetConnection
from library_logging import logger
from routes.book_routes import router as book_router
from routes.member_routes import router as member_router
from routes.report_routes import router as report_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    SetConnection.get_connection()

    yield

    SetConnection.close_conn()


app = FastAPI(lifespan=lifespan)

@app.middleware("http")
def http_logger(req: Request, call_next):
    logger.info("%s %s called", req.method, req.url)
    response = call_next(req)

    return response


app.include_router(book_router, tags=["Books"])

app.include_router(member_router, tags=["Members"])

app.include_router(report_router, tags=["Reports"])