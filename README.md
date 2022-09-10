# Podcast-Sync
A small script I wrote to automate the backup process of my favourite podcasts.

## Installation

### Dependencies

You need to have the following dependencies installed:

- Python 3

For Debian based Linux distros
```
sudo apt-get install python3
```
If you dont have Linux: Get Linux! (Notifications won't work on Windows or MacOS)

- Notify-Send
```
sudo apt-get install notify-send
```

- **tqdm**
```
pip3 install tqdm
```

- **requests**
```
pip3 install requests
```

### Configuration

1. Copy the skript somewhere, where it doesn't bother you.
2. Create a *subscription.json* file (you can of course choose your own file name) somewhere on you system containing your subscriptions in the following format

```
[
    {
        "title": "<the name of the podcast>",
        "feed_url": "<the url of the podcasts rss feed>",
        "folder_path": "<folder where the podcast will be saved>"
    }
]
```
3. Set the variable PODCAST_SUBSCRIPTION_FILE to the path of your *subscriptions.json* file
4. Run the script using
```
python3 podcast.py
```

5. (optional) You can create a cron job which automatically schedules the execution of the skript. I will provide a cron job in the future.