# -*- coding: utf-8 -*-
import logging
import argparse
import proverbaro


FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='proverbaro.log', format=FORMAT)

if __name__ == '__main__':
    parser  = argparse.ArgumentParser(description='Proverbaro')
    parser.add_argument('consumer_key', help='The consumer key of the aplication')
    parser.add_argument('consumer_secret', help='The consumer secret of the aplication')
    parser.add_argument('access_token', help='The access token')
    parser.add_argument('access_token_key', help='The access token secret')
    args = parser.parse_args()
    proverbaro.init_proverbaro(args.consumer_key, args.consumer_secret, args.access_token, args.access_token_key)
    proverbaro.show_proverb()
