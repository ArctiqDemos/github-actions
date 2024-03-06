FROM python:3.10-slim

# Install dependencies
RUN pip install --upgrade pip && \
    pip install \
        requests==2.25.1 \
        azure-identity==1.6.0 \
        azure-keyvault-secrets

COPY . /action

ENTRYPOINT ["python", "/action/rotate_private_key.py"]
