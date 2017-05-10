class ComplaintEntry :
    '''Represents a single entry under Latest Entries/ Latest Posts.'''
    def __init__(self, phone, code, count, latest_comment) :
        self.phone_number = phone
        self.comment = latest_comment
        self.area_code = code
        self.number_of_reports = count

    def __str__(self) :
        return "(Phone number: {}, Area Code: {}, Number of Reports: {}, Latest comment: {})".format(self.phone_number, self.area_code, self.number_of_reports, self.comment)

import urllib.request
import json
from bs4 import BeautifulSoup
from string import whitespace

URL = 'https://s3.us-east-2.amazonaws.com/gsd-auth-callinfo/callnotes.html'
HTML_PARSER = 'html.parser'

def read_and_beautify_webpage(url, parser_type) :
    '''Returns a BeautifulSoup object created from the
    url parameter which is parsed with the parser_type parameter  .'''
    page = urllib.request.urlopen(url)
    html_doc = page.read()
    soup = BeautifulSoup(html_doc, parser_type)
    return soup

def scan(soup) :
    previews = soup.find(id='previews')
    list_items = previews.find_all(class_='oos_listItem')
    items = []
    for item in list_items:
        phone_number = item.find(class_='oos_previewHeader').find('a').string
        comment = item.find(class_='oos_previewBody').contents[0].string
        area_code = item.find(class_='oos_previewFooter').find('a').string.translate(dict.fromkeys(map(ord, whitespace))).replace('areacode', '').replace('(', '').replace(')', '')
        number_of_comments = item.find(class_='postCount').string
        items.append(ComplaintEntry(phone_number, area_code, number_of_comments, comment))
    return items

def filter_by_area_code(complaint, area_code) :
    return complaint.area_code == area_code

def convert_to_json(obj) :
    return json.dumps(obj.__dict__)

def get_complaints() :
    soup = read_and_beautify_webpage(URL, HTML_PARSER)
    complaints = scan(soup)
    return complaints

def get_complaints_json() :
    complaints = get_complaints()
    if len(complaints) == 0:
        return {}
    else:
        return [convert_to_json(complaint) for complaint in complaints]

def get(area_code) :
    return [ complaint  for complaint in get_complaints()  if complaint.area_code == area_code  ]

def get_json(area_code) :
    complaints = get(area_code)
    if len(complaints) == 0 :
        return {}
    else :
        return [ convert_to_json(complaint)  for complaint in complaints ]

def main() :
    res = get_json('426')
    for r in res :
        print(r)

main()
