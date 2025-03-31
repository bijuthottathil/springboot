import os
import requests

# GitHub API headers
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
OWNER = REPO_NAME.split("/")[0]

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def enable_secret_scanning():
    """Enable secret scanning on the repository"""
    url = f"https://api.github.com/repos/{REPO_NAME}/security-and-analysis"
    payload = {"security_and_analysis": {"secret_scanning": {"status": "enabled"}}}
    
    response = requests.patch(url, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        print("✅ Secret scanning enabled")
    else:
        print(f"❌ Failed to enable secret scanning: {response.text}")

def set_branch_protection(branch="main"):
    """Set branch protection rules"""
    url = f"https://api.github.com/repos/{REPO_NAME}/branches/{branch}/protection"
    payload = {
        "required_status_checks": {
            "strict": True,
            "contexts": ["security-scan", "code-review"]
        },
        "enforce_admins": True,
        "required_pull_request_reviews": {
            "require_code_owner_reviews": True,
            "required_approving_review_count": 2
        },
        "restrictions": None
    }

    response = requests.put(url, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        print(f"✅ Branch protection set for {branch}")
    else:
        print(f"❌ Failed to set branch protection: {response.text}")

if __name__ == "__main__":
    print("🔐 Setting up SOX security configurations...")
    enable_secret_scanning()
    set_branch_protection()
    print("🚀 Security setup complete!")
