import requests
r = requests.post(
    "https://api.deepai.org/api/deepdream",
    data={
        'image': 'https://www.ahnegao.com.br/wp-content/uploads/2020/09/MEME-2-14.jpg',
        # 'image': open('/path/to/image.jpg', 'rb'),
    },
    headers={'api-key': '2972167e-46f4-4660-8c35-538f065ccc70'}
)

new_image_iteration = r.json()['output_url']

for i in range(10):
    r = requests.post(
    "https://api.deepai.org/api/deepdream",
    data={
        'image': str(new_image_iteration),
        # 'image': open('/path/to/image.jpg', 'rb'),
    },
    headers={'api-key': '2972167e-46f4-4660-8c35-538f065ccc70'}
    )
    new_image_iteration = r.json()['output_url']
    print(r.json())

print(new_image_iteration)