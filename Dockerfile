FROM python:3.7-alpine
WORKDIR /app
COPY app .

RUN apk add --update --no-cache g++ gcc libxslt-dev libffi-dev cargo openssl-dev
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 3228
COPY . .
CMD ["python3", "main.py"]