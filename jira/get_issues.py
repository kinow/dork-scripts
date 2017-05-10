#!/usr/bin/env python3

from jira import JIRA
import json

JIRA_URL='https://issues.apache.org/jira/'
jira = JIRA(JIRA_URL)

help_wanted_issues = jira.search_issues('project=OPENNLP AND resolution IS EMPTY and labels = help-wanted', maxResults=100)

for issue in help_wanted_issues:
    issue_url = "%sbrowse/%s" % (JIRA_URL, issue.key)
    print("* %s[%s]: %s" % (issue_url, issue.key, issue.fields.summary))
