import logging
from datetime import datetime, timedelta
import threading, time
from time import sleep
import requests,re,random
import json
from urllib.parse import parse_qs
import os


# Get the current working directory
current_directory = os.getcwd()

# Define the relative path for the log file
relative_path = 'scraper/scrapy'

# Construct the absolute path by joining the current directory and the relative path
file_path = os.path.join(current_directory, relative_path)

logging.basicConfig(
                    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
logger.propagate = False


data_list = [
  {
    "cookes": "personalization_id='v1_dHHFLDyKtDVCMB311mOTGg==';lang=en;att=1-ycHI63cHXIvpuNVQFPl14HlqS4C7HiyLnKgrPAFU;auth_token=ba499e9788c9ba4d7bd5a22fd24327f5058da2d4;ct0=b86fb5f0515528aca84644829cdf3b9aa58e505e3000b1755d2f8c2e0453746521219ba508d27f8840470811f8b73485b983a7430df1e572cc35d9a8d0aa068923bc4a992b9509bae1d2668494af3a06;gt=1750018407460897212;_ga=GA1.2.1402762415.1706071873;kdt=oddzwALPLG4FY7nHIjRSrRt5qEXIEbT72YjAPBXg;_gid=GA1.2.678308757.1706071873;twid=u%3D1745514902863929344;guest_id=v1%3A170607187673692322;guest_id_ads=v1%3A170607187673692322;_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDL1zjmNAToMY3NyZl9p%250AZCIlZWI0NDFjNzBkMjgzMWE0ZTFiZDU5MTU1ZTE0ZDA2ZDE6B2lkIiU3Zjdh%250AYTFkYzJiMDQ4YWJlZDhlMzYyMTE5ZGI0YWJlYg%253D%253D--11a182538497f43357f1bdfbbd59fac05bc17db1;guest_id_marketing=v1%3A170607187673692322"
  },
  {
    "cookes": "personalization_id='v1_dHHFLDyKtDVCMB311mOTGg==';lang=en;att=1-ycHI63cHXIvpuNVQFPl14HlqS4C7HiyLnKgrPAFU;auth_token=ba499e9788c9ba4d7bd5a22fd24327f5058da2d4;ct0=b86fb5f0515528aca84644829cdf3b9aa58e505e3000b1755d2f8c2e0453746521219ba508d27f8840470811f8b73485b983a7430df1e572cc35d9a8d0aa068923bc4a992b9509bae1d2668494af3a06;gt=1750018407460897212;_ga=GA1.2.1402762415.1706071873;kdt=oddzwALPLG4FY7nHIjRSrRt5qEXIEbT72YjAPBXg;_gid=GA1.2.678308757.1706071873;twid=u%3D1745514902863929344;guest_id=v1%3A170607187673692322;guest_id_ads=v1%3A170607187673692322;_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDL1zjmNAToMY3NyZl9p%250AZCIlZWI0NDFjNzBkMjgzMWE0ZTFiZDU5MTU1ZTE0ZDA2ZDE6B2lkIiU3Zjdh%250AYTFkYzJiMDQ4YWJlZDhlMzYyMTE5ZGI0YWJlYg%253D%253D--11a182538497f43357f1bdfbbd59fac05bc17db1;guest_id_marketing=v1%3A170607187673692322"
  },
  {
    "cookes": "personalization_id='v1_dHHFLDyKtDVCMB311mOTGg==';lang=en;att=1-ycHI63cHXIvpuNVQFPl14HlqS4C7HiyLnKgrPAFU;auth_token=ba499e9788c9ba4d7bd5a22fd24327f5058da2d4;ct0=b86fb5f0515528aca84644829cdf3b9aa58e505e3000b1755d2f8c2e0453746521219ba508d27f8840470811f8b73485b983a7430df1e572cc35d9a8d0aa068923bc4a992b9509bae1d2668494af3a06;gt=1750018407460897212;_ga=GA1.2.1402762415.1706071873;kdt=oddzwALPLG4FY7nHIjRSrRt5qEXIEbT72YjAPBXg;_gid=GA1.2.678308757.1706071873;twid=u%3D1745514902863929344;guest_id=v1%3A170607187673692322;guest_id_ads=v1%3A170607187673692322;_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDL1zjmNAToMY3NyZl9p%250AZCIlZWI0NDFjNzBkMjgzMWE0ZTFiZDU5MTU1ZTE0ZDA2ZDE6B2lkIiU3Zjdh%250AYTFkYzJiMDQ4YWJlZDhlMzYyMTE5ZGI0YWJlYg%253D%253D--11a182538497f43357f1bdfbbd59fac05bc17db1;guest_id_marketing=v1%3A170607187673692322"
  },
  {
    "cookes": "personalization_id='v1_dHHFLDyKtDVCMB311mOTGg==';lang=en;att=1-ycHI63cHXIvpuNVQFPl14HlqS4C7HiyLnKgrPAFU;auth_token=ba499e9788c9ba4d7bd5a22fd24327f5058da2d4;ct0=b86fb5f0515528aca84644829cdf3b9aa58e505e3000b1755d2f8c2e0453746521219ba508d27f8840470811f8b73485b983a7430df1e572cc35d9a8d0aa068923bc4a992b9509bae1d2668494af3a06;gt=1750018407460897212;_ga=GA1.2.1402762415.1706071873;kdt=oddzwALPLG4FY7nHIjRSrRt5qEXIEbT72YjAPBXg;_gid=GA1.2.678308757.1706071873;twid=u%3D1745514902863929344;guest_id=v1%3A170607187673692322;guest_id_ads=v1%3A170607187673692322;_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDL1zjmNAToMY3NyZl9p%250AZCIlZWI0NDFjNzBkMjgzMWE0ZTFiZDU5MTU1ZTE0ZDA2ZDE6B2lkIiU3Zjdh%250AYTFkYzJiMDQ4YWJlZDhlMzYyMTE5ZGI0YWJlYg%253D%253D--11a182538497f43357f1bdfbbd59fac05bc17db1;guest_id_marketing=v1%3A170607187673692322"
  },
  {
    "cookes": "personalization_id='v1_dHHFLDyKtDVCMB311mOTGg==';lang=en;att=1-ycHI63cHXIvpuNVQFPl14HlqS4C7HiyLnKgrPAFU;auth_token=ba499e9788c9ba4d7bd5a22fd24327f5058da2d4;ct0=b86fb5f0515528aca84644829cdf3b9aa58e505e3000b1755d2f8c2e0453746521219ba508d27f8840470811f8b73485b983a7430df1e572cc35d9a8d0aa068923bc4a992b9509bae1d2668494af3a06;gt=1750018407460897212;_ga=GA1.2.1402762415.1706071873;kdt=oddzwALPLG4FY7nHIjRSrRt5qEXIEbT72YjAPBXg;_gid=GA1.2.678308757.1706071873;twid=u%3D1745514902863929344;guest_id=v1%3A170607187673692322;guest_id_ads=v1%3A170607187673692322;_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDL1zjmNAToMY3NyZl9p%250AZCIlZWI0NDFjNzBkMjgzMWE0ZTFiZDU5MTU1ZTE0ZDA2ZDE6B2lkIiU3Zjdh%250AYTFkYzJiMDQ4YWJlZDhlMzYyMTE5ZGI0YWJlYg%253D%253D--11a182538497f43357f1bdfbbd59fac05bc17db1;guest_id_marketing=v1%3A170607187673692322"
  },
  {
    "cookes": "personalization_id='v1_dHHFLDyKtDVCMB311mOTGg==';lang=en;att=1-ycHI63cHXIvpuNVQFPl14HlqS4C7HiyLnKgrPAFU;auth_token=ba499e9788c9ba4d7bd5a22fd24327f5058da2d4;ct0=b86fb5f0515528aca84644829cdf3b9aa58e505e3000b1755d2f8c2e0453746521219ba508d27f8840470811f8b73485b983a7430df1e572cc35d9a8d0aa068923bc4a992b9509bae1d2668494af3a06;gt=1750018407460897212;_ga=GA1.2.1402762415.1706071873;kdt=oddzwALPLG4FY7nHIjRSrRt5qEXIEbT72YjAPBXg;_gid=GA1.2.678308757.1706071873;twid=u%3D1745514902863929344;guest_id=v1%3A170607187673692322;guest_id_ads=v1%3A170607187673692322;_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDL1zjmNAToMY3NyZl9p%250AZCIlZWI0NDFjNzBkMjgzMWE0ZTFiZDU5MTU1ZTE0ZDA2ZDE6B2lkIiU3Zjdh%250AYTFkYzJiMDQ4YWJlZDhlMzYyMTE5ZGI0YWJlYg%253D%253D--11a182538497f43357f1bdfbbd59fac05bc17db1;guest_id_marketing=v1%3A170607187673692322"
  },
  {
    "cookes": "personalization_id='v1_dHHFLDyKtDVCMB311mOTGg==';lang=en;att=1-ycHI63cHXIvpuNVQFPl14HlqS4C7HiyLnKgrPAFU;auth_token=ba499e9788c9ba4d7bd5a22fd24327f5058da2d4;ct0=b86fb5f0515528aca84644829cdf3b9aa58e505e3000b1755d2f8c2e0453746521219ba508d27f8840470811f8b73485b983a7430df1e572cc35d9a8d0aa068923bc4a992b9509bae1d2668494af3a06;gt=1750018407460897212;_ga=GA1.2.1402762415.1706071873;kdt=oddzwALPLG4FY7nHIjRSrRt5qEXIEbT72YjAPBXg;_gid=GA1.2.678308757.1706071873;twid=u%3D1745514902863929344;guest_id=v1%3A170607187673692322;guest_id_ads=v1%3A170607187673692322;_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDL1zjmNAToMY3NyZl9p%250AZCIlZWI0NDFjNzBkMjgzMWE0ZTFiZDU5MTU1ZTE0ZDA2ZDE6B2lkIiU3Zjdh%250AYTFkYzJiMDQ4YWJlZDhlMzYyMTE5ZGI0YWJlYg%253D%253D--11a182538497f43357f1bdfbbd59fac05bc17db1;guest_id_marketing=v1%3A170607187673692322"
  },
  {
    "cookes": "personalization_id='v1_dHHFLDyKtDVCMB311mOTGg==';lang=en;att=1-ycHI63cHXIvpuNVQFPl14HlqS4C7HiyLnKgrPAFU;auth_token=ba499e9788c9ba4d7bd5a22fd24327f5058da2d4;ct0=b86fb5f0515528aca84644829cdf3b9aa58e505e3000b1755d2f8c2e0453746521219ba508d27f8840470811f8b73485b983a7430df1e572cc35d9a8d0aa068923bc4a992b9509bae1d2668494af3a06;gt=1750018407460897212;_ga=GA1.2.1402762415.1706071873;kdt=oddzwALPLG4FY7nHIjRSrRt5qEXIEbT72YjAPBXg;_gid=GA1.2.678308757.1706071873;twid=u%3D1745514902863929344;guest_id=v1%3A170607187673692322;guest_id_ads=v1%3A170607187673692322;_twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDL1zjmNAToMY3NyZl9p%250AZCIlZWI0NDFjNzBkMjgzMWE0ZTFiZDU5MTU1ZTE0ZDA2ZDE6B2lkIiU3Zjdh%250AYTFkYzJiMDQ4YWJlZDhlMzYyMTE5ZGI0YWJlYg%253D%253D--11a182538497f43357f1bdfbbd59fac05bc17db1;guest_id_marketing=v1%3A170607187673692322"
  }
]



lop_time=0
loping_limite=8
#def profile_scrept(user_name,cookies,reaction_limite,viwes_limite,comment_limite,nb_tweets):

data_profile=[]


def get_profile_uid(cookies,user_name,headers):
        try:
            params = {
            'variables': '{"screen_name":"%s"}'%(user_name),
            }
            response = requests.get(
                'https://twitter.com/i/api/graphql/_pnlqeTOtnpbIL9o-fS_pg/ProfileSpotlightsQuery',
                params=params,cookies=cookies,headers=headers)
            data=(response.json())
            rest_id = data['data']['user_result_by_screen_name']['result']['rest_id']
            return rest_id
        except : return "invaid"


def scretpt(loads_data, reaction_limite, viwes_limite, comment_limite, user_name):
    try:
        # Attempt to retrieve the entries from the loaded data
        try:
            entry_id = loads_data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][1]["entries"]
        except IndexError as e:
            logging.warning("IndexError encountered, trying alternative index for entries.")
            try:
                entry_id = loads_data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][0]["entries"]
            except IndexError:
                entry_id = loads_data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"][2]["entries"]

        # Process each entry
        for data in entry_id:
            # Skip cursor responses
            if "tweet" not in data["entryId"]:
                continue

            # Parse tweet details
            result = data["content"]["itemContent"]["tweet_results"]["result"]
            legacy = result.get("legacy", result.get("tweet", {}).get("legacy", {}))

            print(f"This is the data what you want {legacy}")

            post_id = legacy.get("id_str", "")
            date_post = legacy.get("created_at", "")
            connnt_num = legacy.get("reply_count", 0)
            chaption = legacy.get("full_text", "")
            reaction_numbr = legacy.get("favorite_count", 0)
            viwes = result.get("views", {}).get("count", 0)
            post_url = legacy.get("entities", {}).get("media", [{}])[0].get("expanded_url", f"https://twitter.com/{user_name}/status/{post_id}")
            user_name = result.get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {}).get("screen_name", "")

            # Filter out reposts and ads
            if user_name and user_name not in post_url:
                continue

            # Append data if it meets the criteria
            if int(reaction_numbr) >= int(reaction_limite) and int(connnt_num) >= int(comment_limite) and int(viwes) >= int(viwes_limite):
                data_profile.append({
                    "user_name":user_name,
                    "post_id": post_id,
                    "post_url": post_url,
                    "date_of_post": date_post,
                    "tweet": chaption,
                    "likes": reaction_numbr,
                    "comments": connnt_num,
                    "views": viwes
                })

    except Exception as e:
        logging.error(f"Exception in scretpt: {e}")


