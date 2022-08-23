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


def get_style_content():
    content = ''' 
     <style>
        .appContainer {
            padding: 12px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
            transition: 0.3s;
            margin-left: auto;
            margin-right: auto;
            border-radius: 8px;
            max-width: 1200px;
            margin-top: 16px;
        }

        .header {
            display: flex;
            width: 100%;
            padding: 0;
            text-align: center;
            margin: 12px
        }

        .iconImage {
            border-radius: 5px;
            width: 100px;
            height: 100px;
        }

        .ss-container {
            display: flex;
            gap: 5px;
            margin: 0 20px;
            width: 100%;
            flex-direction: row;
            justify-content: space-around;
        }

        .img-container {
            flex: 1;
            width: 100px;
            border-radius: 5px;
            transition: all 0.5s ease-in-out;
        }

        .ss-image {
            width: 100%;
            border-radius: 5px;
            overflow: hidden;

        }

        .img-container:hover {
            transform: scale(2.0);
            z-index: 4;
        }

        .keys {
            margin: 12px 0;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .keys p {
            font-size: 16px;
        }

        .short-description {
            opacity: 0.6;
            font-size: 16px;
            margin: 12px 0;
        }
    </style>
    '''
    return content


def generate_app_section(title, icon, rating, download, screenshots, short_description):
    img_content = ""
    for ss in screenshots:
        img_content = img_content + \
            f"""
             <div class="img-container">
                <img class="ss-image" src="{ss}"/>
            </div>\n
             """
    content = f"""
        <div class="appContainer">
            <div class='header'>
                <img class="iconImage" src={icon} />
                <h1 style="margin-left:12px;margin-top:40px;text-align:center;cursor:pointer;">
                    <a>{title}</a>
                </h1>
            </div>
            <div class='info'>
                <div class="keys">
                    <p>👉 <b>{rating}</b> User ratings</p>
                    <p>👉 <b>{download}+</b> installs</p>
                </div>
                <div style="display:flex;gap:5px;justify-content:space-around;">
                    {img_content}
                </div>
                <p class='short-description'>
                    {short_description}
                </p>
            </div>
            </div> 
    """
    return content


def get_app_details(data):
    return generate_app_section(data['title'], data['icon'], data['rating'], data['downlaod'],
                                data['screenshots'], data['short_description'])


destination = "test.html"
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
append_content_to_file(destination, get_style_content(), False)
append_content_to_file("portfolio.json", json.dumps(jsonData), True)
# with open('scapper_output.json', 'w', encoding='utf-8') as f:
#     json.dump(result, f, ensure_ascii=False, indent=4)
# print("Fetch Complete")
