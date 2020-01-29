import requests
from io import open as iopen


pic_url= "https://images.craigslist.org/00707_hkZFU3Kj0gX_600x450.jpg"

with open('pic5.jpg', 'wb') as handle:
    r = requests.get(pic_url, stream=True)
    print("attempting download...")
    if not r.ok:
        print(r)

    for block in r.iter_content(1024):
        if not block:
            break

        handle.write(block)
print(handle)

'''

 
def fetch_image(img_ur, save_filename):
    img = requests.get(img_ur)
    if img.status_code == 200:
        with iopen(save_filename, 'wb') as f:
            f.write(img.content)
    else:
        print('Received error: {}'.format(img.status_code))
 
testlink = 'https://commons.wikimedia.org/wiki/File:Relstandard.gif'
 
filename = 'Goldilocks3.jpg'
fetch_image(testlink, filename)
'''