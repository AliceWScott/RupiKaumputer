#!/usr/bin/python3
import cgitb; cgitb.enable()
from text_processor import runRupi, runFrost, runContesse, testImport
import pickle
import random
from image_search import searchFlickr
content = runRupi()
(src, static) = searchFlickr(content)
url =  ('<br><a href="{0}" title="none"><img src="{1}" alt="none"></a>').format(src, static)

print("Content-type: text/html\n\n")
print(content)
print(url)

