import os
config = {
    'allowed_host_list': [
        'http://localhost:8080'
    ],
    'blacklisted_slack_users': [
        'testuser',
        'slackbot'
    ],
    'slackApiUrl': 'https://slack.com/api',
    'slackToken': os.environ['SLACK_TOKEN']
}
