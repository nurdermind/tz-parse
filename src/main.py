import os

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from redis import Redis
from rq import Queue
from rq.job import Job

from core.parser import Parser
from core.utils import convert_content_type_to_internal_format

redis_conn = Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=os.getenv('REDIS_PORT', 6379))
q = Queue(connection=redis_conn)

app = FastAPI()


@app.post("/launch/")
async def json_endpoint(request: Request):
    body = await request.body()
    raw_data = body.decode("utf-8")
    content_type = request.headers.get('Content-Type')
    try:
        internal_format = convert_content_type_to_internal_format(content_type)
        parser = Parser([raw_data], type_format=internal_format)
        job = Job.create(parser.parse, connection=redis_conn)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    job = q.enqueue_job(job)

    return JSONResponse(content={"job_id": job.id})


@app.get("/get-result/{job_id}/")
def get_result(job_id: str):
    job = Job.fetch(job_id, connection=redis_conn)
    status = job.get_status()
    if job.is_finished:
        return JSONResponse(content={"result": job.return_value(), 'status': status})
    return JSONResponse(content={"result": None, 'status': status})
