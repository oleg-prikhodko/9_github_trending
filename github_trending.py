import sys
from datetime import date, timedelta

import requests


def get_trending_repositories(max_repos):
    api_url = "https://api.github.com/search/repositories"
    headers = {"Accept": "application/vnd.github.v3+json"}
    week_ago = date.today() - timedelta(weeks=1)
    params = {
        "q": "created:>={}".format(week_ago.isoformat()),
        "sort": "stars",
        "per_page": max_repos,
    }
    response = requests.get(api_url, params=params, headers=headers)
    repos = response.json()["items"]
    return repos


def print_repos(repos):
    for repo in repos:
        print(
            "{}: {} stars, {} issue(s) -> {}".format(
                repo["name"],
                repo["stargazers_count"],
                repo["open_issues_count"],
                repo["html_url"],
            )
        )


if __name__ == "__main__":
    try:
        trending_repos = get_trending_repositories(max_repos=20)
        print_repos(trending_repos)
    except requests.RequestException as error:
        sys.exit(error)
