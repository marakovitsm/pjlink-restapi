FROM docker.io/rockylinux/rockylinux:9

# Exposing port 80
EXPOSE 80

# Setting the workdir
WORKDIR /srv/projector-restAPI

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Updating base container
RUN dnf update -y

# Installing software
RUN dnf -y install nginx python-devel openldap-devel gcc python nginx-mod-http-perl

# Installing pip dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copying everything
COPY . .

# Adding Nginx conf
ADD nginx.conf /etc/nginx/nginx.conf

# Removing nginx.conf file from /srv/ directory
RUN rm -f ./nginx.conf

# Making entry point executable
RUN chmod +x ./entrypoint.sh

# Running App
CMD [ "./entrypoint.sh" ]