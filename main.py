import requests, os, argparse
parser = argparse.ArgumentParser()

parser.add_argument("-img", "--image-url", dest="image_path", help="Image url")
parser.add_argument("-d", "--directory-path", dest="directory_path", help="Image path")
parser.add_argument("-a", "--api-key", dest="api_key", help="API key")
parser.add_argument("-it", "--iterations", dest="iterations", help="Number of iterations", type=int)

args = parser.parse_args()

image_path = args.image_path
directory_path = args.directory_path
api_key = args.api_key
iterations = args.iterations
mode = 'local' if directory_path else 'remote'

def download_images_to_folder(urls, filenames):
    for url, filename in zip(urls, filenames):
        filename = filename.split('.')
        filename = ('_dream.').join(filename)
        r = requests.get(url, allow_redirects=True)
        if not os.path.exists('dream'):
            os.mkdir('dream')
        open(os.path.join(r'dream', filename), 'wb').write(r.content)

def get_images_from_folder(folder):
    images_in_folder = []
    for root, subdirs, files in os.walk(folder):
        for file in files:
            images_in_folder.append(file)
    return images_in_folder

def dreamify(mode, image_path, api_key):
    if mode == 'local':
        r = requests.post(
            "https://api.deepai.org/api/deepdream",
            files={
                'image': open(str(image_path), 'rb'),
            },
            data={
                'image': str(image_path),
            },
            headers={'api-key': str(api_key)}
        )
    elif mode == 'remote':
        r = requests.post(
            "https://api.deepai.org/api/deepdream",
            data={
                'image': str(image_path),
            },
            headers={'api-key': str(api_key)}
        )
    try:
        return r.json()['output_url']
    except:
        return r.json()

def dreamify_loop(mode, image, api_key, iterations=1):
    for iteration in range(iterations): 
        image = dreamify(mode, image, api_key)
        mode = 'remote'
        print(f'{iteration} iteration: {image}')
    return(image)

if mode == 'local':
    images_to_process = get_images_from_folder(directory_path)
    dreamified_images_urls = list(map(lambda x: dreamify_loop(mode, (os.path.join(directory_path, x)), api_key, iterations), images_to_process))
    download_images_to_folder(dreamified_images_urls, images_to_process)
elif mode == 'remote':
    image_to_process = image_path
    dreamified_image_url = dreamify_loop(mode, image_to_process, api_key, iterations)
    download_images_to_folder([dreamified_image_url], ["image.jpg"])