def loping(rest_id, user_name, tweet_text, cookies, reaction_limite, viwes_limite, comment_limite, nb_tweets, headers):

    global messag, lop_time
    lop_time += 1
    scretpt(tweet_text.json(), reaction_limite, viwes_limite, comment_limite, user_name)

    try:
        cursor = re.findall('"value":"(.*?)","cursorType', tweet_text.text)[1]
        variables = {
            "userId": rest_id,
            "count": 100,
            "cursor": cursor,
            "includePromotedContent": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
            "withV2Timeline": True
        }

        features = {
        "responsive_web_graphql_exclude_directive_enabled":True,"verified_phone_label_enabled":False,"creator_subscriptions_tweet_preview_api_enabled":True,"responsive_web_graphql_timeline_navigation_enabled":True,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":False,"c9s_tweet_anatomy_moderator_badge_enabled":True,"tweetypie_unmention_optimization_enabled":True,"responsive_web_edit_tweet_api_enabled":True,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":True,"view_counts_everywhere_api_enabled":True,"longform_notetweets_consumption_enabled":True,"responsive_web_twitter_article_tweet_consumption_enabled":False,"tweet_awards_web_tipping_enabled":False,"freedom_of_speech_not_reach_fetch_enabled":True,"standardized_nudges_misinfo":True,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":True,"rweb_video_timestamps_enabled":True,"longform_notetweets_rich_text_read_enabled":True,"longform_notetweets_inline_media_enabled":True,"responsive_web_media_download_video_enabled":False,"responsive_web_enhance_cards_enabled":False}

        response = requests.get(
            'https://twitter.com/i/api/graphql/NBWKw7od2So5qClZpLyQ0w/UserTweets',
            params={'variables': json.dumps(variables), 'features': json.dumps(features)},
            cookies=cookies,
            headers=headers,
            allow_redirects=False
        )

        if response.status_code == 200:
            if lop_time < loping_limite and len(data_profile) <= nb_tweets:
                loping(rest_id, user_name, response, cookies, reaction_limite, viwes_limite, comment_limite, nb_tweets, headers)
            else:
                messag = "Done"
        elif response.status_code >= 400:
            het_coookes(user_name, cookies, reaction_limite, viwes_limite, comment_limite, nb_tweets)
    except Exception as e:
        logging.exception(f"Exception in loping: {e}")
        het_coookes(user_name, cookies, reaction_limite, viwes_limite, comment_limite, nb_tweets)

    return messag



def screpeing_profile_post(user_name,cookies,reaction_limite,viwes_limite,comment_limite,nb_tweets,get_uid_only=False):  #seach fast page and get data
    # try:

        headers = {'authority': 'twitter.com',
        'accept': '*/*','accept-language': 'en-US,en;q=0.9,id;q=0.8,bn;q=0.7','authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json','referer': 'https://twitter.com/Haqiqatjou','sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',#W_ueragnt(),
        'x-client-transaction-id': 'BVz3kb2LqtGYEhSPp3wEynvqiYCGRff9SjF37JH8htWXjiV5EGmxJM1qfuQKTa5UksI2VwTpdzt8BMp7gReDTRzgyOj4BA',
        'x-client-uuid': 'd145651c-dfcd-4e30-a8fd-abd1e72f3f86',
        'x-twitter-active-user': 'yes','x-twitter-auth-type': 'OAuth2Session','x-twitter-client-language': 'en',
        'x-csrf-token':cookies['ct0']}
        data_profile.clear()
        rest_id=get_profile_uid(cookies,user_name,headers)
        if get_uid_only:
            return rest_id
        if "invaid" in rest_id:
            het_coookes(user_name,cookies,reaction_limite,viwes_limite,comment_limite,nb_tweets)
        else:
            params = {
                'variables': '{"userId":"%s","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withVoice":true,"withV2Timeline":true,"near":"%s","count":200,"querySource":"recent_search_click","product":"Top"}' % (rest_id, location),
                'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}'
            }
            tweet_text = requests.get('https://twitter.com/i/api/graphql/NBWKw7od2So5qClZpLyQ0w/UserTweets',params=params,cookies=cookies,headers=headers)

            if tweet_text.status_code==200:
                loping(rest_id,user_name,tweet_text,cookies,reaction_limite,viwes_limite,comment_limite,nb_tweets,headers)
                # thread1 = threading.Thread(target=loping, args=(rest_id,user_name,tweet_text,cookies,reaction_limite,viwes_limite,comment_limite,nb_tweets,headers,date_time))
                # thread1.start()
                # thread1.join()
            elif tweet_text.status_code>=400:
                screpeing_profile_post(user_name,cookies,reaction_limite,viwes_limite,comment_limite,nb_tweets)
            if "Done" in messag:
                return data_profile
            else:
                logging.error("Something Is Wrong Or Invaid Cookes")
                return  "Something Is Wrong Or Invaid Cookes"
    # except Exception as e:
    #     logging.error(f"screpeing_profile_post {e}")
    #     return e
            
            

def het_coookes(user_name, cookies, reaction_limite, viwes_limite, comment_limite, nb_tweets):
    try:
        # Assuming data_list is a list of dictionaries with a 'cookies' key
        cookies_list = [entry['cookies'] for entry in data_list]
        new_cookie_str = random.choice(cookies_list)
        new_cookies = {key: value[0] for key, value in parse_qs(new_cookie_str.replace(' ', ''), separator=';').items()}
        
        # Call the scraping function with the new cookies
        screpeing_profile_post(user_name, new_cookies, reaction_limite, viwes_limite, comment_limite, nb_tweets)
    except Exception as e:
        logging.error(f"Error in het_coookes: {e}")



search_data=[]

def felteringx(post_url, reaction_numbr, connnt_num, chaption, viwes, reaction_limite, viwes_limite, comment_limite, date_post, post_id,user_name):
    print("_____________________________________________6")

    try:
        # Convert string numbers to integers for comparison
        reaction_number = int(reaction_numbr)
        comment_number = int(connnt_num)
        view_number = int(viwes)

        # Check if the post meets the specified limits
        if reaction_number >= reaction_limite and comment_number >= comment_limite and view_number >= viwes_limite:
            search_data.append({
                "user_name": user_name, 
                "post_id": post_id,
                "post_url": post_url,
                "date_of_post": date_post,
                "tweet": chaption,
                "likes": reaction_number,
                "comments": comment_number,
                "views": view_number
            })
    except Exception as e:
        logging.error(f"felteringx Exception: {e}")


def felteringx(post_url, reaction_numbr, connnt_num, chaption, viwes, reaction_limite, viwes_limite, comment_limite, date_post, post_id, location,user_name):
    try:

        # Convert string numbers to integers for comparison
        reaction_number = int(reaction_numbr)
        comment_number = int(connnt_num)
        view_number = int(viwes)
        # Check if the post meets the specified limits
        if reaction_number >= reaction_limite and comment_number >= comment_limite and view_number >= viwes_limite:
            search_data.append({
                "user_name": user_name, 
                "post_id": post_id,
                "post_url": post_url,
                "date_of_post": date_post,
                "tweet": chaption,
                "likes": reaction_number,
                "comments": comment_number,
                "views": view_number,
                "location": location  # Include location information
            })
    except Exception as e:
        logging.error(f"felteringx Exception: {e}")



def parsing(loads_data, reaction_limite, viwes_limite, comment_limite):


    """
    Parses all data from the response or input text and filters tweets based on given limits.

    Parameters:
    loads_data (dict): The loaded JSON data from Twitter's response.
    reaction_limite (int): The minimum number of reactions required.
    viwes_limite (int): The minimum number of views required.
    comment_limite (int): The minimum number of comments required.
    """
    try:
        entries = loads_data["data"]["search_by_raw_query"]["search_timeline"]["timeline"]["instructions"][0]["entries"]
        for entry in entries:

            if "tweet" not in entry["entryId"] or "promoted-tweet" in entry["entryId"]:
                continue

            content = entry.get("content", {})
            tweet_results = content.get("itemContent", {}).get("tweet_results", {})
            result = tweet_results.get("result", {})
            user_name = result.get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {}).get("screen_name", "")

            location = result.get("core", {}).get("user_results", {}).get("result", {}).get("legacy", {}).get("location")

            print(location)

            if result.get('__typename') != 'Tweet':
                continue

            legacy = result.get("legacy", {})
            date_post = legacy.get("created_at")
            connnt_num = legacy.get("reply_count")
            post_id = legacy.get("id_str")
            chaption = legacy.get("full_text")
            reaction_numbr = legacy.get("favorite_count")
            viwes = result.get("views", {}).get("count", 0)

            # Construct post URL
            media_url = legacy.get("entities", {}).get("media", [{}])[0].get("expanded_url")
            post_url = media_url if media_url else f"https://twitter.com/topics/status/{post_id}"

            # Filter and append data
            felteringx(post_url, reaction_numbr, connnt_num, chaption, viwes, reaction_limite, viwes_limite, comment_limite, date_post, post_id, location,user_name)

    except Exception as e:
        logging.error(f"Parsing Exception: {e}")



