from fastapi import Header, HTTPException

# curl -X 'GET' \
#   '{PROTOCOL}://{URL}:{PORT}}/{PATH}?token={token_value}' \
#   -H 'accept: application/json' \
#   -H 'x-token: {x-token_value}'

async def get_token_header(x_token: str = Header(...)):
    if x_token != "simple":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != "simple":
        raise HTTPException(status_code=400, detail="No Jessica token provided")