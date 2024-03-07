# Generate App Token Action

The Generate App Token Action is a GitHub Action that generates a short lived JWT from a GitHub App installation using the GitHub App's private key stored securely in Azure Key Vault.

### Prerequisites:

1.  **Python**: Ensure you have Python installed on your system. You can download and install Python from the official Python website.
    
2.  **Azure Account**: You need an Azure account to access Azure Key Vault. If you don't have an account, you can sign up for a free trial here.
    

### Setup Instructions:
    
1.  **Github Repository Secrets**:
    
    **`AZURE_SUBSCRIPTION_ID`**: This is a unique identifier for your Azure subscription. It's required to specify which Azure subscription you want to access.

    **`AZURE_CLIENT_ID`**: (Service Principal ID): When you create a Service Principal in Azure, you receive a unique identifier known as the Client ID. This ID is used to authenticate your application or pipeline with Azure.

    **`AZURE_CLIENT_SECRET`**: (Service Principal Secret): Along with the Client ID, you also receive a Client Secret when creating a Service Principal. The Client Secret acts as the password for the Service Principal and is used for authentication.

    **`AZURE_TENANT_ID`**: Azure Tenant ID is a unique identifier for your Azure Active Directory (AD) tenant. It's required for authentication and authorization processes.

3.  **GitHub App Configuration**:
    
    Ensure you have the necessary details of your GitHub App and Azure Key Vault:
    
    *   GitHub App ID (`app_id`)
    *   GitHub App Installation ID (`installation_id`)
    *   Azure Key Vault URL (`kv_url`)
    *   Azure Key Vault Secret Name (`kv_secret_name`)

## Usage

To use the Generate App Token Action in your GitHub Actions workflow, you need to provide the following inputs:

- **`kv_url`**: The URL of the Azure Key Vault where the GitHub App's private key is stored.
- **`kv_secret_name`**: The name of the secret (private key) in the Azure Key Vault.
- **`installation_id`**: The installation ID of the GitHub App.
- **`app_id`**: The ID of the GitHub App.

Here's an example workflow that uses the Generate App Token Action:

```yaml
name: Generate Temporary GitHub App Token

on:
  workflow_dispatch:

jobs:
  generate-token:
    runs-on: ubuntu-latest
    outputs:
      token: ${{ steps.generate.outputs.token }}

    steps:
    - name: Generate GitHub App Token
      id: generate
      uses: ArctiqDemos/github-actions/generate-app-token@main
      with:
        app_id: 849736
        installation_id: 48083491
        kv_url: https://github-secret-store.vault.azure.net
        kv_secret_name: safe-settings-test
        azure_client_id: ${{ secrets.AZURE_CLIENT_ID }}
        azure_client_secret: ${{ secrets.AZURE_CLIENT_SECRET }}
        azure_subscription: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        azure_tenant: ${{ secrets.AZURE_TENANT_ID }}

    - name: Get Github Repos
      run: |
        curl -H "Authorization: Bearer ${{ steps.generate.outputs.token }}" "https://api.github.com/orgs/ArctiqDemos/repos"
```
