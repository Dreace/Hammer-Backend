FROM dreace233/python-base:hammer
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app
COPY . /app
CMD ["python","index.py"]