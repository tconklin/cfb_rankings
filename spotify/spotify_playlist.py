import numpy as np #import required libraries/modules
import os
import matplotlib.pyplot
import math
import json
import urllib2

#rank: entire phrase by 1
#rank: half phrase by 0.5
#rank: third of phrase by 0.333
#rank: subsequent by a/L
#alpha*n_tracks + beta*sum((length-m_length)/n)**2
def word_count(phrase):
    """
input: phrase (multiple words)
output: phrases (break down of phrase chunks between 2-half_words)
example p = word_count("the truth will set you free)
p = 
['the+truth+will+set+you+free',
 'the+truth+will+set',
 'the+truth+will',
 'set+you+free',
 'the+truth',
 'will+set',
 'you+free']
    """
    phrase = phrase.replace(' ', '+') #replaces all spaces with + signs...this is the format spotify requires
    n_words = 1
    s_phrase = len(phrase)
    b_word = [0]
    e_word = []
    for j in range(s_phrase): #finds the beginning and ends of words based on where the spaces are
        if phrase[j] == '+':
            n_words += 1
            b_word.append(j+1)
            e_word.append(j)
    e_word.append(s_phrase)
    phrases = [phrase]
    for k in range(int(np.floor(n_words/2)+1),1,-1): #constructs a list of possible phrases you can make
        #print k
        l_phrase = np.floor(n_words/2.)
        counter = int(np.floor(n_words/k))
        for j in range(counter):
            phrases.append(phrase[b_word[k*j]:e_word[k*(j+1)-1]])
    return phrases

def get_json(phrase):
    """
Searches Spotify's track list for the input phrase. Returns relevant song information: song name, song length, artist, popularity, and url
input: phrase
output: song name, song length, artist, popularity, and url
example: song_name, song_length, artist, popularity, url = get_json("I'm+gonna+get+free")
    """
    url = 'http://ws.spotify.com/search/1/track.json?q='+phrase #searches spotify for a specific phrase
    url_json = urllib2.urlopen(url)
    song_list = json.load(url_json)
    n_songs = min(song_list["info"]["num_results"],100) #gets only the results from the first page
    song_names = ["" for x in range(n_songs)] #preallocates space for song_names, length etc
    song_length = np.zeros(n_songs)
    song_url = ["" for x in range(n_songs)]
    song_popularity = np.zeros(n_songs)#["" for x in range(n_songs)]
    artist_names = ["" for x in range(n_songs)]
    song_artist = ["" for x in range(n_songs)]
    for j in range(n_songs): #sets the values for song_names, length etc
        #print j, n_songs
        song_names[j] = song_list["tracks"][j]["name"]
        song_length[j] = song_list["tracks"][j]["length"]
        song_url[j] = song_list["tracks"][j]["href"]
        song_popularity[j] = song_list["tracks"][j]["popularity"]
        artist_names[j] = song_list["tracks"][j]["artists"][0]["name"]
        song_artist[j] = song_names[j]+", "+artist_names[j]
    return song_names, song_length, song_url, song_popularity, artist_names, song_artist

def coefficients(tot_songs,u_length):
    """
input: expected number of songs, vector of lengths
output: alpha, beta
example alpha,beta = coefficients(10,[200,300,250,220,200,100,300,250,320,120,220,230,210])
alpha = 38.25, beta=1.0
    """
    beta = 1. #finds the expected alpha and beta values for a total number of songs and a vector of lengths
    var_length = np.std(u_length)
    alpha = beta*(var_length/float(tot_songs))**2. #rearranging the equation, taking the derivative, and solving for 0 (function minimum will occur when dx/dy = 0)
    return alpha, beta

