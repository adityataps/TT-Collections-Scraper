import csv
import os
import json
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup

def extract_tiktok_links(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('a', href=True)
    tiktok_data = []  # using a list to maintain order
    processed_links = set()  # to avoid duplicates

    for link in links:
        href = link['href']
        if 'https://www.tiktok.com/@' in href and ('/video/' in href or '/photo/' in href):
            username = '@' + href.split('@')[1].split('/')[0]  # include @ symbol
            alt_text = link.find('img', alt=True)['alt'] if link.find('img', alt=True) else ''
            sound = ''
            name = ''
            if 'created by' in alt_text[-200:]:
                sound_index = alt_text[-200:].index('created by')
                name_part = alt_text[-200:][sound_index + 10:]
                with_index = name_part.find(' with ')
                if with_index != -1:
                    name = name_part[:with_index].strip()
                    sound = name_part[with_index + 6:].strip()
                    sound = f"original sound—{name}"

                alt_text = alt_text[:-200] + alt_text[-200:][:sound_index]

            video_id = href.split('/')[-1]

            try:
                video_id_int = int(video_id)
                unix_timestamp = video_id_int >> 32
                date_est = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc).astimezone(timezone(timedelta(hours=-5)))
                date_est_formatted = date_est.strftime('%a %b %d %Y %H:%M:%S')
            except ValueError:
                unix_timestamp = ''
                date_est_formatted = ''

            if href not in processed_links and username and (alt_text or sound):
                tiktok_data.append({
                    'Video/Post ID': video_id,
                    'Date (UNIX timestamp)': unix_timestamp,
                    'Date (EST)': date_est_formatted,
                    'Name': name,
                    'Username': username,
                    'Description': alt_text,
                    'Sound Name': sound,
                    'Link': href
                })
                processed_links.add(href)

    file_dir = os.path.dirname(file_path)
    csv_file_path = os.path.join(file_dir, 'html_page_metadata.csv')
    json_file_path = os.path.join(file_dir, 'html_page_metadata.json')

    print(f"CSV file will be saved at: {csv_file_path}")
    print(f"JSON file will be saved at: {json_file_path}")

    # Write to CSV
    with open(csv_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Video/Post ID',
            'Date (UNIX timestamp)',
            'Date (EST)',
            'Name',
            'Username',
            'Description',
            'Sound Name',
            'Link'
        ])
        for row in tiktok_data:
            writer.writerow([
                row['Video/Post ID'],
                row['Date (UNIX timestamp)'],
                row['Date (EST)'],
                row['Name'],
                row['Username'],
                row['Description'],
                row['Sound Name'],
                row['Link']
            ])

    # Write to JSON with ensure_ascii=False
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(tiktok_data, file, indent=4, ensure_ascii=False)

# Prompt the user to enter the file path
file_path = input("Please enter the path to the HTML file: ")
extract_tiktok_links(file_path)
