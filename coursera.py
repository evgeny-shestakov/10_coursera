import requests
import openpyxl
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html
import random
import re


def get_random_indexes(max_range, num_items):
    num_items = min(max_range, num_items)
    return random.sample(list(i for i in range(max_range - 1)), num_items)
    

def parse_course_simple_content(html_content, selector, add_regex_remove = ''):
    soup = BeautifulSoup(html_content, 'html.parser')
    regex = '<[^<]+?>{0}'.format(add_regex_remove)
    try:
        return re.sub(regex, '', str(soup.select(selector)[0])).strip()
    except IndexError:
        return None


def get_courses_list(url = 'https://www.coursera.org/sitemap~www~courses.xml', 
                     max_urls = 20):
    xml = html.fromstring(requests.get(url).text.encode('utf-8'))
    count_locs = int(xml.xpath("count(//url/loc)"))
    random_indxs = get_random_indexes(count_locs, max_urls)
    return (xml.xpath("//url/loc")[indx].text for indx in random_indxs)


def get_course_info(course_slug):
    html = requests.get(course_slug).text.encode('utf-8')
    course = {'url': course_slug}
    course_params = [('lang', 'div.rc-Language', '|(Subtitles: )'), 
        ('date', 'div.rc-StartDateString', '|(Starts)'), 
        ('avg_rating', 'div.ratings-text', '|(stars)'),
    ]

    for course_param, css_selector, add_regex in course_params:
        course[course_param] = parse_course_simple_content(html, 
                                                           css_selector, add_regex)
    #soup = BeautifulSoup(, 'html.parser')
    #for text in :
    
    #lang = re.sub('<[^<]+?>', '', str(soup.select('div.rc-Language')[0]))
    #date = re.sub('<[^<]+?>', '', str(soup.select('div.rc-StartDateString')[0]))
    #course['lang'] = parse_course_content(html, 'div.rc-Language')
    #course['date'] = parse_course_content(html, 'div.rc-StartDateString')
    
    #startdate rc-StartDateString caption-text
    
    print(course)
    #test = soup.find_all('div.rc-Language')
    


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    #for url in get_courses_list(max_urls = 1):
    #    print (url)
    #course_slug = 'https://www.coursera.org/learn/leadership-design-innovation'
    course_slug = 'https://www.coursera.org/learn/protools'
    
    print(get_course_info(course_slug))

 