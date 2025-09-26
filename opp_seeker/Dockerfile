FROM python:3.12.3

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.

WORKDIR .

# Copy requirements first to leverage Docker cache
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . /opp_seeker

EXPOSE 5099

#CMD ["sh", "-c", "gunicorn -w 3 -b 0.0.0.0:5099 opp_seeker.flask_app.main:app"]
CMD ["python", "opp_seeker/flask_app/main.py"]
