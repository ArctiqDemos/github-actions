# Generate Runner Token Action

The Generate Runner Token Action is an action that returns a registration token that can be used by developers to quickly get a token to register a runner to a repository.

### Prerequisites:

1.  **Python**: Ensure you have Python installed on your system. You can download and install Python from the official Python website.
    
2.  **Azure Account**: You need an Azure account to access Azure Key Vault. If you don't have an account, you can sign up for a free trial here.
    

### Setup Instructions:
    
1.  **Github Repository Secrets**:
    
    **`AZURE_SUBSCRIPTION_ID`**: This is a unique identifier for your Azure subscription. It's required to specify which Azure subscription you want to access.

    **`AZURE_CLIENT_ID`**: (Service Principal ID): When you create a Service Principal in Azure, you receive a unique identifier known as the Client ID. This ID is used to authenticate your application or pipeline with Azure.

    **`AZURE_CLIENT_SECRET`**: (Service Principal Secret): Along with the Client ID, you also receive a Client Secret when creating a Service Principal. The Client Secret acts as the password for the Service Principal and is used for authentication.

    **`AZURE_TENANT_ID`**: Azure Tenant ID is a unique identifier for your Azure Active Directory (AD) tenant. It's required for authentication and authorization processes.

2.  **GitHub App Configuration**:
    
    Ensure you have the necessary details of your GitHub App and Azure Key Vault:
    
    *   GitHub Organization (`org_name`)
    *   Giithub Repository Name (`repo_name`)
    *   Github Token (`github_token`)

## Usage

To use the Generate Runner Token Action in your GitHub Actions workflow, you need to provide the following inputs:

- **`org_name`**: The Github organization the repository resides in.
- **`repo_name`**: The name of the repository the runner will be registered to.
- **`github_token`**: The token used for authorization of API requests to Github.

Here's an example workflow that uses the Generate Runner Token Action:

```yaml
name: Generate Github Runner Token

on:
  workflow_dispatch:

jobs:
  generate-token:
    runs-on: ubuntu-latest
    outputs:
      token: ${{ steps.generate.outputs.token }}

    steps:
    - name: Generate Github App JWT
      id: auth
      uses: ArctiqDemos/github-actions/generate-app-token@main
      with:
        app_id: <GITHUB_APP_ID>
        installation_id: <GITHUB_APP_INSTALLATION_ID>
        kv_url: https://github-secret-store.vault.azure.net
        kv_secret_name: safe-settings-test
        azure_client_id: ${{ secrets.AZURE_CLIENT_ID }}
        azure_client_secret: ${{ secrets.AZURE_CLIENT_SECRET }}
        azure_subscription: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
        azure_tenant: ${{ secrets.AZURE_TENANT_ID }}

    - name: Get Runner Registration Token
      id: generate
      uses: ArctiqDemos/github-actions/generate-runner-token@main
      with:
        org_name: ArctiqDemos
        repo_name: github-actions
        github_token: ${{ steps.auth.outputs.token }} # Using a short lived JWT token that was generated in the first step.
```
