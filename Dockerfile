FROM python:3

WORKDIR /usr/backend
COPY requirements.txt ./
COPY django .
COPY entrypoint.sh .
RUN pip install --no-cache-dir -r requirements.txt 
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
CMD [ "uvicorn", "gigasite.asgi:application", "--host", "0.0.0.0" ]
EXPOSE 8000