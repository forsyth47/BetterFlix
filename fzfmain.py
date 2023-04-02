import requests
import json
import pyfzf
import os
import mpv
fzf = pyfzf.FzfPrompt()
player=mpv.MPV()

#apiurl = "https://api.consumet.org"
#apiurl = "https://api.animxeast.eu.org"
#apiurl = "https://entertainment-scrapper.vercel.app"
#apiurl = "https://c.delusionz.xyz"
#apiurl = "https://apiconsumetorg-1.forsyth47.repl.co"
apiurl = "https://api.haikei.xyz"


print("""
      
$$$$$$$\             $$\     $$\                         $$$$$$$$\ $$\ $$\           
$$  __$$\            $$ |    $$ |                        $$  _____|$$ |\__|          
$$ |  $$ | $$$$$$\ $$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\  $$ |      $$ |$$\ $$\   $$\ 
$$$$$$$\ |$$  __$$\\_$$  _|\_$$  _|  $$  __$$\ $$  __$$\ $$$$$\    $$ |$$ |\$$\ $$  |
$$  __$$\ $$$$$$$$ | $$ |    $$ |    $$$$$$$$ |$$ |  \__|$$  __|   $$ |$$ | \$$$$  / 
$$ |  $$ |$$   ____| $$ |$$\ $$ |$$\ $$   ____|$$ |      $$ |      $$ |$$ | $$  $$<  
$$$$$$$  |\$$$$$$$\  \$$$$  |\$$$$  |\$$$$$$$\ $$ |      $$ |      $$ |$$ |$$  /\$$\ 
\_______/  \_______|  \____/  \____/  \_______|\__|      \__|      \__|\__|\__/  \__|
                                                                                     
      """)
print ("Recommended sever: [UPCLOUD/VIDCOULD]")
moviename = str(input("Enter the Movie/TVSeries name: "))
def defsearch():
  urlsearch = apiurl + "/movies/flixhq/" + moviename
  responsesearch = requests.get(urlsearch, params={"page": 1})
  datasearch = responsesearch.json()
  resultsearch = datasearch['results']
  search_input = fzf.prompt([f"{i + 1}. {result['title']}" for i, result in enumerate(resultsearch)])
  if search_input:
    search_input = int(search_input[0].split(".", 1)[0])
    print("You selected:", search_input)
  else:
    print("No movie title selected.")
  movieid = resultsearch[search_input - 1]['id']

  if movieid.startswith("tv/"):
    movieidstripped = movieid[3:]
    urlmovie = apiurl + "/movies/flixhq/info?id=tv/" + movieidstripped
  else:
    movieidstripped = movieid[6:]
    urlmovie = apiurl + "/movies/flixhq/info?id=movie/" + movieidstripped
  responsemovie = requests.get(urlmovie)
  datamovie = responsemovie.json()
  print (datamovie["description"]  + "\n"*2)
  print ("Type: "+datamovie["type"])
  print ("Release Date: "+datamovie["releaseDate"])
  movieid = fzf.prompt([f"{i + 1}. {episode['title']}" for i, episode in enumerate(datamovie['episodes'])])
  if movieid:
    movieid = int(movieid[0].split(".", 1)[0])
    print("You selected:", movieid)
  else:
    print("No Episode(s) selected.")
  datamovieid = datamovie['episodes'][movieid - 1]['id']

  urlep = apiurl + "/movies/flixhq/servers"
  responseep = requests.get(urlep, params={"episodeId": datamovieid, "mediaId": movieid})
  dataep = responseep.json()
  availservers = fzf.prompt([f"{i + 1}. {server['name']}" for i, server in enumerate(dataep)])
  if availservers:
    availservers = int(availservers[0].split(".", 1)[0])
    print("You selected:", availservers)
  else:
    print("No Server selected.")
  selected_url = dataep[availservers - 1]["name"]
  
  urllink = apiurl + "/movies/flixhq/watch"
  responselink = requests.get(urllink, params={"episodeId": datamovieid, "mediaId": movieid, "server": selected_url})
  datalink = responselink.json()
  sources = datalink['sources']
  subtitles = datalink['subtitles']

  for i, sourceidkvar in enumerate(sources):
    print("\n")
    print(f"Quality: {sourceidkvar['quality']}")
    print(f"isM3u8: {sourceidkvar['isM3U8']}")
    print(f"url: {sourceidkvar['url']}")
    print("\n")
    for subtitle in datalink["subtitles"]:
      if subtitle["lang"].startswith("English"):
        english_subtitle = subtitle["url"]
     
    
    
  print(f"url: {sourceidkvar['url']}")
  player.play(sourceidkvar['url'])
  

  lastseenurl = apiurl + f"/movies/flixhq/watch?episodeId={datamovieid}&mediaId={movieid}&server={selected_url}"
  print (lastseenurl)
  home_dir = os.path.expanduser("~")
  cache_dir = os.path.join(home_dir, ".cache", "Betterflix")
  if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
  data_file = os.path.join(cache_dir, "data.json")
  data = {"lastseenurl": lastseenurl}
  with open(data_file, "w") as f:
    json.dump(data, f, indent=4)

defsearch()
