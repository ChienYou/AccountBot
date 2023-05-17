FROM python:3.10
WORKDIR /AccountBot
COPY requirements.txt /AccountBot/
RUN pip install -r requirements.txt
COPY . /AccountBot
CMD python main.py