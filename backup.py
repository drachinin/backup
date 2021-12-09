import requests
import os
from pprint import pprint


class BackUp:

    def __init__(self, owner_id, token):
        self.token = token
        self.owner_id = owner_id

    def get_photos(self, owner_id):
        print('Getting photos.')
        params = {
            'album_id': 'profile',
            'owner_id': self.owner_id,
            'extended': '1'
        }
        url = f'https://api.vk.com/method/photos.get?access_token=958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008&v=5.131'
        response = requests.get(url, params=params).json()
        photos_info = []
        os.mkdir('photos')
        for i in response['response']['items']: 
            photo_url = i['sizes'][-1]['url']      
            likes = i['likes']['count']
            size = i['sizes'][-1]['type']
            if f'{likes}.jpg' in photos_info:
                likes = f'{likes}_{i["date"]}'
            photos_info.append({"file_name" : f'{likes}.jpg', "size" : size})
            r = requests.get(photo_url)
            with open(f'photos/{likes}.jpg', 'wb') as f:
                f.write(r.content)
        print('Photos uploaded to computer.')
        pprint(photos_info)

    def get_upload_link(self, file, token):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        params = {'path': file, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self):
        self.get_photos(self.owner_id)
        print('Uploading photos to Yandex Disk...')
        for file in os.listdir('photos'):
            href = self.get_upload_link(file, self.token).get('href')
            response = requests.put(href, data=open(f'photos/{file}', 'rb'))
        print('Photos uploaded to Yandex Disk.')


if __name__ == '__main__':
    owner_id = input('Введите id пользователя: ')
    token = input('Введите токен Яндекс.Диска: ')    
    uploader = BackUp(owner_id, token)
    result = uploader.upload()