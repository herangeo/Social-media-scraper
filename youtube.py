import requests
from PIL import Image
from io import BytesIO

def search_youtube(query, no_res):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": "AIzaSyDWMJdHUKJxX5pGY_1cp1uLGT6Sy7n9I9E",
        "type": "video",
        "maxResults": str(no_res)  # You can adjust this value as needed
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    videos = []
    for item in data["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        thumbnail_url = item["snippet"]["thumbnails"]["default"]["url"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({"video_id": video_id, "title": title, "thumbnail_url": thumbnail_url, "video_url": video_url})

    return videos

def display_videos(videos):
    for video in videos:
        print("Video Id:", video["video_id"])
        print("Title:", video["title"])
        print("Thumbnail URL:", video["thumbnail_url"])
        print("Video URL:", video["video_url"])

        # Check if the video URL is accessible
        response = requests.get(video["video_url"])
        if response.status_code != 200:
            print("Video is unavailable, displaying thumbnail instead.")
            response = requests.get(video["thumbnail_url"])
            img = Image.open(BytesIO(response.content))
            img.show()
        print()

if __name__ == "__main__":
    no_res = 10
    query = input("Enter your search query: ")

    videos = search_youtube(query, no_res)
    display_videos(videos)
