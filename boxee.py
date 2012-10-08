# TODO
# web interface based on backbone and pinterest grid-like layout
# ideia: http://www.wtfdiary.com/2012/08/6-amazing-jquery-plugins-to-design.html

from lxml import etree
import requests
import sys
import getpass

# credentials
print "Insert your boxee credentials: "
username = raw_input("Username: ")
password = getpass.getpass("Password: ") 

URL_ELEMENT = "url"
MESSAGE_ELEMENT = "message"
OBJECT_ELEMENT = "object"
WATCH_LATER_ELEMENT = "watchlater"

# obtain the xml file from the Internet
r = requests.get('http://app.boxee.tv/api/get_queue', auth=(username, password))
if r.status_code == 200:
    xml = r.content
else:
    print "Something went wrong, exiting..."
    sys.exit()

print "All the videos on your watch later queue:\n"

tree = etree.fromstring(xml)
all_watchlater_messages = tree.getiterator(MESSAGE_ELEMENT)
watch_later_videos = []

for each_message in all_watchlater_messages:
    if each_message.get("source") == WATCH_LATER_ELEMENT:
        each_object = each_message[2]
        if each_object.get("type") == "stream_video":
            watch_later_videos.append(each_object)
            print "each object: ", each_object # before creating objects
            video_name = unicode(each_object[0].text)
            video_url = unicode(each_object[1].text)
            print "* [" +  video_name + "](" + video_url + ")"
            
print len(watch_later_videos)