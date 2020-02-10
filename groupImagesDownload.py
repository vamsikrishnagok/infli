import requests
import json
import shutil


def download_photo(url):
    result = requests.get(url, stream=True)
    print(result)
    with open("media/" + url.split('/')[-1], 'wb') as out_file:
        shutil.copyfileobj(result.raw, out_file)
    del result

    return url.split('/')[-1]


BASE_URL = "https://api.flickr.com/services/rest/"
FLICKR_API_KEY = "33a183f2b958334e0ea92cd20f8bd6a6"
group_ids = ["16978849@N00", "34427469792@N01", "42097308@N00", "317988@N20"]
group_info = []
images_info = []
group_image = []
imageCount = 1
for k, group_id in enumerate(group_ids, 1):

    payload = {
        'method': 'flickr.groups.getInfo',
        'api_key': FLICKR_API_KEY,
        'group_id': group_id,
        'format': 'json',
        'nojsoncallback': 1
    }

    r = requests.get(BASE_URL, params=payload)

    name = r.json()["group"]['name']['_content']
    flickr_id = r.json()["group"]['id']
    member_count = r.json()["group"]['members']['_content']
    image_count = r.json()["group"]['pool_count']['_content']
    description = r.json()["group"]['description']['_content']

    group_info.append({
        "model": "apis.group",
        "pk": int(k),
        "fields": {
            "flickr_id": str(flickr_id),
            "name": str(name),
            "member_count": int(member_count),
            "image_count": int(image_count),
            "description": str(description).strip()
        }
    })
    with open('group.json', 'w+') as fp:
        json.dump(group_info, indent=4, fp=fp)

    payload = {
        'method': 'flickr.groups.pools.getPhotos',
        'api_key': FLICKR_API_KEY,
        'group_id': group_id,
        'format': 'json',
        'nojsoncallback': 1,
        'per_page': 500,
        'page': 1
    }
    r = requests.get(BASE_URL, params=payload)
    photo_ids = json.loads(r.content.decode('cp1252'))
    for i, photo_id in enumerate(photo_ids["photos"]["photo"], 1):
        payload = {
            'method': 'flickr.photos.getInfo',
            'api_key': FLICKR_API_KEY,
            'photo_id': photo_id["id"],
            'format': 'json',
            'nojsoncallback': 1,
            'per_page': 500,
            'page': 1
        }

        r = requests.get(BASE_URL, params=payload)
        photo = json.loads(r.content.decode('cp1252'))["photo"]
        url = 'https://farm' + str(photo['farm']) + '.staticflickr.com/' + str(photo['server']) + '/' + str(
            photo['id']) + '_' + photo['secret'] + '_b.jpg'

        image_name = download_photo(url)

        images_info.append(
            {
                "model": "apis.images",
                "pk": imageCount,
                "fields": {
                    "flickr_id": str(photo['id']),
                    "owner": "asdasd",
                    "title": photo['title']['_content'],
                    "image": image_name,
                    "secret": photo['secret'],
                    "farm": str(photo['farm']),
                    "server": str(photo['server']),
                    "description": photo['description']['_content'],
                    "comments_count": 0,
                    "views_count": 0}}
        )
        with open('images.json', 'w+') as fp:
            json.dump(images_info, indent=4, fp=fp)

        group_image.append({"model": "apis.groupimage", "pk": i, "fields": {"group": k, "image": imageCount}})

        with open('group_image.json', 'w+') as fp:
            json.dump(group_image, indent=4, fp=fp)

        imageCount = imageCount + 1
