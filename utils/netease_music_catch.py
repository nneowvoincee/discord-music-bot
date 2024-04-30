import asyncio
import re

import requests
import pyncm_async
from pyncm_async import apis

import config
from utils import youtube_catch



async def song_catch(search_word, session): # search by keyword
    data = await apis.cloudsearch.GetSearchResult(search_word, limit=5, session=session)

    if data['code'] != 200:
        return data['code']
    elif data['result']['songCount'] <= 0:
        return None

    info = []
    for song in data['result']['songs']:
        title = song['name']
        duration = '{:02}:{:02}'.format(song['dt'] // 60000, (song['dt'] % 60000) // 1000)
        uploader = '/'.join([ar_data['name'] for ar_data in song['ar']])

        if config.search_VIP_in_ytb and song['fee'] == 1:  # "fee == 1": vip required
            result = await search_in_youtube(' '.join([title, uploader]), song['dt'] // 1000)

            if result['flag']:
                info.append(result['data'])
                continue

        info.append({'platform': 'wyy',
                     'title': title,  # 歌名
                     'duration': duration,  # 歌曲时长
                     'uploader': uploader,  # 歌手1/歌手2/歌手3/...
                     'url': rf'http://link.hhtjim.com/163/{song["id"]}.mp3'})
    return info


async def user_catch(search_word, session): # search user by keyword
    data = await apis.cloudsearch.GetSearchResult(search_word, stype=apis.cloudsearch.USER, limit=1, session=session)
    # print(data)

    if data['result']['userprofileCount'] <= 0:
        return None

    user_data = data['result']['userprofiles'][0]
    user_data = {'nickname': user_data['nickname'],
                 'signature': user_data['signature'],
                 'avatarUrl': user_data['avatarUrl'],
                 'id': user_data['userId'],
                 'playlist': None}

    playlists_data = await apis.user.GetUserPlaylists(user_data['id'], session=session)
    # print(playlists_data)
    user_data['playlists'] = [{'name': each['name'],
                              'id': str(each['id'])} for each in playlists_data['playlist']]
    return user_data


async def playlists_catch(id, session): # get user's playlist
    pyncm_async.SetCurrentSession(session)
    songs_data = await apis.playlist.GetPlaylistInfo(id, total=True, limit=1000, session=session)
    tracks = songs_data['playlist']['tracks']
    if len(tracks) == 0:
        return None

    song_list = []
    task_list = {}
    count = 0
    for each in tracks:
        title = each['name']
        uploader = "/".join([author['name'] for author in each['ar']])
        duration = '{:02}:{:02}'.format(each['dt'] // 60000, (each['dt'] % 60000) // 1000)

        if config.search_VIP_in_ytb and each['fee'] == 1:  # "fee == 1": vip required, try to search the same song in YouTube
            task_list.update(
                {count: asyncio.create_task(search_in_youtube(' '.join([title, uploader]), each['dt'] // 1000))}
            )   # run in background to save time

        else:
            url = rf'http://link.hhtjim.com/163/{each["id"]}.mp3'
            song_list.append({'platform': 'wyy',
                              'title': title,
                              'uploader': uploader,
                              'duration': duration,
                              'url': url
                            })
        count += 1

    fail_count = 0
    for task_index in task_list.keys():
        result = await task_list[task_index]

        if result['flag']:
            song_list.insert(task_index - fail_count, result['data'])
        else:
            fail_count += 1

    return song_list


async def search_in_youtube(search_query, duration):    # search the song (need vip in netease) in youtube
    flag = False
    data = dict()

    result = requests.get("https://www.youtube.com/results?search_query=" + search_query).text
    search_results = re.findall(r"watch\?v=(\S{11}).*?([0-9]+:[0-9]+).*?watch\?v=", result)[:10]

    for result in search_results:  # result: (video_id, duration in "00:00" format)
        if abs(duration -
               (int(result[1][-2:]) + int(result[1].split(':')[0]) * 60)) < 5:  # 对比秒数
            data = await youtube_catch.url_catch(f'https://www.youtube.com/watch?v={result[0]}')
            flag = True
            break

    return {'flag': flag, 'data': data}
