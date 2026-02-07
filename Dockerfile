FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
#COPY Dockerfile/ /app

#EXPOSE 8000

CMD ["python", "blog_project/manage.py", "runserver", "0.0.0.0:8000"]