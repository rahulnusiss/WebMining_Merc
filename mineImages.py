from bs4 import BeautifulSoup
import requests
import re
import urllib.request, urllib.error, urllib.parse
import os
#import argparse
import sys
import json


# adapted from http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search

def get_soup(url, header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')

# search = ""
# num_images
# directory
# >python mineImages.py --search "cat" --num_images 10 --directory "\images"
def main2(searchQuery, num_images):
    query = searchQuery
    max_images = num_images
    save_directory = ""
    images = []
    image_type = "Action"
    query = query.split()
    query = '+'.join(query)
    url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
    soup = get_soup(url, header)
    ActualImages = []  # contains the link for Large original images, type of  image
    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        ActualImages.append((link, Type))
    for i, (img, Type) in enumerate(ActualImages[0:max_images]):
        images.append(img)
    return images
