FROM python:3-alpine
WORKDIR /service
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./
COPY /sys/firmware/devicetree/base/model /sys/firmware/devicetree/base/model
EXPOSE 8080
ENTRYPOINT ["python3","-u", "main.py"]