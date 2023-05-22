# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code to the container
COPY ./product_aggregator_microservice .

# Set environment variables
ENV DJANGO_ENV=docker
ENV DJANGO_SETTINGS_MODULE=product_aggregator_microservice.settings

# Expose the application port
EXPOSE 8000

CMD python manage.py collectstatic --no-input
# Start the Django development server
CMD python manage.py makemigrations \
 && python manage.py migrate \
 && python manage.py runserver 0.0.0.0:8000
