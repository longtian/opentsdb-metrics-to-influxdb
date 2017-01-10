FROM python:3.6
ADD . .
RUN pip install -v -r requirements.txt
CMD ["python","./convert.py"]