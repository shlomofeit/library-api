from fastapi import FastAPI, Request, Response
from library_logging import logger
app = FastAPI()

@app.middleware("http")
def http_logger(req: Request, call_next):
    logger.info("%s %s called", req.method, req.url.path)
    response = call_next(req)

    return response