 # for linux containers
 FROM python:3.10-slim
 # set environment variables
 ENV PYTHONUNBUFFERED=1
 ENV PYTHONDONTWRITEBYTECODE=1
 # set work directory
 WORKDIR /code
 # install dependencies
 COPY requirements.txt .
 RUN pip install django
 RUN pip install whitenoise
 RUN python -m pip install Pillow
 RUN pip install -r requirements.txt || true
 # copy project
 COPY . .
 EXPOSE 8000
 CMD ["python",  "manage.py", "runserver", "0.0.0.0:8000"]
