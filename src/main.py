from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from redis import Redis
from rq import Queue
from rq.job import Job

from core.parser import Parser

redis_conn = Redis(host='127.0.0.1', port=6379)
q = Queue(connection=redis_conn)

app = FastAPI()


@app.post("/json-endpoint/")
async def json_endpoint(request: Request):
    body = await request.body()
    raw_json = body.decode("utf-8")
    parsed_data = Parser([raw_json])
    job = Job.create(Parser([raw_json]).parse)
    job = q.enqueue_job(job)

    return JSONResponse(content={"job_id": job.id})


@app.post("/xml-endpoint/")
async def xml_endpoint(request: Request):
    # Эндпоинт принимает произвольный XML.
    body = await request.body()
    try:
        parsed_data = Parser([body.decode("utf-8")])
        return JSONResponse(content={"received_data": parsed_data})
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid XML format") from e
