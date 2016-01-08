# gmusic-import
A basic script for importing songs from a csv to your Google Play Music library. Definitely a work in progress!

Heavily dependent on the awesome <a target="_blank" href="https://github.com/simon-weber/gmusicapi">gmusicapi</a> library (which in turn has its own dependencies, so definitely take a look before running).

## A few notes:

1. Built when I realized there was no easy way to import my Rdio library to Google Music<br/>
2. I used it to successfully add over 13,000 songs to my library from my Rdio collection (took about 30-45 minutes)<br/>
3. Requires that you have a Google Play Music subscription (formerly Google Music All Access I believe)<br/>
4. Built to import from a local csv file containing track name, artist, album name, and track number (but can be easily modified)<br/>

## How it works:

1. Update the username and password variables in the gmusic-import-script.py file (you'll also need to generate an app specific password)
2. Point the script at a local csv file containing all the tracks you'd like to add to your library (look at <a href="https://github.com/suihanki/gmusic-import/blob/master/example.csv">example.csv</a> for formatting (run ```python gmusic-import-script.py name-of-your-csv-file.csv```)
3. The script will first search the Google Play Music catalogue for each row in your csv, and attempt to find matches
4. Once it processes the entire csv, it will let you know how many matches it found, and ask if you'd like to import (if you like you can exit the script at this point and look at the matched_tracks.csv to see what it found)
5. Next it will add each track to your library by ID
	<li>At the end you should have:<br/>
		<strong>matched_tracks.csv</strong> with all your matches<br/>
		<strong>no_matches.csv</strong> with songs we couldn't find (it's formatted perfectly so that you can retry import at a later date)<br/>
		<strong>library_track_list.csv</strong> with a list of Google Play Music track IDs and track names that we imported (so you can delete what you uploaded if you make a mistake, I haven't built any deletion capabilities yet)<br/>
	</li>

## A few gotchas:

1. It won't necessarily add an entire album to your library if you don't have all the songs listed in your CSV (would be simpler to just find the album and add that but gmusicapi doesn't support that and also I'm pretty picky sometimes about which tracks I add :)<br/>
2. Could definitely use better error catching/logging...<br/>
3. Probably not very efficient (brute forced my way through figuring out how to do different types of loose/exact matching)<br/>
