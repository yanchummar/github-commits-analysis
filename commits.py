import json

from utils.github import call_github_api
from config import COMMITS_SINCE

orgs = call_github_api('/user/orgs', {'per_page': 100})

print('\nGitHub Commits')
print('---------------\n')

print('Select an organization:')
for idx, c_org in enumerate(orgs):
  org_name = c_org['login']
  print('%d. %s' % (idx+1, org_name))

org = int(input('Enter organization\'s number (0 to exit): '))
if org == 0:
  exit
else:
  org = orgs[org-1]

# fetching repos in org
print('\nFetching commits in %s... (this might take a while)' % (org['login']))
repos = []
r_page = 1
while True:
  c_repos = call_github_api('/orgs/%s/repos' % (org['login']), {'per_page': 100, 'page': r_page})
  if len(c_repos) == 0:
    break
  repos += c_repos
  r_page += 1

# fetching commits from each repo
commits = []
for repo in repos:
  repo_commits_url = str(repo["commits_url"]).replace("{/sha}", "")
  c_page = 1
  while True:
    c_commits = call_github_api(repo_commits_url, {'per_page': 100, 'page': c_page, 'since': COMMITS_SINCE}, is_url=True)
    if len(c_commits) == 0:
      break

    for commit in c_commits:
      c_commit = call_github_api(commit['url'], is_url=True) 
      commit['stats'] = c_commit['stats']
      commits.append(commit)

    c_page += 1

with open('data/commits.json', 'w+', encoding='utf-8') as f:
  json.dump(commits, f, ensure_ascii=False, indent=2)

print('Saved %s commits' % (len(commits)))