import requests

def search_videos(query, no_res):
    url = "https://api.dailymotion.com/videos"
    params = {
        "search": query,
        "limit": no_res,  # Limiting to 10 results, adjust as needed
        "fields": "id,title,url,thumbnail_url"
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()

        video_info = [{'video_id' : video['id'], 'title' : video['title'], 'video_url' : video['url'], 'thumbnail_url' : video['thumbnail_url']} for video in data['list']]
        return video_info
    else:
        print("Error occurred:", response.text)
        return None

def main(query, no_res):
    videos = search_videos(query, no_res)
    if videos:
        print("Search Results:")
        for id, title, link, thumbnail_url in videos:
            print(f"Id: {id}")
            print(f"Title: {title}")
            print(f"URL: {link}")
            print(f"Thumbnail URL: {thumbnail_url}")
            print()  # Add a newline for better readability
    else:
        print("No videos found.")

if __name__ == "__main__":
    query = input("Enter your search query: ")
    no_res = int(input())

    main(query, no_res)
