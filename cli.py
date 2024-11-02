import argparse

parser = argparse.ArgumentParser(
    prog="PyPodcastSync",
    description="PyPodcastSync is a programm which automatically downloads subscribte podcasts."
)

parser.add_argument("-u", "--feed-url", help="The url of the podcast feed file.")
parser.add_argument("-s" "--sub-file", help="Podcast subscription file.")

args = parser.parse_args()
