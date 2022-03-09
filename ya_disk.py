import requests


class YandexDisk:
    url = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = self.url + '/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def _get_upload_link(self, ya_disk_path):
        upload_url = self.url + '/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': ya_disk_path, 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, ya_disk_path, disk_file_path):
        href = self._get_upload_link(ya_disk_path=ya_disk_path).get('href', '')
        response = requests.put(href, data=open(disk_file_path, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Info: Upload successful ', end='')

    def upload_to_disk(self, url, ya_disk_path):
        upload_url = self.url + '/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': ya_disk_path, 'url': url, 'overwrite': 'true'}
        req = requests.post(upload_url, headers=headers, params=params)
        log = ''
        if req.status_code == 202:
            print('Upload successful ', end='')
            log = 'Info: Upload successful ' + str(req)
        elif req.status_code == 503:
            print('Service is temporary unavailable')
            log = 'Error: Service is temporary unavailable ' + str(req)
        return log

    def load_photo(self, url, file_name):
        response = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(response.content)

    def create_folder(self, folder):
        folder_url = self.url + '/v1/disk/resources'
        headers = self.get_headers()
        params = {'path': folder}
        req = requests.put(folder_url, headers=headers, params=params)
        log = ''
        if req.status_code == 201:
            print('Folder created')
            log = 'Info: Folder created ' + str(req)
        elif req.status_code == 409:
            print('Folder already exist')
            log = 'Info: Folder already exist ' + str(req)
        return folder, log
