import requests, os, pathlib

# image_path = 'https://www.ahnegao.com.br/wp-content/uploads/2020/09/MEME-2-14.jpg'
image_path = os.path.join(r'D:\arquivo\Projetos\Software\deepdream-tool\imagens\download.jpg')
directory_path = pathlib.Path(r'D:\arquivo\Projetos\Software\deepdream-tool\imagens')
api_key = '2972167e-46f4-4660-8c35-538f065ccc70'
mode = 'local'
iterations = 2
images_in_folder = []

for root, subdirs, files in os.walk(directory_path):
    for file in files:
        p = pathlib.Path(root, file)
        images_in_folder.append(p)

def dreamify(mode, image_path, api_key):
    r = requests.post(
        "https://api.deepai.org/api/deepdream",
        data={
            'image': (open(str(image_path), 'rb') if mode == 'local' else str(image_path)),
        },
        headers={'api-key': str(api_key)}
    )
    print(r.json())
    return r.json()['output_url']

def dreamify_loop(iterations, mode, image_path, api_key):
    for i in range(iterations): 
        image_path = dreamify(mode, image_path, api_key)
        print(i,":", image_path)
    return(image_path)

# map(lambda x: dreamify_loop(iterations, mode, (directory_path / x), api_key), images_in_folder,)

# print(list(map(lambda x: dreamify_loop(iterations, mode, x, api_key), images_in_folder,)))
# print(list(map(lambda x: print(iterations, mode, x, api_key), images_in_folder,)))
print(dreamify_loop(iterations, mode, image_path, api_key))