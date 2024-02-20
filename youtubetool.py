
import os
from urllib.request import urlopen
import json
from dotenv import load_dotenv
import aiohttp
import asyncio
import requests
import concurrent.futures

#provide API key here
load_dotenv()
YOUTUBE_API_KEY = os.getenv("youtube_api_key")

channel_id = 'UCEWpbFLzoYGPfuWUMFPSaoA'
keywords = "law of indices"
# channel_name_list = [ 'The Organic Chemistry Tutor']
# channel_id_list = ['UCX6b17PVsYBQ0ip5gyeme-Q', 'UCEWpbFLzoYGPfuWUMFPSaoA']
# channel_name_list = ['CrashCourse', 'The Organic Chemistry Tutor']


def channelid(ans):
    #to eliminate spaces between search queries with %20
    str1='%20'.join([str(ele) for ele in ans])
    #Use yt API to give search results for username
    site1=urlopen('https://www.googleapis.com/youtube/v3/search?part=snippet&q='+str1 +'&type=channel&key='+YOUTUBE_API_KEY)
    #loads data to a json file format
    a1 = json.load(site1)
    #to get channelid and channelname using username
    ucid=str(a1.get("items")[0].get("id").get('channelId'))
    channelname=a1.get("items")[0].get("snippet").get('title')
    #returns channelid & channelname
    return(ucid,channelname)



async def search_videos(api_key, channel_id, keywords):
    """Search for videos in specific channels with keywords.
    Parameters needed: youtube api key, channel_id, keyword.
    Returns a tuple containing the video title and URL.
    """
    base_url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'type': 'video',
        'q': keywords,
        'maxResults': 1,  # You can adjust this number
        'key': api_key
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            response_json = await response.json()

            # Check if 'items' is empty or not present
            if not response_json.get('items'):
                print("No items found in response:", response_json)
                return None  # Or handle the empty case as appropriate

            # Assuming 'items' is not empty and contains the expected structure
            video_id = response_json['items'][0]['id']['videoId']
            video_title = response_json["items"][0]['snippet']['title']
            video_url = f"https://www.youtube.com/embed/{video_id}"

            video = (video_title, video_url)
            return video



