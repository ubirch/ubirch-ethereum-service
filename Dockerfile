FROM python:3.6

WORKDIR /ethereum-service/

COPY requirements.txt ubirch-ethereum-service/ethereum_service.py /ethereum-service/

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "ethereum_service.py"]
