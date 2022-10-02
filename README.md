# 🚨 AppSec Alerts

A low effort and cheap to run, framework for tracking and alerting on dangerous patterns.

Security teams, or passionate engineers both want to catch dangerous patterns (whether code or infrastrucure) before or at the time of deployment. In an ideal world, developers would be notified of the issue when making their pull request, and given the options to either dismiss as false positive, or modify the code to fix the issue. Unfortunately rolling out this capability to an entire development team often involves a lot of friction, and paying a large sum of money to a vendor.

The alternate approach is to use an alerting pipeline where the target audience are security engineers (or self selected developers) who are notifed when a dangerous pattern is spotted and they can investigate to determine next steps.

This framework is low effort and maintainability, there are no services for you to run, it leverages CI platforms provided by GitHub and Bitbucket. There are no databases for you configure, rather it uses the repository itself to track state over time. It's easy to customise, you're free to run whatever checks you want over whatever asset you can get your hands on. Lastly, it's cheap, there are no fees to pay, you should be able to comfortably exist within the free limits provided by GitHub Actions and Bitbucket Pipelines.

### Summary
- ✅ Cheap
- ✅ Don't have to mess around with Docker or services or databases
- ✅ Very extensible
- ✅ Easy to test everything locally
- ✅ Logs and alerts when something breaks
- ✅ Git workflow for adding new alerts
- ✅ You can modify state files if you want to ignore false positives ahead of time
- ❌ You have to write some code

## Install

Simply copy this repo structure into your own organisation and delete what you don't need.

## Example Usage

This example repo is running a [single semgrep rule](https://github.com/CameronLonsdale/Appsec-Alerts/blob/main/semgrep-rules/jwt-decode-without-verify.yml) over an [example vulnerable repo](https://github.com/CameronLonsdale/Example-Vulnerable-Repo). The [scan ran](TODO LINK TO ACTION LOGS) via GitHub Actions and the finding was [committed back to the repo](TODO LINK TO COMMIT) so we don't alert on it again in the future.

## Recommendations

I highly recommend as a rule of thumb you never exceed 10 or more alerts per week. Keep the alerts as high confidence as possible, something that definitely needs attention to either confirm or declare false positive. If there is no doubt that a vulnerability was found, then add an integration to track the vulnerability elsewhere rather than send an alert.
