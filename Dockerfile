FROM python:alpine3.7
COPY . /pyblock
WORKDIR /pyblock
RUN pip install -r requirements.txt
EXPOSE 5050
CMD python ./app.py