def loping_serch(tweet_text,cookies,reaction_limite,viwes_limite,comment_limite,nb_tweets,chatagory,headers):

    parsing(tweet_text.json(),reaction_limite,viwes_limite,comment_limite)
    global messag,lop_time
    lop_time+=1
    """
    this a lop for send request gto get more data or Scrolling
    """
    try:
        cursor=re.findall('"TimelineTimelineCursor","value":"(.*?)","cursorType',str(tweet_text.text))[1]
        # print(cursor)
        params = {
        # 'variables': '{"rawQuery":"%s","count":50,"cursor":"%s","querySource":"recent_search_click","product":"Top"}'%(chatagory,cursor),
        'variables': '{"rawQuery":"%s","count":200,"querySource":"recent_search_click","product":"Top","withLocation":true}' % (chatagory),
        'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}',
        }
        response = requests.get('https://twitter.com/i/api/graphql/PaIcTAgMdfWySgs3aVU5TA/SearchTimeline', params=params,cookies=cookies,headers=headers,)
        if response.status_code ==200:
            s=len(search_data)
            if lop_time<loping_limite:
                if s >= int(nb_tweets):
                    messag = "Done"
                    return messag
                else:
                    loping_serch(response,cookies,reaction_limite,viwes_limite,comment_limite,nb_tweets,chatagory,headers)
            else:messag = "Done"
        if response.status_code >=400:
               het_coookes_search(chatagory,reaction_limite,viwes_limite,comment_limite,nb_tweets)
    except Exception as e:
        het_coookes_search(chatagory,reaction_limite,viwes_limite,comment_limite,nb_tweets)
        return e



