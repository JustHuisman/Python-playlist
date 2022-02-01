import sqlite3, sys

try:                 
    conn = sqlite3.connect(r'C:\Users\Just\Desktop\chinook.db') #Enter your own path to your downloaded Chinook database file here
    cur = conn.cursor()
    import_file = input ('Enter a name for a file to import from: ')
    
    with open(import_file, 'r') as f:                        
        unfiltered = f.read().splitlines()
        keywords = [filter_empty_lines for filter_empty_lines in unfiltered if filter_empty_lines]
                
except FileNotFoundError:
                sys.exit('File not found')
except PermissionError:
                sys.exit('No permission for this file')
except OSError:
                sys.exit('Cannot read out this file')

cur.execute('''SELECT playlists.PlaylistId, playlists.Name
               FROM playlists''')

playlists = cur.fetchall()
choose_playlist = input ('Enter a name for the playlist: ')
existing_playlists = False

for read_playlist in playlists:
    playlist_id = read_playlist[0]
    existing_playlists = read_playlist[1]
    if choose_playlist == read_playlist[1]:
        existing_playlists = True  
        break
                
if existing_playlists == True:                      
    sys.exit('This playlist already exists')
        
else:
    playlist_id += 1
    print('--- Start import from playlist ---')
    cur.execute('''INSERT INTO playlists
                   VALUES (?, ?)''', (playlist_id, choose_playlist))
    conn.commit()
    cur.execute('''UPDATE sqlite_stat1
                   SET stat = ?
                   WHERE sqlite_stat1.tbl = 'playlists' ''', (playlist_id,))
    conn.commit()
    
for keyword in keywords:
                cur.execute('''SELECT tracks.TrackId, tracks.Name, artists.Name
                               FROM tracks
                               INNER JOIN albums ON tracks.AlbumId = albums.AlbumId
                               INNER JOIN artists ON albums.ArtistId = artists.ArtistId
                               WHERE tracks.name LIKE (?||'%') ''', (keyword,))
                found_tracks = cur.fetchall()
              
                selection_menu = False
                for keyword in found_tracks:
                                track_id = keyword[0]
                                track_name = keyword[1]
                                artist_name = keyword[2]
                                                             
                                if len(found_tracks) == 1:
                                    cur.execute('''INSERT INTO playlist_track
                                                   VALUES (?, ?)''', (playlist_id, track_id))
                                    last_row = cur.lastrowid
                                    conn.commit()
                                if len(found_tracks) > 1:          
                                    selection_menu = True

                while selection_menu:
                    try:
                        print ('Choose from the following tracks: ')
                        for start, (track_id, track_name, artist_name) in enumerate(found_tracks, start=1):
                            print('{}\t{}\t{}'.format(start, track_name, artist_name))                        
                        choose_track = int(input('Your choice: '))

                        if choose_track in range(1, len(found_tracks)+1):
                            i = 0
                            for keyword in found_tracks:
                                track_id = keyword[0]
                                i += 1
                                if i == choose_track:
                                    break
  
                            cur.execute('''INSERT INTO playlist_track
                                           VALUES (?, ?)''', (playlist_id, track_id))
                            last_row = cur.lastrowid                
                            conn.commit()                              
                            break
                        print ('Choice not recognized. Enter a number from 1 to', len(found_tracks))
                        
                    except ValueError:
                        print ('Only enter numbers')
                        continue

cur.execute('''UPDATE sqlite_stat1
               SET stat = ?
               WHERE sqlite_stat1.tbl = 'playlist_track' ''', (last_row,))
conn.commit()

for keyword in keywords:
         
    cur.execute('''SELECT tracks.TrackId, tracks.Name, artists.Name
                 FROM tracks
                 INNER JOIN albums ON tracks.AlbumId = albums.AlbumId
                 INNER JOIN artists ON albums.ArtistId = artists.ArtistId
                 WHERE tracks.name LIKE (?||'%') ''', (keyword,))
    found_tracks = cur.fetchall()
    
    if len(found_tracks) == 0:
        print('--- No tracks found for ', keyword, ' ---')

print('--- Import from playlist complete ---')