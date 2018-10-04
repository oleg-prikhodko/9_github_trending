import sys
from datetime import date, timedelta
from functools import reduce

import requests


def validate_response(response):
    ok_status_code = 200
    if response.status_code != ok_status_code:
        raise ValueError(response.text)


def get_trending_repositories(max_repos, since):
    api_url = "https://api.github.com/search/repositories"
    headers = {"Accept": "application/vnd.github.v3+json"}
    params = {
        "q": "created:>={}".format(since.isoformat()),
        "sort": "stars",
        "per_page": max_repos,
    }
    response = requests.get(api_url, params=params, headers=headers)
    validate_response(response)
    repos = response.json()["items"]
    return repos


def get_open_issues_amount(repo_owner, repo_name):
    api_url = "https://api.github.com/repos/{}/{}/issues".format(
        repo_owner, repo_name
    )
    params = {"state": "open"}
    response = requests.get(api_url, params=params)
    validate_response(response)

    issues = response.json()
    accumulator_initial_value = 0
    issues_amount = reduce(
        lambda accumulator, issue: accumulator + 1
        if "pull_request" not in issue
        else accumulator,
        issues,
        accumulator_initial_value,
    )
    return issues_amount


def print_repos(repos_with_issues_amount):
    for repo, issues_amount in repos_with_issues_amount:
        print(
            "{}: {} stars, {} issue(s) -> {}".format(
                repo["name"],
                repo["stargazers_count"],
                issues_amount,
                repo["html_url"],
            )
        )


if __name__ == "__main__":
    try:
        week_ago = date.today() - timedelta(weeks=1)
        trending_repos = get_trending_repositories(
            max_repos=20, since=week_ago
        )
        issues_amounts = [
            get_open_issues_amount(repo["owner"]["login"], repo["name"])
            for repo in trending_repos
        ]
        repos_with_issues_amount = zip(trending_repos, issues_amounts)
        print_repos(repos_with_issues_amount)
    except (ValueError, requests.RequestException) as error:
        sys.exit(error)
