FROM python:3.5

RUN mkdir -p /home/task/
WORKDIR /home/task/
COPY . /home/task/

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x ./run.sh
ENTRYPOINT ["bash", "./run.sh"]
