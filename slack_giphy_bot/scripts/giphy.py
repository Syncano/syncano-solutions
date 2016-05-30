import json
import requests

giphy_url = CONFIG.get('giphy_url', 'http://api.giphy.com/v1/gifs/trending?api_key=dc6zaTOxFJmzC&limit=1')
slack_hook_url = CONFIG.get('slack_hook_url')
slack_channel = CONFIG.get('slack_channel')
slack_username = CONFIG.get('slack_username', 'Bot')
slack_icon_emoji = CONFIG.get('slack_icon_emoji', ':smiling_imp:')
slack_message = CONFIG.get('slack_message', '{gif}')

if not slack_hook_url:
    raise Exception('Config for "slack_hook_url" is required')

if not slack_channel:
    raise Exception('Config for "slack_channel" is required')

headers = {'content-type': 'application/json'}
response = requests.get(giphy_url, headers=headers, timeout=5)
response = response.json()
gif = response['data'][0]['images']['fixed_height_small']['url']


payload = {
    "channel": slack_channel,
    "username": slack_username,
    "text": slack_message.format(gif=gif),
    "icon_emoji": slack_icon_emoji,
}

requests.post(slack_hook_url, data=json.dumps(payload), headers=headers, timeout=5)