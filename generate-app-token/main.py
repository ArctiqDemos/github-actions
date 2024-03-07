import sys
import jwt
import requests
import os
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

app_id            = os.getenv('INPUT_APP_ID')
installation_id   = os.getenv('INPUT_INSTALLATION_ID')
kv_url            = os.getenv('INPUT_KV_URL')
kv_secret_name    = os.getenv('INPUT_KV_SECRET_NAME')

credential = ClientSecretCredential(
    client_id=os.getenv('INPUT_AZURE_CLIENT_ID'),
    client_secret=os.getenv('INPUT_AZURE_CLIENT_SECRET'),
    tenant_id=os.getenv('INPUT_AZURE_TENANT'),
    subscription_id=os.getenv('INPUT_AZURE_SUBSCRIPTION')
)

def retrieve_private_key(kv_url, kv_secret_name):
    # Create a SecretClient to access the Key Vault
    client = SecretClient(vault_url=kv_url, credential=credential)

    # Retrieve the secret (private key) from the Key Vault
    secret = client.get_secret(kv_secret_name)
    return secret.value

def get_repositories(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get("https://api.github.com/orgs/ArctiqDemos/repos", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch repositories:", response.text)
        return None

def main():
    # Retrieve the private key from Azure Key Vault
    private_key = retrieve_private_key(kv_url, kv_secret_name)

    payload = {
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=10),
        "iss": app_id
    }

    jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    )

    if response.status_code == 201:
        token_data = response.json()
        installation_token = token_data["token"]

        repositories = get_repositories(installation_token)
        if repositories:
            for repo in repositories:
                print(repo["name"])
    
        print(f"::set-output name=token::{installation_token}")
    else:
        print("Failed to generate installation token:", response.text)
        sys.exit(1)

if __name__ == "__main__":
    main()