def spotify_poetry(phrase, alpha=2.5, beta=1, tot_songs=50, wt=1.):
    """
creates an output file of song urls, song names, and artist names using a weighted ranking of outputs of
"phrase". To limit the number of songs set alpha and beta (2.5,1 is roughly 50 songs) OR tot_songs. To
assign less weight to matches that meet less of the phrase, adjust weight from 0 (equal) to any positive
value.
input: phrase, alpha, beta, total songs (only if alpha or beta are not set), weight
output: unique song name, song length, song url, weighted song popularity, artist name, chi square values, phrase
outfile1: phrase.txt --> spotify url
outfile2: phrase_ivy.txt --> song name, artist name
example: sn, sl, su, sp, an, chis, p = spotify_poetry("the truth will set you free",alpha=2.5,beta=1,tot_songs=50, wt=1.)
    """
    phrases = word_count(phrase) #gets the possible phrases that can be made out of "phrase"
    if not os.path.exists('/home/tim/spotify'):
        os.mkdir('/home/tim/spotify')
    outfile = '/home/tim/spotify/'+phrase.replace(' ','_')+'.txt' #creates the outfile for the spotify urls
    outfile_ivy = '/home/tim/spotify/'+phrase.replace(' ','_')+'_ivy.txt' #creates the outfile for the spotify urls
    n_phrases = np.size(phrases)
    n_rows = np.zeros((n_phrases))
    song_name = [] #sets variables to an empty array
    song_length = []
    song_url = []
    song_popularity = []
    artist_name = []
    song_artist = []
    for j in range(n_phrases):
        print phrases[j]
        weight = len(phrases[j])/float(len(phrases[0])) #how similar the current phrase is to the original phrase
        sn, sl, su, sp, an, sa = get_json(phrases[j]) #get song name, etc
        song_name = np.append(song_name, sn, axis=0)
        song_length = np.append(song_length, sl, axis=0)
        song_url = np.append(song_url, su, axis=0)
        song_popularity = np.append(song_popularity, sp*weight**wt, axis=0) #set weighted popularity
        artist_name = np.append(artist_name, an, axis=0)
        song_artist = np.append(song_artist, sa, axis=0)
    u_songs = np.unique(sa) #gets only unique song names
    n_songs = np.size(sn)
    n_u_songs = np.size(u_songs)
    u_length = np.zeros(n_u_songs)
    u_url = u_songs.copy()
    u_url = np.array(u_url,dtype='<U73') #sets data type of array to >> than needed for the url
    u_popularity = np.zeros(n_u_songs)
    u_aname = u_songs.copy()
    for j in range(n_songs): #find unique songs in song list
        for k in range(n_u_songs):
            if sa[j] == u_songs[k]: #find the popularity of the song if theres a match
                #if u_popularity[k] <= song_popularity[j]: #override the old parameters with the new parameters and increase the rating
                    u_popularity[k] += song_popularity[j]
                    u_length[k] = song_length[j]
                    u_url[k] = 'http://open.spotify.com/track/'+song_url[j][14:]
                    u_aname[k] = artist_name[j]
    rating_order = np.argsort(-u_popularity) #ratings, ascending order
    u_songs = u_songs[rating_order] #song order
    u_length = u_length[rating_order]
    u_url = u_url[rating_order]
    u_popularity = u_popularity[rating_order]
    u_aname = u_aname[rating_order]
    if not alpha or not beta: #if the coefficients don't exist, set them
        alpha,beta = coefficients(tot_songs,u_length)
    else:
        chis = np.zeros(n_u_songs)+np.inf #set the array value to infinite (to exclude the first 5 songs)
        for j in range(5,n_u_songs):
            chis[j] = alpha*(j+1)+beta*np.sum(np.std(u_length[:j]))**2./float(j) #get the chi squared value
    min_chis = np.argsort(chis)[0] #find where chi square is a minimum
    np.savetxt(outfile,u_url[0:min_chis],fmt='%s',delimiter=', ') #saves the URLs of the songs (up to the spot where chi square is minimum)
    np.savetxt(outfile_ivy,u_songs[0:min_chis],fmt='%r',delimiter=', ') #saves the URLs of the songs (up to the spot where chi square is minimum)
    return u_songs[:min_chis], u_length[:min_chis], u_url[:min_chis], u_popularity[:min_chis], u_aname[:min_chis],chis,phrase
