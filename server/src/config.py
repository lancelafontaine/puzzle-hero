import os
config = {
    'allowed_host_list': [
        'http://localhost:8080'
    ],
    'blacklisted_slack_users': [
        'testuser',
        'slackbot'
    ],
    'slack_api_url': 'https://slack.com/api',
    'slack_api_token': os.environ['SLACK_TOKEN'],
    'sparkpost_api_url': 'https://api.sparkpost.com/api/v1',
    'sparkpost_api_token': os.environ['SPARKPOST_TOKEN']
}
