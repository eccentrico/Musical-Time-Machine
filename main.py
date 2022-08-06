import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests
CLIENT_SECRET="ca914c9edca34eecaaf18a8da9b7c330"
CLIENT_ID="a3a31aaa9f59472aab8d15b91a474661"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]



date=input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response=requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}").text
soup=BeautifulSoup(response,"html.parser")
songs1=soup.select("li > h3")
list=[song.getText()for song in songs1]
new_list=[cupid.strip("\n\t") for cupid in list[0:100]]
song_names = new_list

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist=sp.user_playlist_create(user=user_id,name=f"{date} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"],items=song_uris)



