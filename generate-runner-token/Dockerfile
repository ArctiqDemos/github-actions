FROM python:3.10-slim

# Install required dependencies
RUN pip install requests

# Copy the Python script into the container
COPY main.py /main.py

# Set the entrypoint for the action
ENTRYPOINT ["python", "/main.py"]