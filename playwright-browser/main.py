import json
import time

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        # Launch browser (equivalent to webdriver.Chrome())
        browser = p.chromium.launch(
            headless=False
        )  # Set headless=True to run without GUI
        page = browser.new_page()

        # Navigate to Instagram
        page.goto('https://www.instagram.com/instagram')

        soups = []
        previous_height = 0

        while True:
            # Scroll to bottom
            current_height = page.evaluate('document.body.scrollHeight')
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')

            # Wait for content to load
            time.sleep(5)

            # Get page content
            html = page.content()
            soups.append(BeautifulSoup(html, 'html.parser'))

            # Check if we've reached the bottom
            new_height = page.evaluate('document.body.scrollHeight')
            if new_height == current_height:
                break
            previous_height = current_height

        # Extract post URLs
        post_urls = []
        for soup in soups:
            anchors = soup.find_all('a', href=True)
            post_urls.extend(
                [
                    anchor['href']
                    for anchor in anchors
                    if anchor['href'].startswith(('/p/', '/reel/'))
                ]
            )

        unique_post_urls = list(set(post_urls))
        print(f'before: {len(post_urls)}, after: {len(unique_post_urls)}')

        # Process each post URL
        json_list = []
        query_parameters = '__a=1&__d=dis'

        for url in unique_post_urls:
            try:
                modified_url = (
                    f'https://www.instagram.com{url}?{query_parameters}'
                )
                page.goto(modified_url)

                # Wait for JSON content in <pre> tag
                page.wait_for_selector('pre', timeout=10000)
                pre_content = page.text_content('pre')

                # Parse JSON
                json_parsed = json.loads(pre_content)
                json_list.append(json_parsed)

            except Exception as e:
                print(f'Error processing URL {url}: {e}')

        # Process JSON data (same as original)
        all_urls = []
        all_dates = []

        for json_data in json_list:
            item_list = json_data.get('items', [])

            for item in item_list:
                date_taken = item.get('taken_at')

                # Handle carousel media
                carousel_media = item.get('carousel_media', [])
                for media in carousel_media:
                    image_url = (
                        media.get('image_versions2', {})
                        .get('candidates', [{}])[0]
                        .get('url')
                    )
                    if image_url:
                        all_urls.append(image_url)
                        all_dates.append(date_taken)
                        print('carousel image added')

                    video_versions = media.get('video_versions', [])
                    if video_versions:
                        video_url = video_versions[0].get('url')
                        if video_url:
                            all_urls.append(video_url)
                            all_dates.append(date_taken)
                            print('carousel video added')

                # Handle single images
                image_url = (
                    item.get('image_versions2', {})
                    .get('candidates', [{}])[0]
                    .get('url')
                )
                if image_url:
                    all_urls.append(image_url)
                    all_dates.append(date_taken)
                    print('single image added')

                # Handle videos
                video_versions = item.get('video_versions', [])
                if video_versions:
                    video_url = video_versions[0].get('url')
                    if video_url:
                        all_urls.append(video_url)
                        all_dates.append(date_taken)
                        print('video added')

        print(f'Total URLs collected: {len(all_urls)}')
        browser.close()


if __name__ == '__main__':
    main()
