import datetime
import json
import os
import ya_disk
import vk


if __name__ == '__main__':
    now = datetime.datetime.now()
    present_day = now.strftime('_%Y-%m-%d')

    with open('vk_token.txt', 'r') as file_object:
        vk_token = file_object.read().strip()
    with open('ya_token.txt', 'r') as file_object:
        ya_token = file_object.read().strip()

    ya_disk = ya_disk.YandexDisk(token=ya_token)
    vk_user = vk.VkUser(vk_token, '5.131')
    
    user = 'begemot_korovin'  # input('Input VK user id: ')
    folder = '/diplom_basic'  # input('Input new folder name: ')
    photo_dict = vk_user.photo_get(user)
    photos_stats = []
    counter = 0
    path = ya_disk.create_folder(folder + present_day)
    for name, url in photo_dict.items():
        cur_photo = {}
        counter += 1
        ya_disk.upload_to_disk(url, path + '/' + name)
        ya_disk.load_photo(url, name)
    #     ya_disk.upload_file_to_disk('/diplom_basic/' + name, name)
        print(f'{counter}/{len(photo_dict)} completed')
        size = '{:.3f}'.format(os.stat(name).st_size / 1024)
        cur_photo['file_name'], cur_photo['size'] = name, str(size) + ' Kb'
        photos_stats.append(cur_photo)
        os.remove(name)
    with open('photos_uploaded.json', 'w') as f:
        json.dump(photos_stats, f, indent=2)
