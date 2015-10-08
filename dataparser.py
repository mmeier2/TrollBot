
# coding=utf-8
from lxml import html
import re
import redis
import requests
from app import app

from cli_chat import remove_punc

phrase_dict = {}
script_files = ['trailer_park.txt', 'office.txt', 'arrested_dev.txt']


def cleanup(script):
    lines = []
    for line in script:
        line = remove_punc(line)
        line_list = re.split('-', line)
        for new in line_list:
            if ':' in new or '[' in new:
                pass
            else:
                lines.append(new)

    return lines


def three_base_chain(phrases):
    """
    takes in a list of phrases and parses into the three based groupings
    to store into the redis datastore
    """ 
    for phrase in phrases:
        phrase = (phrase + ' <stop>').lower().split()
        phrase_length = len(phrase)
        if phrase_length == 2:
            phrase.append('<stop>')
        for index, word in enumerate(phrase):
            if index < phrase_length - 2 and phrase_length > 2:
                phrase_key = (phrase[index], phrase[index+1])
                if phrase_key in phrase_dict:
                    if phrase[index+2] in phrase_dict[phrase_key]:
                        pass
                    else:
                        a = phrase_dict[phrase_key]
                        b = phrase[index+2]
                        a.append(b)
                        phrase_dict[phrase_key] = a
                else:
                    phrase_dict[phrase_key] = [phrase[index+2]]

def add_to_redis(db):
    redis_conn = redis.Redis(host='localhost', port='6379', db=db)
    for key, value in phrase_dict.iteritems():
        for word in value:
            redis_conn.sadd('-'.join(key), word)


def parse_data():
    for i, script in enumerate(script_files):
        print "reading " + script
        with open(script, 'r') as f:
            urls = f.readlines()

        for url in urls:
            url = url.replace('\n', '')
            webpage = requests.get(url)
            tree = html.fromstring(webpage.text)

            # print webpage.text
            script_container = tree.xpath('//div[@class="episode_script"]')
            script = tree.xpath('//div[@class="scrolling-script-container"]/text()')
            script = cleanup(script)

            print "creating chains"
            three_base_chain(script)

        print "adding to redis"
        add_to_redis(i)

if __name__ == '__main__':
    parse_data()
