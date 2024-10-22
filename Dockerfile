FROM python:3.11-alpine
WORKDIR /service
COPY requirements.txt .
RUN pip install --prefer-binary -r requirements.txt
COPY . ./
EXPOSE 8080
ENTRYPOINT ["python3","-u", "main.py"]