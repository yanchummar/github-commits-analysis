import json
import csv
import datetime
from utils.common import display_time

from config import COMMITS_SINCE

f = open('data/commits.json')
commits = json.load(f)
f.close()

member_data = {}
for commit in commits:
  if commit['author'] is None:
    continue
  author_login = commit['author']['login']
  if author_login not in member_data:
    member_data[author_login] = []
  member_data[author_login].append(commit)

org_name = commits[0]['commit']['url'].split('/')[4]
print('\nSelect a report for commits in %s' % org_name)
print('1. Member-wise Commits Count')
print('2. Commits from a Member')

# getting current date
now = datetime.datetime.utcnow()

while True:
  opt = int(input('\nEnter your option (0 to exit): '))

  if opt == 0:
    break

  elif opt == 1:
    output = []
    for member in member_data:
      output.append([member, len(member_data[member])])
    # saving to csv
    with open('reports/member_commits.csv', 'w+') as f:
      write = csv.writer(f)
      write.writerows(output)
    print('\nSaved report to reports/member_commits.csv')

  elif opt == 2:
    u_login = input('\nEnter the member\'s username: ')
    if u_login not in member_data.keys():
      print('No commits found from the member since %s' % (COMMITS_SINCE))
      continue
    
    u_name = member_data[u_login][0]['commit']['author']['name']
    print('\nCommits by %s' % u_name)
    print('-------------------------------------')

    offset = 0
    while True:
      print('')
      for commit in member_data[u_login][offset:offset+10]:
        commit_timestamp = datetime.datetime.strptime(commit["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
        #commit_timestamp = commit_timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
        time_diff = now - commit_timestamp
        time_diff = time_diff.total_seconds()
        print(commit["commit"]["message"], "\n%s ago" % display_time(time_diff), "\n")
      
      c_opt = input('Enter "it" to see more commits from %s: ' % u_name)
      
      if c_opt != "it":
        break
      else:
        print('------------------------------------------------')
        offset += 10
    
  
