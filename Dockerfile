FROM registry.access.redhat.com/ubi9/ubi-minimal

# as root
USER 0
ENV PYTHON_VERSION=3.9.16

RUN microdnf update -y
RUN microdnf install pip nc -y

# set work directory
WORKDIR /code

RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

USER 1001
# Mounts the application code to the image
COPY . /code


EXPOSE 8001

# runs the production server
ENTRYPOINT ["./app/entrypoint.sh"]
