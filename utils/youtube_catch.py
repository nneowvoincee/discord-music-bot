import http
import yt_dlp.utils
from yt_dlp import YoutubeDL

import config
import asyncio

async def url_catch(url):   # search by url
    with YoutubeDL(config.ytdl_options) as ydl:
        loop = asyncio.get_event_loop()
        try:
            results = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
            result = {'platform': 'ytb',
                      'title': results['title'],
                      'uploader': results['uploader'] if 'uploader' in results else '',
                      'duration': results['duration_string'] if 'duration_string' in results else '',
                      'url': results['url']}

        except http.client.InvalidURL:
            return 'Invalid url'
        except yt_dlp.utils.ExtractorError as e:
            if "Unsupported URL" in str(e):
                return 'Unsupported URL'
            else:
                return 'Extract fail'
        except:
            return 'Other error'

    return result


async def query_catch(search_query, numOfResult=5):   # search by keyword
    with YoutubeDL(config.ytdl_options) as ydl:
        arg = f"ytsearch{numOfResult}:" + search_query
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, lambda: ydl.extract_info(arg, download=False))

    info_list = []
    for each in results['entries']:
        if 'duration_string' not in each:
            continue
        info_list.append({
            "url": each['url'],
            "title": each['title'],
            "channel": each['uploader'],
            "duration": each['duration_string']
        })

    return info_list

if __name__ == '__main__':
    asyncio.run(url_catch('https://www.youtube.com/watch?v=5aN-yk6kGsk', None))
