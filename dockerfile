FROM python:3.12-slim
WORKDIR /usr/local/app

COPY ./bacon_package/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./bacon_package ./bacon_package
COPY ./setup.py ./
RUN pip install .

RUN python3.12 ./bacon_package/db_generate.py

CMD ["python3.12", "./bacon_package/server.py"]