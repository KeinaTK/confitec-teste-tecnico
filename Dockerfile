FROM python:3.10.6-slim
WORKDIR /api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src ./src
# COPY entrypoint.sh /

EXPOSE 5000

# ENTRYPOINT [ "/entrypoint.sh" ]