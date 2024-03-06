import requests
import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

app_id            = os.getenv('INPUT_APP_ID')
installation_id   = os.getenv('INPUT_INSTALLATION_ID')
kv_url            = os.getenv('INPUT_KV_URL')
kv_secret_name    = os.getenv('INPUT_KV_SECRET_NAME')
token             = os.getenv('INPUT_TOKEN')

credential = ClientSecretCredential(
    client_id=os.getenv('INPUT_AZURE_CLIENT_ID'),
    client_secret=os.getenv('INPUT_AZURE_CLIENT_SECRET'),
    tenant_id=os.getenv('INPUT_AZURE_TENANT'),
    subscription_id=os.getenv('INPUT_AZURE_SUBSCRIPTION')
)

def generate_new_private_key(installation_id, token):
    # Generate a new private key for the GitHub App
    response = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/new_private_key",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 201:
        private_key_data = response.json()
        return private_key_data["key"]
    else:
        print("Failed to generate new private key:", response.text)
        return None

def update_private_key_in_keyvault(vault_url, secret_name, new_private_key):
    # Create a SecretClient to access the Key Vault
    #credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    # Update the secret (private key) in the Key Vault
    client.set_secret(secret_name, new_private_key)

def main():
    # Generate a new private key for the GitHub App
    new_private_key = generate_new_private_key(installation_id, token)
    if new_private_key:
        # Update the private key in Azure Key Vault
        update_private_key_in_keyvault(kv_url, kv_secret_name, new_private_key)
        print("Private key updated in Azure Key Vault.")
    else:
        print("Failed to generate new private key.")

if __name__ == "__main__":
    main()
