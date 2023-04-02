import requests
import json
import pyfzf

#apiurl = "https://api.consumet.org"
#apiurl = "https://api.animxeast.eu.org"
#apiurl = "https://entertainment-scrapper.vercel.app"
#apiurl = "https://c.delusionz.xyz"
#apiurl = "https://apiconsumetorg-1.forsyth47.repl.co"
apiurl = "https://api.haikei.xyz"
moviename = str(input("Enter the Movie/TVSeries name: "))

def defsearch():
  urlsearch = apiurl + "/movies/flixhq/" + moviename
  responsesearch = requests.get(urlsearch, params={"page": 1})
  datasearch = responsesearch.json()
  resultsearch = datasearch['results']
  for i, resultidkvar in enumerate(resultsearch):
    print(f"{i + 1}. {resultidkvar['title']}")
  print()
  search_input = int(input("Enter the number of the title: "))
  movieid = resultsearch[search_input - 1]['id']

  if movieid.startswith("tv/"):
    movieidstripped = movieid[3:]
    urlmovie = apiurl + "/movies/flixhq/info?id=tv/" + movieidstripped
  else:
    movieidstripped = movieid[6:]
    urlmovie = apiurl + "/movies/flixhq/info?id=movie/" + movieidstripped
  responsemovie = requests.get(urlmovie)
  datamovie = responsemovie.json()
  print (datamovie["image"] + "\n"*2)
  print (datamovie["description"]  + "\n"*2)
  print ("Type: "+datamovie["type"])
  print ("Release Date: "+datamovie["releaseDate"])
  for i, idvaridk in enumerate(datamovie['episodes']):
    print(f"{i+1}. {idvaridk['title']}")
  print()
  ep_input = int(input("Enter the number of the episode: "))
  datamovieid = datamovie['episodes'][ep_input - 1]['id']

  urlep = apiurl + "/movies/flixhq/servers"
  responseep = requests.get(urlep, params={"episodeId": datamovieid, "mediaId": movieid})
  dataep = responseep.json()
  for i, episode in enumerate(dataep):
    print(f"{i+1}: {episode['name']}")
  print()
  link_input = int(input("Enter a Server (1/2/3/...): "))

  selected_url = dataep[link_input - 1]["name"]
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
#  for i, subtitlesidkvar in enumerate(subtitles):
    

defsearch()
