import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import re
from itranslate import itranslate as itrans
import lyricsgenius as lg
from langdetect import detect
from private import CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN
import asyncio
import aiohttp

# This is for using Spotify and Genius APIs. I am getting secret tokens from another file as requested
# Since this is very old project of mine, I did not use async. For async, there is another API down below (disify).

auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = sp.Spotify(auth_manager=auth_manager)
genius = lg.Genius(ACCESS_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)
eng_turk_dict = dict()

def get_song_info(song_name_artist):
    artist = song_name_artist.split('-')[0]
    song_name = song_name_artist.split('-')[1]

    try:
        searchResults = spotify.search(q="artist:" + artist + " track:" + song_name, type="track")
    except searchResults["tracks"]["items"] == []:
        return 1, 2
    except:
        return 3,4
    
    searchResults = searchResults["tracks"]["items"][0]
    track_info =[[searchResults["album"]["name"],\
                       searchResults["artists"][0]["name"],\
                       searchResults['name'], \
                       searchResults["album"]["release_date"], \
                       searchResults['uri']]]
                      
    Song_DF = pd.DataFrame(track_info, columns=["Album_Name", "Artist_Name", "Song_Name", "Release_Date", "Uri"])
    print("********************************Song Info********************************")
    print("\n")
    last_artist_name, last_song_name = searchResults["artists"][0]["name"], searchResults['name']
    print(Song_DF)
    return last_artist_name, last_song_name

def get_lyrics(artist, song_name):
    try:
        lyrics = genius.search_song(song_name, artist).lyrics
    except:
        return None
    return lyrics

def translate_lyrics(song_name):
    new_artist_name, new_song_name = get_song_info(song_name)
    if new_artist_name == 1 and new_song_name == 2:
        return "The song could not found"
    elif new_artist_name == 3 and new_song_name == 4:
        return "Connection has lost! Please try again"

    lyrics_list = list()
    
    replace_dict = {'s':'is', 'd':'would', 've':'have', 'm':'am', 't':'not', 're':'are', 'll':'will', 'don':'do'}
    
    lang_words = []
    lang_dest_words = list()
    
    # getting lyrics
    lyrics = get_lyrics(new_artist_name, new_song_name)
    if lyrics == None:
        return "Lyrics can not be found..."
    print("********************************Lyrics********************************")
    print(lyrics)
    print("********************************Translations********************************")
    
    # adding lyrics to an array after splitting
    for i in lyrics.split("\n"):
        if i != '':
            i = i.lower()
            i = re.sub("[^a-zA-Z]", ' ', i)
            lyrics_list.append(i)
#     print(lyrics_list)

    #print(TextBlob(lyrics_list[0]).detect_language)
    
    if detect(lyrics_list[0]) != 'en':
        return "Please select English songs!"
    
    # adding words to an array word by word
    for i in lyrics_list:
        i = i.split(" ")
        for j in i:
            if j.startswith("(") or j.endswith(")"):  
                j = j.replace("(", "")
                j = j.replace(")", "")
            if j in replace_dict.keys(): j = j.replace(j, replace_dict[j])

            if j == "the" or j in lang_words or j == '': continue
                
            if j in eng_turk_dict.keys():
                #print("j = ", j, "eng_turkde vardı")
                lang_words.append(j)
                lang_dest_words.append(eng_turk_dict[j])
            else:
                #print("j = ", j, "elseye girdi")
                word = itrans(j, from_lang='en', to_lang='tr')
                eng_turk_dict[j] = word
                lang_words.append(j)
                lang_dest_words.append(word)

    # creating a dataframe with the original words and their tranlastions
    pd.set_option('display.max_rows', None)
    keys = ["turkish", "english"]
    values = [lang_dest_words, lang_words]
    
    lang2lang_dest_words = pd.DataFrame(columns=keys)
    
    for i, j in zip(keys, values): lang2lang_dest_words[i] = j
        

    print(lang2lang_dest_words)
    #return lang2lang_dest_words, eng_turk_dict
    return eng_turk_dict

async def check_email(email):
    async with aiohttp.ClientSession() as session:
        url = 'https://www.disify.com/api/email/' + email
        async with session.get(url) as response:
            if response.status != 200:
                raise aiohttp.ClientResponseError(response.status, message=f"Unexpected status code {response.status}")
            data = await response.json()
            print(f"Is e-mail disposable: {data.get('disposable')}")

translate_lyrics("Adele-Set Fire to the Rain")

print("\n******************************************************\n")
email = "350227@uwr.edu.pl"
asyncio.run(check_email(email))