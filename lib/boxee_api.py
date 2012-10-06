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

URL_ELEMENT = "url"
MESSAGE_ELEMENT = "message"
OBJECT_ELEMENT = "object"
WATCH_LATER_ELEMENT = "watchlater"

class BoxeeAPI(object):

    """docstring for BoxeeAPI"""
    def __init__(self, username, password):
        # super(BoxeeAPI, self).__init__()
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
        
        print "All the videos on your watch later queue:\n"
        pass
        
    def parse_videos(self, xml):
        
        """docstring for parse_videos"""
        tree = etree.fromstring(xml)
        all_watchlater_messages = tree.getiterator(MESSAGE_ELEMENT)
        watch_later_videos = []
        
        for each_message in all_watchlater_messages:
            if each_message.get("source") == WATCH_LATER_ELEMENT:
                each_object = each_message[2]
                if each_object.get("type") == "stream_video":
                    video = Video()
                    # watch_later_videos.append(each_object)
                    print "each object: ", each_object # before creating objects
                    video.name = unicode(each_object[0].text)
                    video.url = unicode(each_object[1].text)
                    video.thumb = unicode(each_object[3].text)
                    if len(each_object) >= 5:
                        video.description = unicode(each_object[4].text)
                    if len(each_object) >= 7:
                        video.provider = unicode(each_object[6].text)
                    # print "* [" +  video_name + "](" + video_url + ")"
                    watch_later_videos.append(video)
    	       
        return watch_later_videos