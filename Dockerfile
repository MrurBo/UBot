# Use the official Python image as the base image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment
RUN python -m venv venv

# Activate the virtual environment and install dependencies
RUN /bin/sh -c ". venv/bin/activate && pip install --no-cache-dir -r requirements.txt" || powershell -Command "& .\venv\Scripts\Activate.ps1; pip install --no-cache-dir -r requirements.txt"

# Set the entrypoint to activate the virtual environment and run the scripts
ENTRYPOINT ["/bin/sh", "-c", ". venv/bin/activate && python api.py && python main.py && python website.py || powershell -Command \"& .\\venv\\Scripts\\Activate.ps1; python api.py; python main.py; python website.py\""]