# gmusic-import
A basic script for importing songs from a csv to your Google Play Music library. Definitely a work in progress!

Heavily dependent on the awesome <a target="_blank" href="https://github.com/simon-weber/gmusicapi">gmusicapi</a> library.

A few notes:

*Built when I realized there was no easy way to import my Rdio library to Google Music<br/>
*I used it to successfully add over 13,000 songs to my library from my Rdio collection (took about 30-45 minutes)<br/>
*Requires that you have a Google Play Music subscription (formerly Google Music All Access I believe)<br/>
*Built to import from a local csv file containing track name, artist, album name, and track number (but can be easily modified)<br/>

How it works:

<ol>
	<li>Point the script at a local csv file containing all the tracks you'd like to add to your library (look at <a href="#">example.csv</a> for formatting</li>
	<li>The script will first search the Google Play Music catalogue for each row in your csv, and attempt to find matches</li>
	<li>Once it processes the entire csv, it will let you know how many matches it found, and ask if you'd like to import (if you like you can exit the script at this point and look at the matched_tracks.csv to see what it found)</li>
	<li>Next it will add each track to your library by ID</li>
	<li>At the end you should have:<br/>
		matched_tracks.csv with all your matches<br/>
		no_matches.csv with songs we couldn't find (it's formatted perfectly so that you can retry import at a later date)<br/>
		library_track_list.csv with a list of Google Play Music track IDs and track names that we imported (so you can delete what you uploaded if you make a mistake, I haven't built any deletion capabilities yet)<br/>
	</li>
</ol>

A few gotchas:

*It won't necessarily add an entire album to your library if you don't have all the songs listed in your CSV (would be simpler to just find the album and add that but gmusicapi doesn't support that and also I'm pretty picky sometimes about which tracks I add :)<br/>
*Could definitely use better error catching/logging...<br/>
*Probably not very efficient (brute forced my way through figuring out how to do different types of loose/exact matching)<br/>
