#google.py or Top40.py
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#	Author: ncd
#
#	Title: Top40.py
#
#	Usage: >>> execfile('google.py') or >>> execfile('Top40.py') 
#
#	Description: Grab the top 40 list from dogstarradio.com and pump that list
#	into google search and see if we can find some free mustic!
#
#	Version: 1.0.1
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
#	Code is licensed under MIT license.
#
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import time
import os
import sys
import traceback
import re
import urllib2
import random

from xgoogle.search import GoogleSearch

os.system('clear')

###############################################################################
# This function gets the latest top 40 most played artists on sirius:alt nation
###############################################################################
def gethits(): 
	response = urllib2.urlopen('http://dogstarradio.com/top40.php?channel=21')
	html = response.read()
	###########################################################################
	# TODO: did not find 'Thirty Seconds to Mars,' you found ' Seconds to Mars'
	###########################################################################
	hitlist	= ''.join(re.findall('<td>([0-9 A-Za-z0-9 \n&]*)</td>',html)) 
	hitlist_a = []
	hitlist_b = ''
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

	return hitlist_a
	
search = '* "free music" * music * download * '

###############################################################################
# keep updating with sites that are bad
###############################################################################
dont_search	=	' -rapidshare'\
				' -torrent'\
				' -site:*wire*.com'\
				' -site:*share*.com'\
				' -site:*torrent*.com'\
				' -site:abcmusic.net'\
				' -site:kazaa.com'\
				' -site:velocityreviews.com'\
				' -site:blog.ncday.net'

hot_bands = gethits()

###############################################################################
# bands that i know provide free music
###############################################################################
known_free =	['blink182',
				'Smashing Pumpkins',
				'Gregg Michael Gillis',
				'girl talk']

for bnd in known_free:
	hot_bands.append(bnd)

###############################################################################
# make the output file 'unique'
###############################################################################
file=open(os.path.expanduser('~/top40_' + str(int(time.time())) + '.txt'),'w')

###############################################################################
# Google only accepts 32 search parameters
###############################################################################
test_list = search + dont_search
makeList = 0

if len(test_list.split()) >= 31:
	print "Google's search parameter limit (31) reached or exceeded"
	sys.exit
	
for band in hot_bands:
	band = '"' + band + '"'
	print 'getting ready to search for band: ' + band
	
	try:
		gs = GoogleSearch(search + band + dont_search, random_agent=True)		
		gs.results_per_page = 25 # can also be 25 or 100
		rand = random.randint(0,1000) # adjust for experiment
		print 'sleeping for ' + str(rand) + ' seconds...'
		time.sleep(rand)
	except:
		traceback.print_exc()
	try: 
		results = gs.get_results()
	except:
		print 'moving on',band
		traceback.print_exc()
		continue
	
	print "searching: ",band
	count = 0
	counter = 0

	for res in results:
		try:
			title = res.title.encode("utf8")
			url = res.url.encode("utf8") 
			if count == 0:
				file.write(':artist: __<b>' + band.strip('"') + '</b>__\n')
				count += 1
			if makeList == 0:
				file.write('<ul>\n')
				makeList += 1
			file.write('<li><a href="' + str(url) + '"' + 'target="_blank">' +
					   str(title) + '</a>\n')
			counter += 1
			if counter == 5: # I only want the top five hits 
				file.write('</ul>\n')
				makeList = 0
				# Force write to disk, in order to view output in real time.
				file.flush()
				os.fsync(file)
				break
		except:
			print traceback.print_exc()

file.close()

