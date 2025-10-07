import requests
from bs4 import BeautifulSoup
import csv

response = requests.get('https://www.letras.mus.br/mais-acessadas/')

best = BeautifulSoup(response.content, 'html.parser').find('ol', class_='top-list_mus --top')

csv_list = []

url = best.find('li').a['href']
i = 0
for music in best:
    i += 1
    url = music.a['href']
    response = requests.get("https://www.letras.mus.br"+url)
    content = BeautifulSoup(response.content, 'html.parser')

    song = content.find('h1', class_ = 'textStyle-primary').text
    artist = content.find('h2', class_ = 'textStyle-secondary').text
    lyrics = content.find('div', class_ = 'lyric-original')
    rank = content.find('div', class_ = 'head-info-exib').b.text
    
    lyrics_str = ''
    for line in lyrics.find_all(string=True):
        lyrics_str += line + ' '

    csv_list.append((song, artist, rank, lyrics_str))
    print(f'done scraping music {i}')
print('scraping completed')
collumns = ['song', 'artist', 'rank', 'lyrics']

with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(collumns)
    writer.writerows(csv_list) 