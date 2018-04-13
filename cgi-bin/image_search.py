import flickrapi
import colorsys
from PIL import Image
import requests
import io
import random
import RAKE
from api_secret import API_KEY, API_SECRET

IA_URL = 'https://archive.org/metadata/{}'
IA_FLICKR_UID = '126377022@N07'
MIN_LIGHTNESS = 200 #mininum lightness of image's primary colour
MAX_SIZE = 500 #length or width of image, in pixels

def getURL(tags):

    flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='etree')



    photos = list(flickr.walk(
                           per_page=50,
                           tag_mode='any',
                           tags=tags,
                           extras='url_o',
                           sort='relevance',
                           is_commons=True))

    
    urls = []

    # return the url of the most relevant photo which matches all criteria
    for p in photos:

        img_file = requests.get(p.get('url_o'), stream=True)
        img_file.raw.decode_content = True
        im = Image.open(io.BytesIO(img_file.raw.read()))

        # convert between colour systems
        colours = max(im.getcolors(im.size[0] * im.size[1]))[1]
        try:
            hls = colorsys.rgb_to_hls(colours[0], colours[1], colours[2])
        except:
            continue
        
        lightness = int(hls[1])
        if  lightness < MIN_LIGHTNESS:
            continue # use photos with light background colour

        url_src = 'https://www.flickr.com/photos/{}/{}'.format(p.get('owner'), p.get('id'))
        url_static = "https://farm" + p.get('farm') + ".staticflickr.com/" +  p.get('server') + "/" + p.get('id') + "_" + p.get('secret') + "_b.jpg"
        urls.append((url_src, url_static))


    if len(urls) > 0:
        if len(urls)> 1: 
            random.shuffle(urls)
        return urls[0]
    else:
        return None

def searchFlickr(text):
    # First, extract keywords from text using RAKE algo
    # use the top keywords as input tags to the flickr API call
    rake = RAKE.Rake(RAKE.SmartStopList())
    keywords = rake.run(text, maxWords=1)
    keywords = [w for (w,r) in keywords]
    url = getURL(keywords)
    if url: return url
    else: return getURL(['illustration'])
