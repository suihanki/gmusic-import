import csv
from gmusicapi import Mobileclient
import string
import sys

username = 'example@example.com'
app_password = '123456'

api = Mobileclient()
api.login(username, app_password, Mobileclient.FROM_MAC_ADDRESS)
# => True

matched_track_list = []
no_match_track_list = []
library_track_list = []

def importGmusic(inputFileName):
	error_count = 0
	with open(inputFileName, 'r') as inputFile:
		csvfile = csv.reader(inputFile, delimiter=',', quotechar='"')
		for line in csvfile:
			if error_count > 3:
				break
			if line == ['Name', 'Artist', 'Album', 'Track Number']:
				continue
			else:
				lower_case_line = [line[0].lower(), line[1].lower(), line[2].lower(), line[3].lower()]
				try:
					response = api.search_all_access(lower_case_line[0].decode('utf-8')+" "+lower_case_line[2].decode('utf-8')+" "+lower_case_line[1].decode('utf-8'))
				except:
					error_count += 1

				if response['song_hits']:
					match_result = _find_matches(lower_case_line, response['song_hits'])
					if match_result:
						matched_track_list.append(match_result)
				else:
					response = api.search_all_access(lower_case_line[0].decode('utf-8')+" "+lower_case_line[1].decode('utf-8'))
					if response['song_hits']:
						match_result = _find_matches(lower_case_line, response['song_hits'])
						if match_result:
							matched_track_list.append(match_result)
					else:
						# truly no matches
						no_match_track_list.append(line)
						print ('No match found :( - '+line[0]+' / '+line[1])

	inputFile.close()
	if matched_track_list:
		print ("Num of matches: "+str(len(matched_track_list)))
		_create_csv_output(matched_track_list,'matched_tracks.csv',csvtype='matches')
		user_input = raw_input("Proceed with import of matched tracks? y/n: ")
		if user_input == 'y':
			_add_tracks_to_library(matched_track_list)

	if no_match_track_list:
		print ("No matches found: "+str(len(no_match_track_list)))
		_create_csv_output(no_match_track_list,'no_match_tracks.csv',csvtype='nomatches')


def _find_matches(line, track_hits):
	for match_type in ['exact','loose','looser','loosest']:
		for song in track_hits:
			i = 0
			song_list = [song['track']['title'].encode('utf-8').lower(),
						 song['track']['artist'].encode('utf-8').lower(),
						 song['track']['album'].encode('utf-8').lower(),
						 str(song['track']['trackNumber']),
						 song['track']['nid']]
			
			if match_type == 'exact':
				# match Track Name, Artist, and Album
				if song_list[0:2] == line[0:2]:
					print ('Found match: "'+line[0]+'" / "'+song_list[0]+'"')
					return(_parse_track_info(line, song_list))

			if match_type == 'loose':
				# match Track Name, Album
				if song_list[0] == line[0] and song_list[2] == line[2]:
					print ('Found match: "'+line[0]+'" / "'+song_list[0]+'"')
					return(_parse_track_info(line, song_list))

			if match_type == 'looser':
				# match Track Name, Artist
				if song_list[0:1] == line[0:1]:
					print ('Found match: "'+line[0]+'" / "'+song_list[0]+'"')
					return(_parse_track_info(line, song_list))

			if match_type == 'loosest':
				# match Artist, Album
				if song_list[1:2] == line[1:2]:
					print ('Found match: "'+line[0]+'" / "'+song_list[0]+'"')
					return(_parse_track_info(line, song_list))
				else:
					i += 1
					if i > 4:
						no_match_track_list.append(line)
						print ('No match found :( - '+line[0]+' / '+line[1])
						return None


def _parse_track_info(line, song_list):
	track_info = dict()
	track_info['name'] = song_list[0]
	track_info['artist'] = song_list[1]
	track_info['album'] =  song_list[2]
	track_info['track_number'] = song_list[3]
	track_info['z_original_track_name'] = line[0]
	track_info['z_original_track_artist'] = line[1]
	track_info['z_original_track_album'] = line[2]
	track_info['z_original_track_number'] = line[3]
	track_dict = dict()
	track_dict[song_list[4]] = track_info

	return track_dict


def _create_csv_output(track_list, csvname, csvtype=None):
	with open(csvname, 'wb') as outputFile:
		csvobject = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		if csvtype == 'matches':
			csvobject.writerow(['track name','track artist','track album','track number',
								'original track name','original track artist','original track album',
								'original track number'])

			for track in track_list:
				track_id = str(track.keys()[0])
				track_info = track.get(track_id)
				csvobject.writerow([track_info['name'],track_info['artist'],track_info['album'],
								   str(track_info['track_number']),track_info['z_original_track_name'],
								   track_info['z_original_track_artist'],track_info['z_original_track_album'],
								   track_info['z_original_track_number']])
		
		if csvtype == 'nomatches':
			csvobject.writerow(['Name','Artist','Album','Track Number'])

			for track in track_list:
				csvobject.writerow(track)
		
		if csvtype == 'library':
			csvobject.writerow(['library_track_id','name'])

			for track in track_list:
				csvobject.writerow(track)

		outputFile.close()


def _add_tracks_to_library(matched_track_list):
	failed_count = 0
	for track in matched_track_list:
		try:
			library_track_id = api.add_aa_track(track.keys()[0])
			track_info_match = track.get(track.keys()[0])
			library_track_list.append([track.keys()[0],track_info_match['name']])
		except:
			failed_count += 1

	_create_csv_output(library_track_list,'library_track_list.csv',csvtype='library')
	print ('Added: '+str(len(library_track_list))+' / Failed: '+str(failed_count))


def main(argv):
    inputFileName = argv[0]
    importGmusic(inputFileName)

if __name__ == "__main__":
   main(sys.argv[1:])