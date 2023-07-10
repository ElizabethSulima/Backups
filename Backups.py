import logging
import requests
import os
import json
from conf import token_vk

logging.basicConfig(level=logging.INFO, filename="py_log.log", format="%(asctime)s %(levelname)s %(message)s")
logging.debug("A DEBUG message")
logging.info("A INFO")
logging.warning("A WARNING")
logging.error("An ERROR")
logging.critical("A message a level CRITICAL severity")

class Photos_VK:
    def __init__(self, token):
        self.token = token
    def get_photos_items(self, offset=0, count=5):
        url_vk = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': user_ids,
            'album_id': 'profile',
            'access_token': token_vk,
            'v': '5.131',
            'extended': 1,
            'photo_sizes': 1,
            'offset': offset,
            'count': count
        }
        response = requests.get(url=url_vk, params=params).json()
        res = response['response']['items']
        return res

    def get_photos_(self):
        all_photo_count = self.get_photos_items()
        photos = []
        max_sizes_photos = {}

        if not os.path.exists(f'C:/Users/Lenovo/Desktop/photos_users_vk'):
            os.mkdir(f'C:/Users/Lenovo/Desktop/photos_users_vk')

        for photo in all_photo_count:
            photos_info = {}
            for size in photo['sizes']:
                if size['type'] == 'z':
                    if photo['likes']['count'] not in max_sizes_photos.keys():
                        max_sizes_photos[photo['likes']['count']] = size['url']
                        photos_info['file_name'] = f"{photo['likes']['count']}.jpg"
                    else:
                        max_sizes_photos[f"{photo['likes']['count']} + {photo['date']}"] = size['url']
                        photos_info['file_name'] = f"{photo['likes']['count']}_{photo['date']}.jpg"
                photos_info['size'] = size['type']
            photos.append(photos_info)

        for ph_name, ph_url in max_sizes_photos.items():
            with open('photos_users_vk/%s' % f'{ph_name}.jpg', 'wb') as file:
                image = requests.get(ph_url)
                file.write(image.content)

        with open('photos.json', 'w') as f:
            json.dump(photos, f, indent=2)

class Yandex_Disk:
    def __init__(self, token):
        self.token = token

    def folder_creation(self):
        url_ya = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers_ya = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {user_token_ya}'}
        params_ya = {
            'path': f'{folder_name}',
            'overwrite': 'false'}
        response_folder = requests.put(url=url_ya, headers=headers_ya, params=params_ya)

    def ya_disk_upload(self, path_to_file: str):
        url_ = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params_ = {
            'path': f'{folder_name}/{file_name}',
            'overwrite': 'true'
        }
        headers_ = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {user_token_ya}'
        }
        response = requests.get(url_, headers=headers_, params=params_)
        url_for_upload = response.json().get('href', '')
        upload = requests.put(url_for_upload, data=open(path_to_file, 'rb'), headers=headers_)

user_ids = str(input(f'Введите id пользователя Vk: '))
photo_download = Photos_VK(token_vk)
photo_download.get_photos_()

user_token_ya = str(input(f'Введите свой токен Я.Диска: '))
yandex_upload = Yandex_Disk(user_token_ya)

folder_name = str(input('Введите имя папки на Яндекс диске для сохранения фото: '))
yandex_upload.folder_creation()

photos_list = os.listdir('photos_users_vk')
for photo in photos_list:
    file_name = photo
    files_path = os.getcwd() + '\photos_users_vk\\' + photo
    result = yandex_upload.ya_disk_upload(files_path)