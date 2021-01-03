import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import configparser

# Pull keys and other configurations
config = configparser.ConfigParser()
config.read('config.ini')
mailchimp_config = config['MAILCHIMP']

# API Reference https://github.com/mailchimp/mailchimp-marketing-python

class OnCampusJobList():
    def __init__(self):
        self._client = self.get_mailchimp_client()
        self._info = None
        self._members = None
                
    def get_mailchimp_client(self) -> MailchimpMarketing.Client:
        try:
            client = MailchimpMarketing.Client()
            client.set_config({
                "api_key": mailchimp_config['MAILCHIMP_API_KEY'],
                "server": mailchimp_config['MAILCHIMP_SERVER_PREFIX']
            })
            return client        

        except ApiClientError as error:
            print(error)
            return None

    def get_info(self):
        if self._info is None:
            mailchimp_lists = self._client.lists.get_all_lists()['lists']    
            filter_lambda = lambda x: x['name'] == mailchimp_config['LIST_NAME']
            gt_on_campus_list = list(filter(filter_lambda, mailchimp_lists))
            if len(gt_on_campus_list) == 1:
                self._info = gt_on_campus_list[0]                
            else:
                raise f"Failed to find a unique list for '{GT_ON_CAMPUS_LIST_ID}'"
       
        return self._info

    def get_members(self):
        if self._members is None:
            list_id = self.get_info()['id']
            self._members = self._client.lists.get_list_members_info(list_id)['members']
        
        return self._members

def get_email_addresses():
    custom_list = OnCampusJobList()
    members = custom_list.get_members()
    return [x['email_address'] for x in members]

print(get_email_addresses())


