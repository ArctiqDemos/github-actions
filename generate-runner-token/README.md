# Generate App Token Action

The Generate App Token Action is a GitHub Action that generates a token for a GitHub App installation using the GitHub App's private key stored securely in Azure Key Vault.

### Prerequisites:

1.  **Python**: Ensure you have Python installed on your system. You can download and install Python from the official Python website.
    
2.  **Azure Account**: You need an Azure account to access Azure Key Vault. If you don't have an account, you can sign up for a free trial here.
    

### Setup Instructions:
    
1.  **Create Secrets**:
    
    Create a repository secret called `AZURE_CREDENTIALS` with the following:
    
    ```json
    {
    "clientId": "<YOUR_CLIENT_ID>",
    "clientSecret": "<YOUR_CLIENT_SECRET>",
    "subscriptionId": "<YOUR_SUBSCRIPTION_ID>",
    "tenantId": "<YOUR_TENANT_ID>",
    }
    ```

3.  **GitHub App Configuration**:
    
    Ensure you have the necessary details of your GitHub App and Azure Key Vault:
    
    *   GitHub App ID (`app_id`)
    *   GitHub App Installation ID (`installation_id`)
    *   GitHub App Token (`token`)
    *   Azure Key Vault URL (`vault_url`)
    *   Azure Key Vault Secret Name (`secret_name`)

## Usage

To use the Generate App Token Action in your GitHub Actions workflow, you need to provide the following inputs:

- **Azure Key Vault URL**: The URL of the Azure Key Vault where the GitHub App's private key is stored.
- **Azure Key Vault Secret Name**: The name of the secret (private key) in the Azure Key Vault.
- **GitHub App Installation ID**: The installation ID of the GitHub App.
- **GitHub App ID**: The ID of the GitHub App.

Here's an example workflow that uses the Generate App Token Action:

```yaml
name: Generate GitHub App Token

on:
  workflow_dispatch:


jobs:
  generate-token:
    runs-on: ubuntu-latest
    outputs:
      token: ${{ steps.generate.outputs.token }}

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Generate GitHub App Token
      id: generate
      uses: ArctiqTeam/a-github-actions/generate-app-token@main
      with:
        app_id: ${{ secrets.APP_ID }}
        installation_id: ${{ secrets.INSTALLATION_ID }}
        kv_url: ${{ secrets.KV_URL }}
        kv_secret_name: ${{ secrets.KV_SECRET_NAME }}
        azure_credentials: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Get Org Repos
      run: |
        curl -H "Authorization: Bearer ${{ steps.generate.outputs.token }}" "https://api.github.com/orgs/ArctiqDemos/repos"  

```
