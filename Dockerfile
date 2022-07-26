FROM python:3.9
WORKDIR /code
# copy all the code to /code
COPY . /code
# copy requirements
COPY ./requirements.txt /code/requirements.txt
# install requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# run server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]