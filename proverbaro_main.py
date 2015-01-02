# -*- coding: utf-8 -*-
import logging
import argparse
import proverbaro
import datetime
from time import sleep


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='proverbaro.log', format=FORMAT)
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

day = 24 * 60 * 60

def calculate_remaining_delay(delay):
    delta  = proverbaro.fetch_delta_from_last_post()
    if delta != None and delay > delta :
        return delay - delta
    else:
        return 0

def execute_remaining_delay(delay):
    remainingtime = calculate_remaining_delay(delay)
    if(remainingtime != 0):
        logger.warning('Remaining delay time: %d' % remainingtime)
        sleep(remainingtime)


def show_proverbs(delay, limit, consumer_key, consumer_secret, access_token, access_token_key):
    publisher = proverbaro.TwitterPublisher(consumer_key, consumer_secret, access_token, access_token_key)
    if limit == None:
        while True:
            proverbaro.show_proverb(publisher)
            sleep(delay)
    else:
        for i in range(limit):
            proverbaro.show_proverb(publisher)
            if i != limit - 1:
                sleep(delay)
            else:
                logger.warning('Last proverb has been shown')

if __name__ == '__main__':
    parser  = argparse.ArgumentParser(description='Proverbaro')
    parser.add_argument('consumer_key', help='The consumer key of the aplication')
    parser.add_argument('consumer_secret', help='The consumer secret of the aplication')
    parser.add_argument('access_token', help='The access token')
    parser.add_argument('access_token_key', help='The access token secret')
    parser.add_argument('-d', '--delay', type=int, help='Delay in seconds between posting proverbs')
    parser.add_argument('-l', '--limit', type=int, help='Number of posts to show')
    parser.add_argument('-f', '--force', help='Forces posting of the first proverb without checking the delay', action="store_true")
    args = parser.parse_args()
    delay = day
    limit = None
    if args.delay:
        delay = args.delay
    if args.limit:
        limit = args.limit
    if not args.force:
        execute_remaining_delay(delay)

    show_proverbs(delay, limit, args.consumer_key, args.consumer_secret, args.access_token, args.access_token_key)