def het_coookes_search(chatagory,reaction_limite,viwes_limite,comment_limite,nb_tweets,cookes_od=None):

    r"""
    If gets any error Change a new cookes and send all data as new on searching function
    """
    # formatted_cookies = ";".join([f"{cookie['name']}={cookie['value']}" for cookie in cookes_od])
    # data_list = json.loads(cookies_file)
    cookes = [entry['cookes'] for entry in data_list]
    # cookes.remove(formatted_cookies)
    cooki=random.choice(cookes)
    parsed_cookies = parse_qs(cooki.replace(' ',''), separator=';')
    cookiesx= {key: value[0] for key, value in parsed_cookies.items()}
    search_Top(cookiesx,chatagory,reaction_limite,viwes_limite,comment_limite,nb_tweets)



def search_Top(cookies,chatagory,reaction_limite,viwes_limite,comment_limite,nb_tweets):

    search_data.clear()
    headers = {'authority': 'twitter.com',
    'accept': '*/*','accept-language': 'en-US,en;q=0.9,id;q=0.8,bn;q=0.7','authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'content-type': 'application/json','referer': 'https://twitter.com/Haqiqatjou','sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',#W_ueragnt(),
    'x-client-transaction-id': 'BVz3kb2LqtGYEhSPp3wEynvqiYCGRff9SjF37JH8htWXjiV5EGmxJM1qfuQKTa5UksI2VwTpdzt8BMp7gReDTRzgyOj4BA',
    'x-client-uuid': 'd145651c-dfcd-4e30-a8fd-abd1e72f3f86',
    'x-twitter-active-user': 'yes','x-twitter-auth-type': 'OAuth2Session','x-twitter-client-language': 'en',
    'x-csrf-token':cookies['ct0'] ,
            }
    params = {
    # 'variables': '{"rawQuery":"%s","count":200,"querySource":"recent_search_click","product":"Top"}'%(chatagory),
    'variables': '{"rawQuery":"%s","count":200,"querySource":"recent_search_click","product":"Top","withLocation":true}' % (chatagory),
    'features': '{"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}',
    'variables': '{"rawQuery":"%s near:\\"%s\\"","count":200,"querySource":"recent_search_click","product":"Top"}' % (chatagory, location),
    }
    response = requests.get('https://twitter.com/i/api/graphql/HgiQ8U_E6g-HE_I6Pp_2UA/SearchTimeline',
        params=params,cookies=cookies,headers=headers)
    if response.status_code == 200:

        loping_serch(response,cookies,reaction_limite,viwes_limite,comment_limite,nb_tweets,chatagory,headers)


    if response.status_code >= 400:
        search_Top(cookies,chatagory,reaction_limite,viwes_limite,comment_limite,nb_tweets)
    if "Done" in messag:
        return search_data
    else:
        return "Something Is Wrong Or Invaid Cookes"



