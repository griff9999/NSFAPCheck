import os.path
import shutil
import tkinter
from tkinter import filedialog

from lyricsgenius import Genius
import music_tag
import glob

NSFAPwords = ["Shit", "shit", "fuck", "Fuck", "piss", "Piss", "Dick", "dick", "cunt", "Cunt", "Cock", "cock",
              " Tits ", " tits ", "Bitch ", "bitch "]
fileput = open("NSFAPsongs", "w")
fileput2 = open("Not_Found_Results.txt", "w")
genius = Genius("INSERT GENIUS API TOKEN HERE", timeout=120)
root = tkinter.Tk()
root.withdraw()
path = filedialog.askdirectory()
path = fr"{path}/**"
titles = []

for files in glob.glob(path, recursive=True):
    print(str(os.path.basename(files)))
    check = 0
    i = 0
    # Additional file types may be specified here, default is FLAC and mp3
    if files.endswith(".flac") or files.endswith(".mp3"):
        f = music_tag.load_file(files)
        artist_item = f["artist"]
        title_item = f["title"]
        does_genius_have_artist = genius.search_artist(str(artist_item), max_songs=0)
        # If artist does not exist on genius skip
        if does_genius_have_artist is not None:
            titles.append(str(title_item))
            song = Genius.search_song(genius, str(title_item), does_genius_have_artist.name)
            if song is not None:
                if song.artist != does_genius_have_artist.name:
                    # This means genius has returned a "best fit", but metadata artist and search artists don't match
                    # These tend to be transcripts, or other unrelated songs.
                    # Genius likely does not have the specifed song and/or artist in its database
                    # So it will be added to a list for manual review
                    song = "bad"
                    fileput2.writelines(str(title_item) + " by " + str(artist_item) + " could not be found\n")
                if song != "bad":
                    for words in NSFAPwords:
                        # If one NSFAP word has been detected, break to save time
                        if check == 1:
                            break
                        if NSFAPwords[i] in song.lyrics:
                            # If you are unable to move or delete files
                            #   uncommenting the following line will mark song as NSFAP in a txt
                            # fileput.writelines(str(title_item) + " by " + str(artist_item) + " is NSFAP\n")
                            # Attempt to move file to location, instead of outright deleting
                            try:
                                # Change C:\\ to desired file path location of NSFAP songs
                                # Example C:\\Users\\exampleuser\\Desktop\\NSFAP\\
                                shutil.move(files, "C:\\" + str(os.path.basename(files)), shutil.copy2)
                            except:
                                # Some files are returning erorrs, they will be marked in file instead of crashing
                                fileput.writelines(str(title_item) + " by " + str(artist_item)
                                                    + " IS NSFAP, BUT ENCOUNTERED AN ERROR\n")
                                check = 1
                                continue
                            check = 1
                            break
                        i = i + 1
                else:
                    continue
        else:
            continue
