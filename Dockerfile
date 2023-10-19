# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install required Python packages
RUN pip install requests
RUN pip install keyring

# Expose the port if needed
# EXPOSE 8080

# Run the Python script
#CMD ["python3", "ipstack.py"]
COPY config.json /app
ENTRYPOINT ["python3", "ipstack.py"]