def cookes(x):

    global cookies
    # data_list = json.loads(cookies_file)
    cookes = [entry['cookes'] for entry in data_list]
    cooki=random.choice(cookes)
    parsed_cookies = parse_qs(cooki.replace(' ',''), separator=';')
    cookies= {key: value[0] for key, value in parsed_cookies.items()}

@cookes
def c():pass

def main(locations, type_search, keywords, reaction_limite,viwes_limite,comment_limite,nb_tweets, get_uid_only=False):

    print("locations", locations)
    print("type_search", type_search)
    print("keywords", keywords)
    print("reaction_limite", reaction_limite)
    print("views_limite", viwes_limite)
    print("comment_limite", comment_limite)
    print("nb_tweets", nb_tweets)
    
    global location
    location = locations
    tweets = []
    uid_list = []
    for keyword in keywords:
            sleep(0.2)
        # try:
            if type_search=='profile':
                # try:
                    global lop_time
                    lop_time=0
                    tweet=screpeing_profile_post(keyword,cookies,reaction_limite,viwes_limite,comment_limite,nb_tweets, get_uid_only)
                    if get_uid_only:
                        uid_list.append(tweet)
                        continue
                    new_data = [{
                        "type": "profile",
                        "keyword": keyword,
                        "tweets": []
                    }]
                    new_data[0]["tweets"].extend(tweet)
                    tweets.extend(new_data)
                # except Exception as e:
                #     print("main:- ",e)
            else:
                # try:
                    tweet=search_Top(cookies,keyword,reaction_limite,viwes_limite,comment_limite,nb_tweets*2)
                    new_data = [{
                        "type": "topic",
                        "keyword": keyword,
                        "tweets": []
                    }]
                    new_data[0]["tweets"].extend(tweet[:nb_tweets])
                    tweets.extend(new_data)

                # except Exception as e:
                #     print("tweet=search_Top:- ",e)

        # except Exception as e :
        #     print(e)
    # with open(f'{current_directory}/data_twi.json',"w",encoding="utf-8") as file:
    #     json_data = json.dump(tweets ,file ,ensure_ascii=False, indent=4)
    #     file.close()
    if get_uid_only:
        return uid_list
    print("Tweets = ",tweets)
    print("\n\n")
    return tweets

# from scraper.scrapy import tweeter_scraper
# print(tweeter_scraper.main("topics",["Computer","PC","Iphone"],0,0,0,15))

if __name__ == "__main__": 

    no_tweets=10           # the number of data you want
    total_likes=10
    total_views=10
    total_comments=10
    # keywords=["ipl"]
    type_search='topic'
    locations = "Bengaluru"
    keywords=["ipl"]
    # type_search='profile'
    new_data=main(locations, type_search, keywords, total_likes,total_views,total_comments,no_tweets)

    with open(f'data_twi.json',"w",encoding="utf-8") as file:
            json_data = json.dump(new_data ,file ,ensure_ascii=False, indent=4)
            file.close()