FROM python:3.11

RUN apt-get update && apt-get install -y locales locales-all
RUN export LC_TIME="ru_RU.UTF-8"
RUN dpkg-reconfigure locales
WORKDIR /src/

COPY /src/requirements.txt .
RUN pip install -r requirements.txt

COPY ./src /src

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]