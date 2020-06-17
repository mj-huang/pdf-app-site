# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /PDF_app_site
WORKDIR /PDF_app_site

# Install dependencies
COPY Pipfile Pipfile.lock /PDF_app_site/
RUN pip install pipenv && pipenv install --system

# Copy project
COPY . /PDF_app_site/

#COPY requirements.txt /PDF_app_site/
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
#RUN pip install --upgrade django
#RUN pip install django-widget-tweaks
#RUN pip install django-cleanup
#COPY . /PDF_app_site
