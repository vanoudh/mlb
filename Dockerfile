FROM docker.io/vanoudh/python-ml

WORKDIR /app

# Add files
ADD . .

ENV GOOGLE_CLOUD_PROJECT baseline-ml
ENV GOOGLE_APPLICATION_CREDENTIALS baseline-ml-key.json

# Install
RUN pip3 install flask \
    flask-login \
    grpcio \
    google-cloud-storage \
    google-cloud-datastore \
    urllib3 \
    gunicorn

# Run web app with one worker
ENTRYPOINT gunicorn -b 0.0.0.0:8080 --workers 1 --timeout 120 app:app