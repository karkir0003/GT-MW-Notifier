from bs4 import BeautifulSoup, element
import requests
from dateutil.parser import parse
import json

JOB_WEBSITE = 'https://studentcenter.gatech.edu/campus-jobs'
JOB_POSTING_CONTAINER_ID = 'block-views-job-postings-block-3'
JOB_POSTING_CLASS = 'views-row'


class JobPostingScraper:
    def __init__(self):
        self.jobs = []

    def getRawData(self):
        response = requests.get(JOB_WEBSITE)
        website_contents = None
        if (response.status_code == 200):
            website_contents = response.text
        else:
            raise "Error accessing website"

        return website_contents

    def getRawJobPostings(self):
        raw_data = self.getRawData()
        soup = BeautifulSoup(raw_data, 'html.parser')
        job_postings_container = soup.find(
            'div', {'id': JOB_POSTING_CONTAINER_ID})
        job_postings = job_postings_container.findAll(
            'div', {'class': JOB_POSTING_CLASS})

        return job_postings


class JobPostingParser:
    def __init__(self, raw_job_posting):
        self.raw_job_posting = raw_job_posting

    def parsePrefixSuffixComponent(self, class_name):
        raw_job_data = self.raw_job_posting.find('div', {'class': class_name})
        prefix = raw_job_data.find(
            'span', {'class': 'field-prefix'}).get_text()
        suffix = raw_job_data.find(
            'span', {'class': 'field-suffix'}).get_text()
        content = raw_job_data.contents[4]

        return f"{prefix} {content} {suffix}".strip()

    def parseBasicComponent(self, class_name):
        raw_job_data = self.raw_job_posting.find('div', {'class': class_name})
        return raw_job_data.contents[2].strip()

    def getTitle(self):
        return self.parsePrefixSuffixComponent('webform-component--position-title')

    def getStartDate(self):
        str_date = self.parseBasicComponent('webform-component--start-date')
        return parse(str_date).isoformat()

    def getEndDate(self):
        str_date = self.parseBasicComponent('webform-component--end-date')
        return parse(str_date).isoformat()

    def getContactName(self):
        return self.parsePrefixSuffixComponent('webform-component--contact-name')

    def getContactEmail(self):
        return self.parseBasicComponent('webform-component--contact-email')

    def getDescription(self):
        raw_job_description = self.raw_job_posting.find(
            'div', {'class': 'webform-component--job-description'})
        return raw_job_description.find('div', {'class': 'webform-long-answer'}).get_text().strip()

    def getHoursSchedule(self):
        return self.parsePrefixSuffixComponent('webform-component--hours-schedule')

    def getLocation(self):
        return self.parsePrefixSuffixComponent('webform-component--location')

    def getWorkStudy(self):
        return self.parsePrefixSuffixComponent('webform-component--work-study')

    def getPayRate(self):
        return self.parsePrefixSuffixComponent('webform-component--pay-rate')

    def getPositionsAvailable(self):
        return self.parsePrefixSuffixComponent('webform-component--positions-available')

    def getJob(self):
        return {
            'title' : self.getTitle(),
            'start_date' : self.getStartDate(),
            'end_date' : self.getEndDate(),
            'contact_name' : self.getContactName(),
            'contact_email' : self.getContactEmail(),
            'description' : self.getDescription(),
            'hours' : self.getHoursSchedule(),
            'location' : self.getLocation(),
            'work_study' : self.getWorkStudy(),
            'pay_rate' : self.getPayRate(),
            'positions_available' : self.getPositionsAvailable()
        }


scraper = JobPostingScraper()
job_postings = scraper.getRawJobPostings()

jobs = [JobPostingParser(x).getJob() for x in job_postings]

print(json.dumps(jobs, indent=4))
