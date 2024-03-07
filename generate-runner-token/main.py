import requests
import os

def generate_token():
    headers = {
        "Authorization": f"token {os.environ['INPUT_GITHUB_TOKEN']}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.post(
        f"https://api.github.com/repos/{os.environ['INPUT_ORG_NAME']}/{os.environ['INPUT_REPO_NAME']}/actions/runners/registration-token",
        headers=headers
    )
    if response.status_code == 201:
        return response.json()["token"]
    else:
        print("Failed to generate runner registration token.")
        return None

if __name__ == "__main__":
    token = generate_token()
    if token:
        print(f"::set-output name=runner_token::{token}")
        print(token)
