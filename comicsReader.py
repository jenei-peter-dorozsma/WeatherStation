# This file is part of the WeatherStation project
# and is licensed under the MIT License. For more details,
# see the LICENSE file in the root directory of this project or visit
# https://github.com/jenei-peter-dorozsma/WeatherStation

import requests
import xml.etree.ElementTree as ET
import re
import urllib.request
from PIL import Image
import io


class ComicsReader:
    def __init__(self, **kwargs):
        # 'https://www.comicsrss.com/rss/flash-gordon.rss',
        # 'https://www.comicsrss.com/rss/office-hours.rss',
        # 'https://www.comicsrss.com/rss/suburban-fairy-tales.rss',
        # 'https://www.comicsrss.com/rss/phantom.rss',

        self.rss_urls = [
            'https://www.comicsrss.com/rss/garfield.rss',
            'https://www.comicsrss.com/rss/peanuts.rss',
            'https://www.comicsrss.com/rss/garfield.rss',
            'https://www.comicsrss.com/rss/life-on-earth.rss',
            'https://www.comicsrss.com/rss/little-moments-of-love.rss',
            'https://www.comicsrss.com/rss/garfield-classics.rss',
            'https://www.comicsrss.com/rss/adult-children.rss',
            'https://www.comicsrss.com/rss/wumo.rss'
        ]
        self.counter = -1

    def extract_src_url(self, source):
        img_src_pattern = r'<img[^>]+src="([^">]+)"'
        match = re.search(img_src_pattern, source)

        if match:
            img_src = match.group(1)
            return img_src
        else:
            return "No image"

    def get_rss_image(self):
        self.counter += 1
        if self.counter == len(self.rss_urls):
            self.counter = 0

        response = requests.get(self.rss_urls[self.counter])

        print(self.rss_urls[self.counter])
        if response.status_code != 200:
            return 'N/A'

        # Parse the RSS feed
        root = ET.fromstring(response.content)

        # Retrieve the latest comic entry
        channel = root.find('channel')
        if channel is not None:
            item = channel.find('item')
            if item is not None:
                comic_info = {
                    'title': item.find('title').text,
                    'link': item.find('link').text,
                    'published': item.find('pubDate').text,
                    'summary': item.find('description').text
                }

        comic_src = self.extract_src_url(comic_info['summary'])
        return comic_src

    def download_image(self, url, output_path, color_set):
        # Download the image from the URL
        response = urllib.request.urlopen(url)
        image_data = response.read()

        # Define the colors
        color1 = color_set[0]
        color2 = color_set[1]
        color3 = color_set[4]

        # Load the image data into a PIL Image object
        image = Image.open(io.BytesIO(image_data)).convert('RGBA')

        # Create a new image with the same size and RGBA mode
        new_image = Image.new('RGBA', image.size)

        # Define color thresholds
        threshold_dark = 85  # Adjust threshold for dark colors
        threshold_light = 170  # Adjust threshold for light colors

        # Process each pixel
        for x in range(image.width):
            for y in range(image.height):
                r, g, b, a = image.getpixel((x, y))

                if a < 128:  # Assuming low alpha means transparency
                    new_image.putpixel((x, y), color3)
                else:
                    brightness = (r + g + b) // 3
                    if brightness < threshold_dark:
                        # Dark colors are transparent
                        new_image.putpixel((x, y), color3)
                    elif brightness > threshold_light:
                        # Bright colors are primary ones
                        new_image.putpixel((x, y), color1)
                    else:
                        # Other colors are secondary ones
                        new_image.putpixel((x, y), color2)

        # Save the new image
        new_image.save(output_path, format='PNG')

    def refresh_image(self, color_set):
        next_image = self.get_rss_image()
        self.download_image(next_image, 'tmp/comics.png', color_set)


if __name__ == '__main__':
    cr = ComicsReader()
    image_url = cr.get_rss_image()
    image = cr.download_image(image_url, 'tmp/comics.png')
