#
# This is a build light meter for bamboo with blinky lights
#


import optparse
import time
import urllib2, base64
import json
import tempfile
import sys
import colorsys
import os
import glob

from BlinkyTape import BlinkyTape
from time import sleep

config = json.load(open("bamboo.json"))

def get_build_data():
    print "[%d] Fetching %s" % (time.time(), url)

    try:
        request = urllib2.Request(url)
        username = config['username']
        password = config['password']
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)   
        page_data = urllib2.urlopen(request)
        data = json.load(page_data)

        if not len(data) or data is None:
            raise Exception("Error parsing build")
        return data

    except Exception as ex:
        print ex

def connect():
    if config['usbport'] is not None:
        port = config['usbport']
        blinky = BlinkyTape(port)
        blinky.displayColor(0, 0, 0)
        return blinky
    else:
        print "Make sure you have setup your config"
        exit()


if __name__ == "__main__":
    led_count = 50
    bt = connect()
    for i in range(led_count/2):
        bt.displayColor(0,0,255)
        bt.show()
        sleep(0.05)
        bt.displayColor(255,0,0)
        bt.show()
        sleep(0.05)
        bt.displayColor(0,255,0)
        bt.show()
        sleep(0.05)
        bt.displayColor(175,175,175)
        bt.show()
        sleep(0.05)
    while True:
        for project in config['projects']:

            url = "{}/rest/api/latest/result/{}.json?expand=results[0:25].testResults".format(config['server'], project['project'])
            data = get_build_data()

            if not data:
                sys.exit(
                "Could not fetch bamboo information.")
            print project['project']

            r, g, b = (project['colour'][0]['r'], project['colour'][0]['g'], project['colour'][0]['b'])
            print "Project colours: {},{},{}".format(r, g, b)
            if data['results']['result'][0]['buildState'] == "Failed":
                for i in range(led_count):
                    bt.displayColor(255,0,0)
                    bt.sendPixel(r, g, b)
                    bt.show()
                    bt.displayColor(175,0,0)
                    bt.sendPixel(r, g, b)
                    bt.show()
                    bt.displayColor(135,0,0)
                    bt.sendPixel(r, g, b)
                    bt.show()
                    bt.displayColor(95,0,0)
                    bt.sendPixel(r, g, b)
                    bt.show()
                    bt.displayColor(45,0,0)
                    bt.sendPixel(r, g, b)
                    bt.show()
                    bt.displayColor(0,0,0)
                    bt.sendPixel(r, g, b)
                    bt.show()                   
                    sleep(0.1)

            bt.displayColor(0,0,0)
            bt.sendPixel(r, g, b)
            firstBuild = ""
            allGreen = True
            for build in data['results']['result']:
                buildState = build['buildState']
                firstBuild if firstBuild else buildState
                if buildState == "Successful":
                    r, g, b = (0, 255, 0) #success
                else:
                    r, g, b = (255,0,0)
                    allGreen = False
                print "Build State: {}. Color: {},{},{}".format(buildState, r, g, b)
                bt.sendPixel(r, g, b)

            print "Complete, waiting"

#            if allGreen:
#                sleep(45)
#            else:
            bt.show()
            cycle = config['cycle']
            sleep(cycle)



