# FROM python:3.10

# WORKDIR /app

# COPY requirements.txt ./requirements.txt

# COPY main.py /app/main.py

# RUN pip3 install -r requirements.txt

# EXPOSE 8501

# COPY . /app

# ENTRYPOINT ["streamlit", "run"]

# CMD ["main.py"]

FROM python:3.10

# we probably need build tools?
RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    python3-dev

RUN apt-get install -y chromium-browser

WORKDIR /app

# if we have a packages.txt, install it
COPY packages.txt packages.txt
RUN xargs -a packages.txt apt-get install --yes

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8501

COPY . .

CMD ["streamlit", "run", "main.py"]