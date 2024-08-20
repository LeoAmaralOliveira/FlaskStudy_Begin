FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
EXPOSE 8000
CMD ["python", "app.py"]