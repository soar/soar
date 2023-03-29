import os
import pathlib
import re
import typing

import dotenv
import github as pygithub
import yaml


dotenv.load_dotenv(dotenv.find_dotenv())


if __name__ == '__main__':
    config: dict = yaml.load(pathlib.Path("config.yml").open(mode="r"), yaml.FullLoader)

    gh = pygithub.Github(login_or_token=os.getenv("GITHUB_TOKEN"))
    user = gh.get_user(config.get("user"))

    # print("Public open PRs:")
    # for pr in gh.search_issues(query=f'author:{user.login} is:public type:pr state:open'):
    #     print(pr.repository.name, pr)
    #
    # print("Public merged PRs:")
    # for pr in gh.search_issues(query=f'author:{user.login} is:public type:pr is:merged'):
    #     print(pr.repository.name, pr)

    prs_output = [
        "<!-- prs -->",
        "## ⛙ My Pull Requests",
        "| Repository | Pull Request | Status | Changes |",
        "| --- | --- | --- | --- |",
    ]
    for pr_link in config.get("pull-requests"):
        pr_link: typing.Dict
        repo = gh.get_repo(pr_link.get("repo"))
        pr = repo.get_pull(pr_link.get("id"))
        prs_output.append(
            f"| `{repo.full_name.split('/')[0]}`/`{repo.name}` | [{pr.title}]({pr.html_url}) "
            f"| {'✔' if pr.merged else ''} | `+{pr.additions}/-{pr.deletions}` |"
        )
    prs_output.append("<!-- end prs -->")

    readme_file = pathlib.Path("README.md")
    readme_content = readme_file.read_text(encoding="utf-8")

    readme_content = re.sub(f"{prs_output[0]}.*{prs_output[-1]}", "\n".join(prs_output), readme_content, flags=re.DOTALL)

    readme_file.write_text(readme_content, encoding="utf-8")
