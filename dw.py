import shutil

import requests

url = 'https://bolivia.respuestaciudadana.org/index.html#!'
response = requests.get(url, stream=True)
with open('img.png', 'wb') as out_file:
       shutil.copyfileobj(response.raw, out_file)
del response
