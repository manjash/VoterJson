# syntax=docker/dockerfile:1
FROM python:3.10-bullseye as builder

ENV VIRTUAL_ENV=/usr/share/python3/app

################ Image for the virtual envirounment build  ################
## Base - "heavy" (~1GB, ~500M when compressed) image with libraries necessary
## for building modules
#FROM snakepacker/python:all as builder

# Creation of venv and pip update
RUN python3.10 -m venv $VIRTUAL_ENV
RUN $VIRTUAL_ENV/bin/pip install -U pip
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /python-docker

# Installing dependencies separately to be able to cache in future builds
# Docker to skip this step if requirements.txt is not changed
COPY requirements.txt /mnt/
RUN $VIRTUAL_ENV/bin/pip install -Ur /mnt/requirements.txt

COPY . .
#
## Copying source distribution into the container and installing it
#COPY dist/ /mnt/dist/
#RUN /usr/share/python3/app/bin/pip install /mnt/dist/* \
#    && /usr/share/python3/app/bin/pip check
#
############################ Final image ############################
## Using "light" image (~100M, when compressed ~50M) with python as a base
#FROM snakepacker/python:3.9 as api
#
## Copying a prepared venv from the builder container into it
#COPY --from=builder /usr/share/python3/app /usr/share/python3/app
#
# Activate venv
#RUN bash /usr/share/python3/app/bin/activate
##
# Setting command to run by default

CMD ["flask", "--app", "voterjsonr", "--debug", "run", "-p", "5000", "--host=0.0.0.0"]
#CMD ["flask", "--app", "voterjsonr", "init-db"]

EXPOSE 5000

