# syntax=docker/dockerfile:1
FROM python:3.9-bullseye as builder
#RUN apk add --no-cache make


#COPY . .
#RUN yarn install --production
#CMD ["node", "src/index.js"]
#EXPOSE 3000


################ Image for the virtual envirounment build  ################
## Base - "heavy" (~1GB, ~500M when compressed) image with libraries necessary
## for building modules
#FROM snakepacker/python:all as builder

# Creation of venv and pip update
RUN python3.9 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U pip

WORKDIR /python-docker

# Installing dependencies separately to be able to cache in future builds
# Docker to skip this step if requirements.txt is not changed
COPY requirements.txt /mnt/
RUN /usr/share/python3/app/bin/pip install -Ur /mnt/requirements.txt

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
## # Setting links to be able to use app commands
## RUN ln -snf /usr/share/python3/app/bin/voterjsonr /usr/local/bin/
##
# Setting command to run by default
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0:5001"]
#
EXPOSE 5001


