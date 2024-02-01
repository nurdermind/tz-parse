from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

from core.parser import Parser

app = FastAPI()


@app.post("/json-endpoint/")
async def json_endpoint(request: Request):
    body = await request.body()
    raw_json = body.decode("utf-8")
    parsed_data = Parser([raw_json]).parse()
    return JSONResponse(content={"received_data": parsed_data})


@app.post("/xml-endpoint/")
async def xml_endpoint(request: Request):
    # Эндпоинт принимает произвольный XML.
    body = await request.body()
    try:
        parsed_data = Parser([body.decode("utf-8")])
        return JSONResponse(content={"received_data": parsed_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid XML format") from e
