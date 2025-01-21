import os
import glob
import json
import csv
import subprocess
import yt_dlp

metadata_folder_path = input('Enter the path to the folder with html_page_metadata.json files: ').strip()

for metadata_path in sorted(glob.glob(os.path.join(metadata_folder_path, '**/html_page_metadata.json'))):
    print(f"Processing file: {metadata_path}")

    # # Ask for the path to html_page_metadata.json
    # metadata_path = input("Enter the path to html_page_metadata.json: ").strip()
    #
    # # Verify the provided metadata path exists
    # if not os.path.isfile(metadata_path):
    #     raise FileNotFoundError(f"The file {metadata_path} does not exist.")

    # Define constants
    PARENT_FOLDER = os.path.dirname(metadata_path)
    OUTPUT_FOLDER = os.path.join(PARENT_FOLDER, "Collection Media")
    ERRORS_FILE = os.path.join(OUTPUT_FOLDER, "errors.txt")
    CSV_FILE = os.path.join(PARENT_FOLDER, "metadata.csv")
    JSON_FILE = os.path.join(PARENT_FOLDER, "metadata.json")

    # Ensure output folder and errors.txt exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    if os.path.exists(ERRORS_FILE):
        os.remove(ERRORS_FILE)  # Clear previous errors

    # Load HTML metadata
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Initialize lists for CSV/JSON metadata
    metadata_list = []
    failed_downloads = []


    # Download video with yt-dlp
    def process_video(entry):
        video_id = entry["Video/Post ID"]
        video_url = entry["Link"]
        output_path = os.path.join(OUTPUT_FOLDER, f"{video_id}.mp4")

        ydl_opts = {
            "quiet": False,
            "outtmpl": output_path,
            # NOTE: Not sure how to properly pass in this arg.
            # "extractor_args": {
            #     'tiktok': {
            #         'api_hostname': 'api16-normal-c-useast1a.tiktokv.com',
            #         'app_info': '7355728856979392262'
            #     }
            # }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(video_url, download=True)
                return {
                    "Views": info.get("view_count", ""),
                    "Likes": info.get("like_count", ""),
                    "Comments": info.get("comment_count", ""),
                    "Track": info.get("track", ""),
                    "Artist": info.get("artist", ""),
                    "Resolution": f"{info.get('width', '')}x{info.get('height', '')}",
                }
            except Exception as e:
                failed_downloads.append(f"Video ID {video_id} failed: {e}")
                return {}

    # Download photos with gallery-dl
    def process_photos(entry):
        photo_url = entry["Link"]
        photo_id = entry["Video/Post ID"]
        output_path = os.path.join(OUTPUT_FOLDER, photo_id)

        os.makedirs(output_path, exist_ok=True)

        command = [
            "gallery-dl",
            "--directory", output_path,
            photo_url,
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            failed_downloads.append(f"Photo ID {photo_id} failed: {e}")

    # Process entries
    for entry in metadata:
        video_id = entry["Video/Post ID"]
        is_video = "/video/" in entry["Link"]

        # Prepare metadata row
        row = {
            "Video/Post ID": entry.get("Video/Post ID", ""),
            "Date (UNIX timestamp)": entry.get("Date (UNIX timestamp)", ""),
            "Date (EST)": entry.get("Date (EST)", ""),
            "Name": entry.get("Name", ""),
            "Username": entry.get("Username", ""),
            "Description": entry.get("Description", ""),
            "Sound Name": entry.get("Sound Name", ""),
            "Link": entry.get("Link", ""),
        }

        # Process based on type
        if is_video:
            video_metadata = process_video(entry)
            row.update(video_metadata)
        else:
            process_photos(entry)
            row.update({
                "Views": "",
                "Likes": "",
                "Comments": "",
                "Track": "",
                "Artist": "",
                "Resolution": "",
            })

        metadata_list.append(row)

    # Write errors to file
    if failed_downloads:
        with open(ERRORS_FILE, "w") as f:
            f.write("\n".join(failed_downloads))

    # Save metadata to CSV
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=metadata_list[0].keys())
            writer.writeheader()
            writer.writerows(metadata_list)
    except Exception as e:
        print("WARN: Could not write metadata.")
        print(e)

    # Save metadata to JSON with ensure_ascii set to False
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata_list, f, indent=4, ensure_ascii=False)

    print(f"Processing complete. Data saved to {PARENT_FOLDER}. Errors logged to {ERRORS_FILE}.\n\n\n")
