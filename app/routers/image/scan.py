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
    # binary_np = np.frombuffer(base64.b64decode(file), dtype=np.uint8)

    img = cv2.imdecode(data, cv2.IMREAD_ANYCOLOR)
    img = cv_functions.remove_image_shadow(img)

    cv2.imwrite('image/shadows_out.png', img)
    return FileResponse('image/shadows_out.png', media_type="image/png")