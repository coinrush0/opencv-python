from typing import Optional
from fastapi import FastAPI
from starlette.responses import StreamingResponse
from fastapi import Depends, FastAPI
from .dependencies import get_query_token, get_token_header
from app.routers.image import scan
import uvicorn

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(scan.router)

@app.get("/favicon.ico")
def favicon():
    file_like = open("./favicon.ico", mode="rb")
    return StreamingResponse(file_like, media_type="image/ico")

@app.get("/")
async def read_root():
    return {"Hello": "World"}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)