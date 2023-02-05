FROM python:3.8-slim-buster

WORKDIR /app2
COPY . .
RUN pip install -r requirement.txt
EXPOSE 5001
CMD ["python","app2.py"]