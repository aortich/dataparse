import hashlib

class JobListing:
    def __init__(self, url, title="", city="", state="", salaryString="", salaryLow=0, salaryHigh=0, salaryAvg=0, description="", tags=""):
        self.title = title
        self.city = city
        self.state = state
        self.salaryString = salaryString
        self.salaryLow = salaryLow
        self.salaryHigh = salaryHigh
        self.salaryAvg = salaryAvg
        self.description = description
        self.tags = tags
        self.url_hash = hashlib.sha256(url)
        self.url = url

    def getValuesString(self):
        return "{title}, {city}, {state}, {salaryString}, {salaryLow}, {salaryHigh}, {salaryAvg}, {description}, {tags}, {url_hash}, {url}".format(locals())