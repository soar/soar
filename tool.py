import os

import github as pygithub


gh = pygithub.Github(login_or_token=os.getenv("GITHUB_TOKEN"))
user = gh.get_user("soar")
print(user.login)

print("Public open PRs:")
for pr in gh.search_issues(query=f'author:{user.login} is:public type:pr state:open'):
    print(pr.repository.name, pr)

print("Public merged PRs:")
for pr in gh.search_issues(query=f'author:{user.login} is:public type:pr is:merged'):
    print(pr.repository.name, pr)
