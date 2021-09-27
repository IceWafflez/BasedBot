import urllib.request
import re

search="test 2"
search = search.replace(" ","+")
print(search)
html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search)
video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
print("https://www.youtube.com/watch?v=" + video_id[0])