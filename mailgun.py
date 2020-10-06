import requests


class MailgunApi:

    API_URL = 'https://api.mailgun.net/v3/{}/messages'

    def __init__(self, domain: str, api_key: str):
        self.domain = domain
        self.key = api_key
        self.base_url = self.API_URL.format(self.domain)

    def send_email(self, to: str, subject: str, text: str, html: str=None):        
        data = {
            'from': 'Our API <no-reply@{}>'.format(self.domain),
            'to': to,
            'subject': subject,
            'text': text,
            'html': html
        }

        return requests.post(url=self.base_url, auth=('api', self.key), data=data)
