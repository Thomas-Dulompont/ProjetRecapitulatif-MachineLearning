FROM python

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt


EXPOSE 8000

CMD ["uvicorn", "fast_api_genre:app", "--host", "0.0.0.0", "--port", "8002"]


# docker build -t nom .   
# docker run -p 8001:8001 nom