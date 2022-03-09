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
        request = requests.get(user_search_url, params={**self.params, **user_search_params})
        req = request.json()['response'][0]['id']
        log = ''
        if request.status_code in ['1', '10']:
            print('Service is busy or unavailable, try later')
        # else:
        #     log = 'Info: Users.get request success ' + str(request)
        time.sleep(0.5)
        return req, request.status_code

    def photo_get(self, user_id):
        log = ''
        photo_dict = {}

        user_ident, user_get_log = self._get_user_id(user_id)
        if user_get_log in ['1', '10']:
            log = 'Error: Please try again later ' + str(user_get_log)
            return photo_dict, log
        photo_url = self.url + 'photos.get'
        photo_params = {
            'user_id': user_ident,
            'album_id': 'profile',
            'extended': '1'
        }

        req_photo = requests.get(photo_url, params={**self.params, **photo_params})

        if req_photo.status_code in ['1', '10']:
            print('Service is busy or unavailable, try again later')
            log = 'Error: Service is busy or unavailable, try again later ' + str(req_photo)
        else:

            for photo in req_photo.json()['response']['items']:
                max_size = max(photo['sizes'], key=lambda x: x['height'])
                if str(photo['likes']['count']) + '.jpg' in photo_dict.keys():
                    photo_dict[str(photo['likes']['count']) + present_day + '.jpg'] \
                        = [max_size['url'], str(max_size['height']) + 'x' + str(max_size['width']) + ' px']
                else:
                    photo_dict[str(photo['likes']['count']) + '.jpg'] \
                        = [max_size['url'], str(max_size['height']) + 'x' + str(max_size['width']) + ' px']
                log = 'Info: User found, photos requested'
        return photo_dict, log
