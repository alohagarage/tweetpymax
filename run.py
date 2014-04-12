#! /usr/bin/env python
import sys, threading, collections, json

import socket, select

from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

configs = json.loads(open('configs.json', 'r').read())

VERBOSE = False


UDP_IP = '0.0.0.0'
UDP_PORT_READ = 7777

UDP_PORT_WRITE = 7778

ts = TwitterStream(auth=OAuth(configs['OAUTH_TOKEN'], configs['OAUTH_SECRET'],
        configs['CONSUMER_KEY'], configs['CONSUMER_SECRET']), timeout=None, block=False)

read_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
read_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
read_sock.bind((UDP_IP, UDP_PORT_READ))
read_sock.setblocking(0)

read_list = [read_sock]

write_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#write_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#write_sock.bind((UDP_IP, UDP_PORT_WRITE))

write_list = [write_sock]

def get_hashtags(tweet):
    return [str(h['text']).lower() for h in tweet['entities']['hashtags']]


def tagiterator( tw ):
    for tweet in tw:
        print tweet
        for tag in get_hashtags(tweet):
            yield tag

def flush_counter(input_array, counter):

    # catch uppercase, lowercase

    _return = []

    for i in input_array:
        if counter.get(i):
            _return.append(str(counter.get(i)))
        else:
            _return.append(str(0))

    counter.clear()

    return (' ').join(_return)

def main():

    if len(sys.argv) < 2:

        print "WAITING FOR INITIAL HASHTAG ARRAY"

        data = 'bang'

        while 'bang' in data:

            data, address = read_sock.recvfrom(1024)

            hashtags_to_track = [j.replace('\x00', '').replace(',', '') for j in data.split(':')]

        print hashtags_to_track

    else:

        if sys.argv[1] == "-v":

            VERBOSE = True

        hashtags_to_track = [j.replace('\x00', '').replace(',', '') for j in sys.argv[-1].split(':')]
    
    tw = ts.statuses.filter(track=(',').join([('#' + h) for h in hashtags_to_track]))

    hashtag_counter = collections.Counter()

    for t in tw:

        readable, writable, in_error = select.select(read_list, [], [], 0)

        for s in readable:
            if s is read_sock:
                data, address = read_sock.recvfrom(1024)

                message = flush_counter(hashtags_to_track, hashtag_counter)

                write_sock.sendto(message, (UDP_IP, UDP_PORT_WRITE))


        if t:

            if VERBOSE:

                print t

            hashtag_counter.update(get_hashtags(t))


if __name__ == '__main__':
    print main()
    
