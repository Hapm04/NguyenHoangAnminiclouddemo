# FROM python:3.11-alpine
# WORKDIR /app
# COPY app.py .
# RUN pip install --no-cache-dir flask requests python-jose
# EXPOSE 8081
# CMD ["python", "app.py"]
FROM python:3.11-alpine
WORKDIR /app
COPY students.json .
COPY app.py .
RUN pip install --no-cache-dir flask requests python-jose pymysql
EXPOSE 8081
CMD ["python", "app.py"]