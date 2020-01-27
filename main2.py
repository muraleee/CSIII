import requests


pic_url= "https://upload.wikimedia.org/wikipedia/commons/3/32/Relstandard.gif"
with open('pic1.jpg', 'wb') as handle:
        response = requests.get(pic_url, stream=True)
        print("attempting download...")
        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
print(handle)

'''
import requests
from io import open as iopen
 
def fetch_image(img_ur, save_filename):
    img = requests.get(img_ur)
    if img.status_code == 200:
        with iopen(save_filename, 'wb') as f:
            f.write(img.content)
    else:
        print('Received error: {}'.format(img.status_code))
 
testlink = 'https://vignette.wikia.nocookie.net/pdsh/images/9/95/Prettygoldilocks.jpg'
 
filename = 'Goldilocks.jpg'
fetch_image(testlink, filename)
'''