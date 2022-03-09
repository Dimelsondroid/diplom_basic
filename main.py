import datetime
import json
import os
import ya_disk
import vk
from pprint import pprint

def log_write(data):
    with open('log.txt', 'a', encoding='utf-8') as log:
        log.write(data + '\n')


def current_date_time():
    now = datetime.datetime.now()
    present_day = now.strftime('_%Y-%m-%d')
    current_time = now.strftime('%d-%m-%Y, %H:%M:%S')
    return present_day, current_time


if __name__ == '__main__':
    photos_stats = []
    counter = 0

    vk_token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    # with open('vk_token.txt', 'r') as file_object:
    #     vk_token = file_object.read().strip()

    # ya_token = ''
    with open('ya_token.txt', 'r') as file_object:
        ya_token = file_object.read().strip()

    ya_disk = ya_disk.YandexDisk(token=ya_token)
    vk_user = vk.VkUser(vk_token, '5.131')

    user = 'begemot_korovin'  # input('Input VK user id: ')
    folder = '/diplom_basic'  # input('Input new folder name: ')
    present_day, current_time = current_date_time()
    photo_dict, vk_log = vk_user.photo_get(user)
    logging = [current_time, vk_log]
    log_write(', '.join(logging))

    present_day, current_time = current_date_time()
    path, path_log = ya_disk.create_folder(folder)
    logging = [current_time, path_log]
    log_write(', '.join(logging))

    for name, params in photo_dict.items():
        cur_photo = {}
        counter += 1

        ya_upload_log = ya_disk.upload_to_disk(params[0], path + '/' + name)
        print(f'{counter}/{len(photo_dict)} completed')
        upload_count_log = f'{counter}/{len(photo_dict)} completed'
        present_day, current_time = current_date_time()
        logging = [current_time, ya_upload_log, upload_count_log]
        log_write(', '.join(logging))
        size = params[1]
        cur_photo['file_name'], cur_photo['size'] = name, str(size)
        photos_stats.append(cur_photo)

    with open('photos_uploaded.json', 'w') as f:
        json.dump(photos_stats, f, indent=2)
