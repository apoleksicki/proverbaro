# -*- coding: utf-8 -*-
import logging
import argparse
import proverbaro
from time import sleep


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='proverbaro.log', format=FORMAT)
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

day = 24 * 60 * 60

def show_proverbs(delay, limit, consumer_key, consumer_secret, access_token, access_token_key):
    if limit == None:
        while True:
            proverbaro.show_proverb(consumer_key, consumer_secret, access_token, access_token_key)
            sleep(delay)
    else:
        pass
        for i in range(limit):
            proverbaro.show_proverb(consumer_key, consumer_secret, access_token, access_token_key)
            sleep(delay)

if __name__ == '__main__':
    parser  = argparse.ArgumentParser(description='Proverbaro')
    parser.add_argument('consumer_key', help='The consumer key of the aplication')
    parser.add_argument('consumer_secret', help='The consumer secret of the aplication')
    parser.add_argument('access_token', help='The access token')
    parser.add_argument('access_token_key', help='The access token secret')
    parser.add_argument('-d', '--delay', type=int, help='Delay in seconds between posting proverbs')
    parser.add_argument('-l', '--limit', type=int, help='Number of posts to show')
    args = parser.parse_args()
    proverbaro.init_proverbaro(args.consumer_key, args.consumer_secret, args.access_token, args.access_token_key)
    delay = day
    limit = None
    if args.delay:
        delay = args.delay
    if args.limit:
        limit = args.limit


    show_proverbs(delay, limit, args.consumer_key, args.consumer_secret, args.access_token, args.access_token_key)
