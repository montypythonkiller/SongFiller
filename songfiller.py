#!/usr/local/bin/python
# -*- coding: utf-8 -*-


'''Bugs to solve
    adding album cover art // half-assedly done


    '''

'''
Late plans and features
    gui

    proper directory management of albums and common img file for sharing

    support formats like mp4. flac, ogg 
'''

from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, error
import os, sys # for manipualting file names
import requests
import xml.etree.ElementTree as ET
import acoustid
#request for api, mutagen for id3 of a music file, elementtree for parsing xml, acoustid for fingerprinting



    



# main function, pass the mp3 file path(s)
def songFiller(path):
    #path url without file name
    linkPath, fileName = os.path.split(path)
    # linkPath needed to rename the file in its own original directory




    # iterate through multiple sets of metadata in acoustid api
    # i actually want just a single set, but i dont know how to do that with no
    # iteration
    for recording_id, score, title, artist in acoustid.match('hINFcviwn0', path):
        artist = artist # replacing with new details
        track = title
        break # breaking the iteration after getting first set of data


    url = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=21141902233cce8762f7445b10684bc8&track=" + title + "&artist=" + artist
    #last.fm api request. getInfo of track method, sent dat of artist and track name
    # xml requested

    res = requests.get(url) # sending the request
    #print res.text #this be the response xml text

    #parsing response xml
    root = ET.fromstring(res.text) # arranging it all is easily managable xml tree

    #print root.tag #this be the root

    for child in root: #parsing through children of root(lfm in last.fm)
        for grandChild in child: #because they have two roots for no fucking reason, like track is after lfm and contains all

          #iterating and checking if any children match our requirement

            if grandChild.tag == "name":
                track = grandChild.text  # for track name

            if grandChild.tag == "artist": # artist has details like name and shit
                for greatChild in grandChild: # again iterate in child of artist
                    if greatChild.tag == "name": # artist name
                        artist = greatChild.text

            if grandChild.tag == "album": # finding album details
                pos =grandChild.attrib["position"]
                album = grandChild[1].text # rough hack may not work later. Current index 1 and 5 have album name and coverart respectively
                image = grandChild[6].text

    print "=============================================="
    print "Album:" , album
    print "Image:" , image
    print "Artist:" , artist
    print "Song:" , track
    print int(pos)

    #downloading the image
    art = requests.get(image)
    artpath = "coverart.png"
    fileimg = open(artpath, "wb")
    for chunk in art.iter_content(100000):
        fileimg.write(chunk)
    fileimg.close()

    #mutagen editing tags
    audio = EasyID3(path)
    audio["title"] = unicode(track)
    audio["artist"] = unicode(artist)
    audio["album"] = unicode(album)
    audio["albumartist"] = unicode(artist)
    audio["tracknumber"] = unicode(int(pos))
    audio.save()

    #mutagen updating cover art
    audio = MP3(path, ID3=ID3)
    audio.tags.add(
       APIC(
          encoding=1,
          mime='image/jpeg',
          type=3,
          desc=u'Cover',
          data=open(artpath).read()
       )
    )
    audio.save(v2_version=3)


    #renaming file
    newName = linkPath + "\\" + str(pos) + " " + str(track) + ".mp3"
    print newName
    #renaming the original file with tracknum+ name + artist method





    os.rename(path, newName)


#path to file
path = raw_input("Enter the directory or file(mp3) path:")
if os.path.isfile(path):
    print "Single file to be filled @", path
    songFiller(path)

    

elif os.path.isdir(path):
    print "A whole directory has been selected."
    files = os.listdir(path)
    print files
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == '.mp3':
            file = path + file
            songFiller(file)
        


else:
    print "Sorry not a file or directory. Try again."
    
        


