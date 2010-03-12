#google.py or Top40.py
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#	Author: ncd
#
#	Title: Top40.py
#
#	Usage: >>> execfile('google.py') 
#
#	Description: Grab the top 40 list from dogstarradio.com and pump that list
#	into google search and see if we can find some free mustic!
#
#	Version: 0.0.1
#
#	Distribution: I wrote it.  Everything is open source, therefore, this code 
#	is open source.  If I am wrong, let me know by leaving a comment on my blog
#	almostincongruent.blogspot.com
#
#	Notes:
#	__in Usage:__
#	>>> is your python prompt
#	__dependency__
#	-must have xgoogle library 
#	-->http://github.com/pkrumins
#
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import time
import os
import sys
from xgoogle.search import GoogleSearch

os.system('clear')

def gethits(): #this function gets the latest top 40 most played artists on 
			   #sirius:alt nation
	import re, urllib2
	response	= urllib2.urlopen('http://dogstarradio.com/top40.php?channel=21')
	html		= response.read()
	hitlist		= ''.join(re.findall('<td>([a-zA-Z0-9 \n&]*)</td>',html))
	hitlist_a	= []
	hitlist_b	= ''
	x = 0
	for chr in hitlist:
		if x == 40:
			break
		if chr.isdigit():
			if hitlist_b == '\n':
				hitlist_b = ''
			if chr != '1' and hitlist_b != '':
				hitlist_a.append(hitlist_b)
				x += 1
				hitlist_b = ''
			continue	
		hitlist_b += chr
	return hitlist_a #list
	
search			= '* "free music" * music * download * '
#keep updating with sites that are bad
dont_search		= ' -rapidshare -torrent -site:limewire.com -site:*wire*.com -site:*wire.com -site:wire*.com -site:*share*.com -site:*share.com -site:share*.com -site:*torrent.com -site:torrent*.com -site:bearshare.com -site:*rapidshare*.com -site:*torrent*.com -site:abcmusic.net -site:kazaa.com -site:velocityreviews.com -site:globalshareware.com' 
hot_bands		= gethits()
known_free		= ['blink182','Smashing Pumpkins'] #bands that i know provide free music

for bnd in known_free:
	hot_bands.append(bnd)

file = open(os.path.expanduser('~/top40_' + str(int(time.time())) + '.txt'),'w') #make the file 'unique'

for band in hot_bands:
	band				= '"' + band + '"'
	gs					= GoogleSearch(search + band + dont_search, random_agent=True)
	gs.results_per_page = 10 #can also be 25 or 100
	time.sleep(10)
	try: 
		results = gs.get_results()
	except:
		print 'moving on',band
		continue
	print "searching: ",search + band + dont_search
	count   = 0
	counter = 0
	for res in results:
		title = res.title.encode('utf8')
		url   = res.url.encode('utf8') 
		if count == 0:
			file.write(':artist: __<b>' + band.strip('"') + '</b>__\n')
			count += 1
		file.write('<a href="' + str(url) + '"' + 'target="_blank">' + str(title) + '</a>\n')
		counter += 1
		if counter == 5: #i only want the top five hits
			break
	time.sleep(.001) #Google does not like being harassed!

file.close()		
