from django.conf import settings
import hashlib
import re
import requests
import json

MAILCHIMP_API_KEY = getattr(settings, 'MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = getattr(settings, 'MAILCHIMP_DATA_CENTER')
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, 'MAILCHIMP_EMAIL_LIST_ID')

def check_email(email):
    if not re.match(r'.+@.+\..+', email):
        raise ValueError('String passed is not a valid email address')
    return email

def get_subscriber_hash(email):
    check_email(email)
    email = email.lower().encode()
    hashed_email = hashlib.md5(email)
    return hashed_email.hexdigest()

class Mailchimp:
    def __init__(self):
        self.key = MAILCHIMP_API_KEY
        self.api_url= f'https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0'
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = f'{self.api_url}/lists/{self.list_id}'

    def get_members_endpoint(self):
        return self.list_endpoint + '/members/'

    def change_subscription_status(self, email, status='unsubscribed'):
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint() + hashed_email
        data = {
        'status': self.check_valid_status(status)
        }
        r = requests.put(endpoint, auth=('', self.key), data=json.dumps(data))
        return r.status_code, r.json()

    def check_subscription_status(self, email):
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint() + hashed_email
        r = requests.get(endpoint, auth=('', self.key))
        return r.status_code, r.json()

    def check_valid_status(self, status):
        choices = ['subscribed', 'unsubscribed', 'cleaned', 'pending']
        if status not in choices:
            raise ValueError('Not a valid choice for email status')
        return status

    def add_email(self, email, status='subscribed'):
        data = {
            'email_address': email,
            'status': self.check_valid_status(status)
        }
        endpoint = self.get_members_endpoint()
        r = requests.post(endpoint, auth=('', self.key), data=json.dumps(data))
        return r.status_code, r.json()

    def unsubscribe(self, email):
        return self.change_subscription_status(email, status='unsubscribed')

    def subscribe(self, email):
        return self.change_subscription_status(email, status='subscribed')

    def pending(self, email):
        return self.change_subscription_status(email, status='pending')



