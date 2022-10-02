import os
import json
import logging
import requests
import subprocess

logging.basicConfig(
    level="INFO",
    force=True,
    format="%(filename)s:%(lineno)s - %(funcName)s()] %(message)s",
)

# This helps us test the alerts locally. By default we setup the checks to always look in our HOME directory
# under the "Example-Vulnerable-Repo" subfolder. When deployed in GitHub Actions we will use the workspace provided by GitHub in
# an environment variable.
#
# You will want this value to be the same as the `path` value from the GitHub action, the name of the folder where the repo-to-be-scanned will be placed.
HOME = os.environ["HOME"]
SCANNING_DIRECTORY = os.environ.get("GITHUB_WORKSPACE", os.path.join(HOME, "Example-Vulnerable-Repo"))


def send_slack_alert(text: str) -> None:
    """Send an alert to a custom slack channel"""
    WEBHOOK_URL = os.environ["WEBHOOK_URL"]
    request.post(url=WEBHOOK_URL, json={"text": text})


def run_semgrep(rule: str, repo: str) -> dict:
    """Run semgrep using a single repo and repo then return the raw results"""
    output = subprocess.check_output(
        f"semgrep --config {rule} {repo} --json", shell=True
    )
    return json.loads(output.decode("utf-8"))
