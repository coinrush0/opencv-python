import cv2
import numpy as np
import base64
import io

from fastapi import APIRouter, Depends, FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from ...dependencies import get_token_header
from app.routers.image.library import cv_functions

# curl -X 'GET' \
#   'http://{URL}:{PORT}}/image/scan/?token={token_value}' \
#   -H 'accept: application/json' \
#   -H 'x-token: {x-token_value}'

router = APIRouter(
    prefix="/image",
    tags=["image"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/scan/")
async def scan(file: bytes = File(...)):
    data = np.fromstring(file, dtype=np.uint8)

    img = cv2.imdecode(data, cv2.IMREAD_ANYCOLOR)
    try:
        height, width, channel = img.shape
    except ValueError:
        height, width = img.shape

    limitSize = 1080
    if height > width:
        if height > limitSize:
            ratio = height / width
            height = limitSize
            width = limitSize / ratio
    else:
        if width > limitSize:
            ratio = width / height
            width = limitSize
            height = limitSize / ratio
    
    dsize = (int(width), int(height))
    img = cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)
    img = cv_functions.remove_image_shadow(img)
    
    res, img = cv2.imencode(".png", img)
    return StreamingResponse(io.BytesIO(img.tobytes()), media_type="image/png")