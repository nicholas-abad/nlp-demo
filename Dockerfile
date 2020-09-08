FROM tiangolo/meinheld-gunicorn:python3.7

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

RUN ls