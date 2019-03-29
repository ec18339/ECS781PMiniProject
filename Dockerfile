FROM python:3.7-alpine
WORKDIR /ECS781PMiniProject
COPY . /ECS781PMiniProject
RUN pip install -U -r requirements.txt
EXPOSE 8080
CMD ["python", "MiniProject.py"]

