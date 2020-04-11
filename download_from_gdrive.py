# download google drive file with url and relevant file id 
# Example: 
# URL = https://drive.google.com/u/0/uc?id=1PItmDj7Go0OBnC1Lkvagz3RRB9qdJUIG&export=download
# file_id = 1PItmDj7Go0OBnC1Lkvagz3RRB9qdJUIG
#  
# Source: https://stackoverflow.com/a/39225039

import requests


def download_file_from_google_drive(URL, id, destination):

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    # URL = "https://docs.google.com/uc?export=download"
    # id = '1PItmDj7Go0OBnC1Lkvagz3RRB9qdJUIG'
    # URL = "https://drive.google.com/u/0/uc?id=1PItmDj7Go0OBnC1Lkvagz3RRB9qdJUIG&export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)
    print('file is downloaded')


if __name__ == "__main__":
    import sys

    url     = "https://drive.google.com/u/0/uc?id=1PItmDj7Go0OBnC1Lkvagz3RRB9qdJUIG&export=download"
    file_id = "1PItmDj7Go0OBnC1Lkvagz3RRB9qdJUIG"
    
    if len(sys.argv) is not 2:
        print("Usage: python download_from_gdrive.py destination_file_path")
    else:
        # DESTINATION FILE ON YOUR DISK
        destination = sys.argv[1]
        download_file_from_google_drive(url, file_id, destination)
