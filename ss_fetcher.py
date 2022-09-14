from google_play_scraper import app
import json
import requests
import os

apps_data = [
    {
        "title": "Video Converter",
        'output_folder': 'video_converter',
        "package": "com.inverseai.video_converter"
    },
    {
        "title": "Shatkora - E-Commerce",
        'output_folder': 'shatkora',
        "package": "com.shatkora.app"
    },
    {
        "title": "Video Compressor",
        'output_folder': 'video_compressor',
        "package": "com.video_converter.video_compressor"
    },
    {
        "title": "Video Merger",
        'output_folder': 'video_merger',
        "package": "com.video_joiner.video_merger"
    },
    {
        "title": "Imaage Compressor",
        'output_folder': 'image_compressor',
        "package": "com.inverseai.image_compressor"
    },
    {
        "title": "Video Downloader",
        'output_folder': 'video_downloader',
        "package": "inverseai.downloader.videodownloader"
    },

]


def save_image(url, output):
    img_data = requests.get(url).content
    with open(output, 'wb') as handler:
        handler.write(img_data)


def append_content_to_file(file, content, clear=False):
    if clear:
        open(file, "w").close()
    with open(file, "a") as myfile:
        myfile.write(content)


def generate_app_section(title, icon, rating, download, screenshots, short_description):
    img_content = ""
    for ss in screenshots:
        img_content = img_content + \
            f"""<img src="{ss}" width="150"/>  """
    content = f"""
<img class="iconImage" src="{icon}" style="border-radius: 5px;width: 100px;height: 100px;">
<h1>{title}</h1>
 <p style="font-size: 16px;">👉 <b>{rating}</b> User ratings</p>
<p style="font-size: 16px;">👉 <b>{download}</b> installs</p>
<p>{short_description}</p> 

{img_content}
__________________________________________________________________________________________
<br> 
"""
    return content


def get_app_details(data):
    return generate_app_section(data['title'], data['icon'], data['rating'], data['downlaod'],
                                data['screenshots'], data['short_description'])


destination = "test.md"
append_content_to_file(destination, "", True)
jsonData = {
    'apps': []
}
for entry in apps_data:
    print(f"start updating app {entry['title']}")
    title = entry['title']
    package = entry['package']
    output_folder = f"images/{entry['output_folder']}"
    result = app(
        package,
        lang='en',  # defaults to 'en'
        country='us'  # defaults to 'us'
    )
    images = result['screenshots']
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    save_image(result['icon'], f'{output_folder}/icon.jpg')

    c = 0
    for image in images:
        save_image(image, f'{output_folder}/img_{c}.jpg')
        c = c+1

    rating = result['score']
    rating_count = result['ratings']
    download = result['installs']
    app_url = result['url']
    short_description = result['summary']
    icon = f"{output_folder}/icon.jpg"
    screenshots = []
    for i in range(0, c):
        screenshots.append(f'{output_folder}/img_{i}.jpg')
    desc = {
        'icon': icon,
        'title': title,
        'rating': rating,
        'rating_count': rating_count,
        'downlaod': download,
        'short_description': short_description,
        'url': app_url,
        'screenshots': screenshots
    }

    jsonData["apps"].append(desc)

    app_section = get_app_details(desc)

    append_content_to_file(destination, app_section, False)

    print(f"End updating app {title} saved in {output_folder}")
# append the styles
# append_content_to_file(destination, get_style_content(), False)
append_content_to_file("portfolio.json", json.dumps(jsonData), True)
# with open('scapper_output.json', 'w', encoding='utf-8') as f:
#     json.dump(result, f, ensure_ascii=False, indent=4)
# print("Fetch Complete")
