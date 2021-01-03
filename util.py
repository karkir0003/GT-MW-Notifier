import requests
import configparser
from email_validator import validate_email, EmailNotValidError
from mailchimp import OnCampusJobList


config = configparser.ConfigParser()
config.read('config.ini')
google_config = config['GOOGLE']

def is_valid_recaptcha(recaptcha_response) -> bool:
    request_url = 'https://www.google.com/recaptcha/api/siteverify'
    verification_data = {
        'secret': google_config['RECAPTCHA_SECRET_KEY'],
        'response': recaptcha_response
    }

    response = requests.post(request_url, data=verification_data)
    if response.status_code == 200:        
        return response.json()['success']
    else:
        return False

def is_valid_email(email) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        return False

def add_email_subscriber(new_email_subscriber):
    custom_list = OnCampusJobList()
    custom_list.add_list_member(new_email_subscriber)
    
    