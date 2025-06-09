FROM python:3

WORKDIR /usr/src/gigasite
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY django .
CMD ["uvicorn", "gigasite.asgi:application"]
EXPOSE 8000