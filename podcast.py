from dataclasses import dataclass
import os
import requests
import xml.etree.ElementTree as ET
import json
from tqdm import tqdm

PODCAST_SUBSCRIPTION_FILE = "./subscriptions.json"

@dataclass
class Podcast:
    title: str
    feed_url: str
    folder_path: str

    def __iter__(self):
        yield 'title', self.title
        yield 'feed_url', self.feed_url
        yield 'folder_path', self.feed_url

    def __eq__(self, other):
        return self.title == other.title and self.feed_url == other.feed_url and self.folder_path == other.folder_path

@dataclass
class Episode:
    title: str
    file: str
    url: str

    def __iter__(self):
        yield 'title', self.title
        yield 'file', self.file
        yield 'url', self.url

    def __eq__(self, other):
        return self.title == other.title and self.file == other.file and self.url == other.url

#*
# Searches new episodes in all podcasts and writes them to file
# *#
def search_for_new_episods_of_podcast(podcast: Podcast) -> None:

    xml = requests.get(podcast.feed_url).text

    with open('feed.xml', 'w') as f:
        f.write(xml)

    tree = ET.parse('feed.xml')
    root = tree.getroot()

    fetched_episodes: list[Episode] = []

    for item in root.findall('./channel/item'):
        title = item.find('title').text
        file = title.lower().replace(" ", "_").replace("ö", "oe").replace("ä", "ae").replace("ü", "ue").replace(".", "").replace("ß", "ss")
        url = item.find('enclosure').attrib["url"]
        fetched_episodes.append(Episode(title, file + ".mp3", url))

    saved_episodes = read_episodes_json(podcast.folder_path)
    episodes_to_save = saved_episodes

    for episode in fetched_episodes:
        if episode not in saved_episodes:
            os.system(f'notify-send "Found new episode ({episode.title}) of podcast {podcast.title} | Downloading..."')
            print("Found episode which not yet been saved: " + episode.title)
            if download_and_save_episode(episode, podcast.folder_path):
                episodes_to_save.append(episode)
                write_episodes_json(episodes_to_save, podcast.folder_path)
                os.system(f'notify-send "Finished downloading episode {episode.title}"')

#*
# Function which writes a list of episodes to a file
# *#
def write_episodes_json(episodes: list[Episode], podcast_saves_folder: str) -> None:  
    with open(podcast_saves_folder + "/episodes.json", "w") as ef:
        converted = list(map(lambda episode: dict(episode), episodes))
        ef.write(json.dumps(converted))


#*
# Reads a list of episodes from the same file as above
# *#
def read_episodes_json(podcast_saves_folder: str) -> list[Episode]:
    if not os.path.exists(podcast_saves_folder):
        print("Episode folder does not exist yet. Creating it...")
        os.mkdir(podcast_saves_folder)
    
    if not os.path.exists(podcast_saves_folder + "/episodes.json"):
        print("File episodes.json does not exist yet.")
        return []

    with open(podcast_saves_folder + "/episodes.json", "r") as ef:
        raw_json = ef.read()
        try:
            podcasts_dicts = json.loads(raw_json)
            return list(map(lambda dic: Episode(dic["title"], dic["file"], dic["url"]), podcasts_dicts))
        except:
            return []

def read_subscriptions_json(path: str) -> list[Podcast]:
    print("Reading subscriptions from file.")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        array_of_podcasts = json.loads(content)
        podcasts = map(lambda p: Podcast(p["title"], p["feed_url"], p["folder_path"]), array_of_podcasts)
        return podcasts
    


def download_and_save_episode(episode: Episode, path: str) -> bool:
    print("Downloading episode: " + episode.title)
    response = requests.get(episode.url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(path + "/" + episode.file, "wb") as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)

    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("Somthing went wrong with the download.")
        return False

    print("Finished download")
    return True

if __name__ == "__main__":
    for podcast in read_subscriptions_json(PODCAST_SUBSCRIPTION_FILE):
        search_for_new_episods_of_podcast(podcast)