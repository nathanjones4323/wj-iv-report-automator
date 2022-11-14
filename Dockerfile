FROM python:3.10

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

RUN mkdir /app

COPY ./app /app

COPY . .

WORKDIR /app

EXPOSE 8501

# ENTRYPOINT ["streamlit", "run"]

# CMD ["main.py"]
