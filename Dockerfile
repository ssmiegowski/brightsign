# Use the official Python image as the base image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Install system-level dependencies
#FROM ubuntu:20.04

#RUN apt-get update && apt-get install -y libsecret-1-0

# Copy the current directory contents into the container
COPY . /app

# Install required Python packages
RUN pip install requests
RUN pip install keyring
RUN pip install keyrings.alt

# Expose the port if needed
# EXPOSE 8080

# Run the Python script
#CMD ["python3", "ipstack.py"]
COPY config.json /app
ENTRYPOINT ["python3", "ipstack.py"]