import sys
from datetime import date, timedelta

import requests


def get_trending_repositories(max_repos, since):
    api_url = "https://api.github.com/search/repositories"
    headers = {"Accept": "application/vnd.github.v3+json"}
    params = {
        "q": "created:>={}".format(since.isoformat()),
        "sort": "stars",
        "per_page": max_repos,
    }
    response = requests.get(api_url, params=params, headers=headers)
    response.raise_for_status()
    repos = response.json()["items"]
    return repos


def get_open_issues_amount(repo_owner, repo_name):
    api_url = "https://api.github.com/repos/{}/{}/issues".format(
        repo_owner, repo_name
    )
    params = {"state": "open"}
    response = requests.get(api_url, params=params)
    response.raise_for_status()

    issues = response.json()
    issues_amount = len(
        [issue for issue in issues if "pull_request" not in issue]
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
    except requests.RequestException as error:
        sys.exit(error)
