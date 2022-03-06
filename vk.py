import requests
import time
import datetime

now = datetime.datetime.now()
present_day = now.strftime('_%Y-%m-%d')


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def _get_user_id(self, user_id):
        user_search_url = self.url + 'users.get'
        user_search_params = {
            'user_id': user_id
        }
        req = requests.get(user_search_url, params={**self.params, **user_search_params}).json()['response'][0]['id']
        time.sleep(1)
        return req

    def photo_get(self, user_id):
        user_ident = self._get_user_id(user_id)
        photo_url = self.url + 'photos.get'
        photo_params = {
            'user_id': user_ident,
            'album_id': 'profile',
            'extended': '1'
        }
        photo_dict = {}
        req_photo = requests.get(photo_url, params={**self.params, **photo_params}).json()['response']['items']
        for photo in req_photo:
            max_size = max(photo['sizes'], key=lambda x: x['height'])
            if str(photo['likes']['count']) + '.jpg' in photo_dict.keys():
                photo_dict[str(photo['likes']['count']) + present_day + '.jpg'] = max_size['url']
            else:
                photo_dict[str(photo['likes']['count']) + '.jpg'] = max_size['url']
        return photo_dict
