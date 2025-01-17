# TikTok Collection Scraper

I cobbled together a fairly straightforward process to get your in-app collections out of TikTok with as much metadata as possible. This has worked nearly perfectly for a few thousand posts thus far.

## What this allows you to do:
- **Download** all the videos, photo slideshows (and their sounds) in a collection.
- **Rename** all the video files and folders of images to their post ID so they’re easier to manage.
- **Get metadata** on the posts in CSV and JSON files.

---

## Steps

### Step 1: Make your collections public on TikTok
1. Go to your collection in the TikTok app.
2. Click **"Make public"**.
3. Copy the link to it and send it to your desktop.  
   You usually need to be signed in on desktop to open it.

---

### Step 2: Scroll (slowly) all the way to the bottom of the page
- Don’t send TikTok too many requests at once; otherwise, you risk getting temporarily IP banned while signed in, which is bad.
- If you have over 1000 videos in your collection, I would recommend scrolling halfway and then coming back in half an hour to finish scrolling. Mimic semi-natural behavior and be careful.  
  > My VPN does not work at all at any step of this process, FYI.

---

### Step 3: Download the HTML contents of the page
1. Press `CMD + S` (on Mac).  
2. Select **"Web Page - Complete"** (Firefox).
 > Writing this documentation too quickly to show you how to do this on other browsers but this part is straightforward with any platform
---

### Step 4: Open the included Python files in VSCode
1. Install all dependencies first (via `pip` or however) into your Python environment:
   - [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) (I’m running 4.12.3)  
   - [yt-dlp](https://github.com/yt-dlp/yt-dlp) (I’m using 2025.01.15)  
   - [This fork of gallery-dl made by CasualYT31](https://github.com/CasualYT31/gallery-dl-tiktok-support/archive/tiktok-support.zip)  
2. Open `TT_Scraper.py` and run it.  
   - The script will ask you to input the path of an HTML document in the terminal.  
   - Navigate to the HTML of the collection you just downloaded, copy the pathname (on Mac: right-click + "Option"), paste it, and press **Enter**.

You should now have a **CSV** and **JSON** file in the same location as your HTML file called:  
- `html_page_metadata.csv`  
- `html_page_metadata.json`  

These contain all the links to the videos and some other metadata we need.

---

### Step 5: Download post content
1. Run `TT_Downloader.py`.  
   - In the terminal, the script will ask for the path to the JSON you just made. Paste it in and press **Enter**.  
2. All posts will now be saved in the same folder as the JSON/HTML file in a folder called `Collection Media`.  
   - Metadata will be saved to `metadata.csv` and `metadata.json`.  
   - Errors will be logged in `errors.txt` within the `Collection Media` folder.  

#### Common reasons for errors:
- Posts with Sensitive content restrictions won't download (due to `yt-dlp`).  
- Some ads have special privileges that prevent downloads seemingly  
- Audio may not download for slideshows (~5–10% of the time). No idea why. 
- General moodiness from TikTok. It will be banned soon so I’m taking what I can get.

---

## Sample Metadata (JSON)

### Sample Video
```json
{
    "Video/Post ID": "7194227443635375403",
    "Date (UNIX timestamp)": 1675036606,
    "Date (EST)": "Sun Jan 29 2023 18:56:46",
    "Name": "📞 ON BARI",
    "Username": "@janetgrandson",
    "Description": "Toothache I hope this cure me #toothache",
    "Sound Name": "original sound—📞 ON BARI",
    "Link": "https://www.tiktok.com/@janetgrandson/video/7194227443635375403",
    "Views": 259,
    "Likes": 15,
    "Comments": 5,
    "Track": "Players - DJ Smallz 732 - Jersey Club Remix",
    "Artist": "Coi Leray",
    "Resolution": "576x1024"
}
```
### Sample Slideshow
```json
{
    "Video/Post ID": "7229476922596592942",
    "Date (UNIX timestamp)": 1683243765,
    "Date (EST)": "Thu May 04 2023 18:42:45",
    "Name": "",
    "Username": "@prosto_chel_11",
    "Description": "Dont mind that theres like shit stuck to her fur #cat #kitty #catsoftiktok #cats #kitty #kittycat #meow #meowmeow",
    "Sound Name": "",
    "Link": "https://www.tiktok.com/@prosto_chel_11/photo/7229476922596592942",
    "Views": "",
    "Likes": "",
    "Comments": "",
    "Track": "",
    "Artist": "",
    "Resolution": ""
}
```
Note: Slideshow posts have a lot of missing data. yt-dlp cannot fully access slideshow posts. TikTokApi might solve this, but I couldn’t figure it out.

# Disclaimers

Scraping is against TikTok guidelines. If they ban you for it, or if anything unsavory happens, its not my fault. Proceed at your own risk.

I'm not a good programmer, and this code is kind of garbage. It's been edited to hell by just about every LLM out there. I'm publishing it because all the tasks it performs are very low-stakes, and it has worked for 100000+ posts at this point for me. I am not an expert. Proceed at your own risk.

# Good luck!
