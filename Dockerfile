FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./src/ /code/src/
COPY ./seeders/ /code/seeders/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]