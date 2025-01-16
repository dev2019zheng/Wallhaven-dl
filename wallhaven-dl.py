########################################################
#        Program to Download Wallpapers from           #
#                  alpha.wallhaven.cc                  #
#                                                      #
#                 Author - Saurabh Bhan                #
#                                                      #
#                  Dated- 26 June 2016                 #
#                 Update - 11 June 2019                #
#         Update by dev2019zheng - 16 Jan 2025         #
########################################################

import os
import requests
import urllib.parse
import json

# Constants
FOLDER_NAME = 'Wallpapers'
API_KEY = "ryYyavZRvlFq0r2eHo88fGu9CDhEZCIn"

DOWNLOAD_URL = ""
# see https://wallhaven.cc/help/api for more information
BASE_API_URL = f"https://wallhaven.cc/api/v1/search?apikey={API_KEY}"
COOKIES = dict()

# Create directory if it doesn't exist
os.makedirs(FOLDER_NAME, exist_ok=True)
def get_category_tag():
    categories = {
        'all': '111', 'anime': '010', 'general': '100', 'people': '001',
        'ga': '110', 'gp': '101'
    }

    print('''
    ****************************************************************
                            Category Codes
    all     - Every wallpaper.
    general - For 'general' wallpapers only.
    anime   - For 'Anime' Wallpapers only.
    people  - For 'people' wallpapers only.
    ga      - For 'General' and 'Anime' wallpapers only.
    gp      - For 'General' and 'People' wallpapers only.
    ****************************************************************
    ''')
    category_code = input('Enter Category: ').lower()
    category_tag = categories.get(category_code, '111')
    
    return category_tag

def get_purity_tag():
    
    purities = {
        'sfw': '100', 'sketchy': '010', 'nsfw': '001',
        'ws': '110', 'wn': '101', 'sn': '011', 'all': '111'
    }
    print('''
    ****************************************************************
                            Purity Codes
    sfw     - For 'Safe For Work'
    sketchy - For 'Sketchy'
    nsfw    - For 'Not Safe For Work'
    ws      - For 'SFW' and 'Sketchy'
    wn      - For 'SFW' and 'NSFW'
    sn      - For 'Sketchy' and 'NSFW'
    all     - For 'SFW', 'Sketchy' and 'NSFW'
    ****************************************************************
    ''')
    purity_code = input('Enter Purity: ').lower()
    purity_tag = purities.get(purity_code, '100')

    return purity_tag

def get_top_range():
    valid_ranges = ['1d', '3d', '1w', '1M', '3M', '6M', '1y']
    topRange = input('Enter the range for toplist (1d, 3d, 1w, 1M, 3M, 6M, 1y): ')
    
    while topRange not in valid_ranges:
        print('Invalid range. Please enter a valid range.')
        topRange = input('Enter the range for toplist (1d, 3d, 1w, 1M, 3M, 6M, 1y): ')
    
    return topRange

def get_category_url():
    category_tag = get_category_tag()
    purity_tag = get_purity_tag()

    return f'{BASE_API_URL}&categories={category_tag}&purity={purity_tag}&page='

def get_latest_url():
    top_range = get_top_range()
    return f'{BASE_API_URL}&topRange={top_range}&sorting=toplist&page='

def get_search_url():
    query = input('Enter search query: ')
    return f'{BASE_API_URL}&q={urllib.parse.quote_plus(query)}&page='

def get_toplist_url():
    category_tag = get_category_tag()
    top_range = get_top_range()
    purity_tag = get_purity_tag()
    return f'{BASE_API_URL}&categories={category_tag}&purity={purity_tag}&topRange={top_range}&sorting=toplist&order=desc&page='

def download_page(page_id, total_images):
    url = DOWNLOAD_URL + str(page_id)
    print(f"Downloading url: {url}")
    response = requests.get(url, cookies=COOKIES)
    page_data = response.json().get("data", [])

    for i, image_data in enumerate(page_data):
        current_image = ((page_id - 1) * 24) + (i + 1)
        image_url = image_data["path"]
        filename = os.path.basename(image_url)
        file_path = os.path.join(FOLDER_NAME, filename)

        if not os.path.exists(file_path):
            img_response = requests.get(image_url, cookies=COOKIES)
            if img_response.status_code == 200:
                print(f"Downloading: {filename} - {current_image} / {total_images}")
                with open(file_path, 'wb') as image_file:
                    for chunk in img_response.iter_content(1024):
                        image_file.write(chunk)
            else:
                print(f"Unable to download {filename} - {current_image} / {total_images}")
        else:
            print(f"{filename} already exists - {current_image} / {total_images}")

def main():
    global DOWNLOAD_URL

    choice = input('''Choose how you want to download the image:
    Enter "category" for downloading wallpapers from specified categories
    Enter "latest" for downloading latest wallpapers
    Enter "toplist" for downloading top list wallpapers
    Enter "search" for downloading wallpapers from search
    Enter choice: ''').lower()

    while choice not in ['category', 'latest', 'search', 'toplist']:
        print('You entered an incorrect value.')
        choice = input('Enter choice: ').lower()

    if choice == 'category':
        DOWNLOAD_URL = get_category_url()
    elif choice == 'latest':
        DOWNLOAD_URL = get_latest_url()
    elif choice == 'toplist':
        DOWNLOAD_URL = get_toplist_url()
    elif choice == 'search':
        DOWNLOAD_URL = get_search_url()

    pages_to_download = int(input('How many pages do you want to download: '))
    total_images_to_download = 24 * pages_to_download
    print(f'Number of Wallpapers to Download: {total_images_to_download}')

    for page_index in range(1, pages_to_download + 1):
        download_page(page_index, total_images_to_download)

if __name__ == '__main__':
    main()
