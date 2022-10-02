import os
import logging

from common import send_slack_alert, run_semgrep, SCANNING_DIRECTORY

SNAPSHOT = "state/jwt_missing_verification.txt"
SCANNING_TARGET = os.path.join(SCANNING_DIRECTORY, "Example-Vulnerable-Repo")

def identify_misconfigured_functions(raw_results: dict) -> dict:
    """Take the raw results from semgrep and return the filename & function name of the misconfigured functions"""
    findings = set()

    results = raw_results["results"]
    for result in results:
        meta_variables = result["extra"]["metavars"]
        # As defined in the semgrep rule itself, $FUNC variable has the function name
        function_name = meta_variables["$FUNC"]["abstract_content"]
        # Remove the prefix from the filename so that results are consistent whether run locally or not
        file_name = result["path"].replace(SCANNING_DIRECTORY, "")
        # In this case, I am using the file and function name to form a key for this finding. If you don't have
        # a function name, that's fine, you might like to hash the line or identifying part of the code as an identifier.
        # The downside is that its hard to look at the state file and find the particular code being referenced.
        #
        # Avoid using a line number instead because that can change without a meaningful change to the dangerous code.
        # The function name could also change, but we assume it would happen less frequent.
        findings.add(f"{file_name}:{function_name}")

    return findings


def main() -> None:
    with open(SNAPSHOT) as f:
        existing_jwt_without_verify = set(f.read().splitlines())

    raw_results = run_semgrep(
        "semgrep-rules/jwt-decode-without-verify.yml", SCANNING_TARGET
    )
    current_jwt_without_verify = identify_misconfigured_functions(raw_results)

    # We always write back to the file with the current data to be recomitted to the repo
    with open(SNAPSHOT, "w") as f:
        f.write("\n".join(sorted(current_jwt_without_verify)))

    new_findings = current_jwt_without_verify - existing_jwt_without_verify
    if new_findings:
        logging.info(f"New function(s) decoding JWT without verification: {new_findings}")
        # send_slack_alert(f"New function(s) decoding JWT without verification: {new_findings}")


if __name__ == "__main__":
    main()
