# taken from http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
# because I want to access the classes module

# import os, sys, inspect
# cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
# if cmd_folder not in sys.path:
#     sys.path.insert(0, cmd_folder)

from lxml import etree
import requests
import sys
import getpass
from classes.video import Video

URL_ELEMENT            = "url"
MESSAGE_ELEMENT        = "message"
OBJECT_ELEMENT         = "object"
WATCH_LATER_ELEMENT    = "watchlater"
NAME_ELEMENT           = "name"
THUMB_ELEMENT          = 'thumb'
DESCRIPTION_ELEMENT    = 'description'
PROVIDER_ELEMENT       = 'provider'
SOURCE_ELEMENT         = 'source'
TYPE_ELEMENT           = 'type'

class BoxeeAPI(object):

    """docstring for BoxeeAPI"""
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_videos(self):
        """docstring for connect"""

        # obtain the xml file from the Internet
        r = requests.get('http://app.boxee.tv/api/get_queue', auth=(self.username, self.password))
        if r.status_code == 200:
            return self.parse_videos(r.content)
            # xml = r.content
        else:
            print "Something went wrong, exiting..."
            return []

        pass

    def parse_videos(self, xml):
        """docstring for parse_videos"""
        tree = etree.fromstring(xml)
        all_watchlater_messages = tree.getiterator(MESSAGE_ELEMENT)
        watch_later_videos = []

        for each_message in all_watchlater_messages:
            if each_message.get(SOURCE_ELEMENT) == WATCH_LATER_ELEMENT:
                for each_object in each_message.iterchildren(OBJECT_ELEMENT):
                    if each_object.get(TYPE_ELEMENT) == "stream_video":
                        video = Video()
                        for element in each_object.iterchildren():
                            if element.tag == NAME_ELEMENT:
                                video.name = unicode(element.text)
                                # print "video name: ", video.name
                            if element.tag == URL_ELEMENT:
                                video.url = unicode(element.text)
                                # print "video url: ", video.url
                            if element.tag == THUMB_ELEMENT:
                                video.thumb = unicode(element.text)
                                # print "video thumb: ", video.thumb
                            if element.tag == DESCRIPTION_ELEMENT:
                                video.description = unicode(element.text)[:137]+"..."
                                # print "video description: ", video.description
                            if element.tag == PROVIDER_ELEMENT:
                                video.provider = unicode(element.text)
                                # print "video provider: ", video.provider
                            else:
                                video.provider = "Unknown"

                        watch_later_videos.append(video)

        return watch_later_videos