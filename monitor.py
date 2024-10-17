import csv
import json
import os
import re
from ssl import Options
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def get_credentials():
    try:
        username = "@GeorgeHira23223"
        password = "Hirangeo@13"
    except Exception as e:
        print(f"Make sure username and password are added to .env file.\nError: {e}")
        return None, None
    return username, password

# Save cookies to a JSON file
def save_cookies(cookies, filename):
    with open(filename, 'w') as f:
        json.dump(cookies, f)

# Load cookies from a JSON file
def load_cookies(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def login(driver, username, password):
    driver.get("https://twitter.com/login")
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)

    username_input = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//input[@autocomplete="username"]')
        )
    )
    username_input.send_keys(username)
    username_input.send_keys(Keys.ENTER)
    print("username entered")
    try:
        phone_or_username_element = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//span[contains(text(), "Enter your phone number or username") or contains(text(), "Enter your phone number or email address")]')
            )
        )
        print("Login failed. Please enter your phone number or username.")
        if phone_or_username_element:
            username_input_field = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]')
                )
            )
            user = 'hirangeorge74@gmail.com'
            username_input_field.send_keys(user)
            username_input_field.send_keys(Keys.ENTER)
            print("Username entered again")
    except:
        print("CHECKING FOR PASSWORD FIELD")

    password_input = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//input[@autocomplete="current-password"]')
        )
    )
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    print("password entered")
    time.sleep(3)

    if "https://twitter.com/home" in driver.current_url:
        print("Login successful!")
    else:
        try:
            phone_or_username_element = wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//span[contains(text(), "Enter your phone number or username") or contains(text(), "Enter your phone number or email address")]')
                )
            )
            print("Login failed. Please enter your phone number or username.")
            if phone_or_username_element:
                username_input_field = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//input[@data-testid="ocfEnterTextTextInput"]')
                    )
                )
                user = 'hirangeorge74@gmail.com'
                username_input_field.send_keys(user)
                username_input_field.send_keys(Keys.ENTER)
                print("Username entered again")
        except:
            print("Login failed.")


def search_tweets(driver, search_by, number_of_tweets):
    wait = WebDriverWait(driver, 20)
    formatted_tweets = []
    for username in search_by:
        try:
            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]')))
            search_input.send_keys(Keys.CONTROL + "a", Keys.DELETE)

            search_input.send_keys(f'from:{username}')
            search_input.send_keys(Keys.ENTER)
            time.sleep(3)

            tweet_count = 0
            list_tweet = []
            while True:
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(4)
                like_elements = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, '[data-testid="like"]')
                    )
                )
                reposts = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, '[data-testid="retweet"]')
                    )
                )
                engagement_elements = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, '[aria-label*="views"]')
                    )
                )
                tweets = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//div[@data-testid="tweetText"]')
                    )
                )
                usernames = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, '[data-testid="User-Name"]')
                    )
                )
                replies = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, '[data-testid="reply"]')
                    )
                )
                hrefs = wait.until(
                    EC.presence_of_all_elements_located(
                        (
                            By.CSS_SELECTOR,
                            "[data-testid=User-Name] a[role=link][href*=status]",
                        )
                    )
                )
                times = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, 'time[datetime]')
                    )
                )

                print("getting tweets ...")

                for username_element, tweet_element, like_element, engagement_element, href_element, reply_element, repost_element, time_element in zip(
                    usernames, tweets, like_elements, engagement_elements, hrefs, replies, reposts, times
                ):
                    user_full_name = username_element.find_element(By.XPATH, "..").text.strip().rstrip(".")
                    twitter_handle = re.search(r'@(\w+)', user_full_name).group()

                    likes = like_element.get_attribute("aria-label")
                    likess = int(likes.split()[0]) if likes else 0

                    view = engagement_element.get_attribute("aria-label")
                    parts = view.split(", ")
                    views_count = int(parts[-1].split()[0])

                    repliess = reply_element.get_attribute("aria-label")
                    repliesss = int(repliess.split()[0]) if repliess else 0

                    repost_text = repost_element.get_attribute("aria-label")
                    repost_value = int(repost_text.split()[0]) if repost_text else 0

                    href = href_element.get_attribute("href")

                    time_value = time_element.get_attribute('datetime')

                    post_id = re.search(r'/status/(\d+)', href).group(1)

                    tweet = {
                        "UserName": user_full_name,
                        "TwitterHandle": twitter_handle,
                        "Date & Time": time_value,
                        "TweetContent": tweet_element.text,
                        "Replies": repliesss,
                        "Retweets": repost_value,
                        "Likes": likess,
                        "Views": views_count,
                        "TweetURL": href,
                    }
                    list_tweet.append(tweet)
                    print(tweet_count)
                    tweet_count += 1
                    if tweet_count >= number_of_tweets:
                        break
                if tweet_count >= number_of_tweets:
                    break

            formatted_tweet = {
                "type": "Profile",
                "keyword": username,
                "tweets": list_tweet
            }
            formatted_tweets.append(formatted_tweet)

        except Exception as e:
            print("Error:", e)

    save_tweet_data(formatted_tweets, "tweets.csv")
    return formatted_tweets

def save_tweet_data(formatted_tweets, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["UserName", "TwitterHandle", "Date & Time", "TweetContent", "Replies", "Retweets", "Likes", "Views", "TweetURL"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user_tweets in formatted_tweets:
            for tweet in user_tweets["tweets"]:
                writer.writerow({
                    "UserName": tweet["UserName"],
                    "TwitterHandle": tweet["TwitterHandle"],
                    "Date & Time": tweet["Date & Time"],
                    "TweetContent": tweet["TweetContent"],
                    "Replies": tweet["Replies"],
                    "Retweets": tweet["Retweets"],
                    "Likes": tweet["Likes"],
                    "Views": tweet["Views"],
                    "TweetURL": tweet["TweetURL"]
                })

def save_tweet_data(tweet_data, filename):
    fieldnames = ["UserName", "TwitterHandle", "Date & Time", "TweetContent", "Replies", "Retweets", "Likes", "Views", "TweetURL"]
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for profile in tweet_data:
            for tweet in profile["tweets"]:
                writer.writerow(tweet)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main(search_criteria, number_of_tweets):
    username, password = get_credentials()
    search_by = search_criteria 

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    cookies_filename = "cookies.json"
    try:
        cookies = load_cookies(cookies_filename)
        if cookies:
            driver.get("https://twitter.com/")
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.get("https://twitter.com/home")
        else:
            print("No cookies found. Using login credentials.")
            login(driver, username, password)
            cookies = driver.get_cookies()
            save_cookies(cookies, cookies_filename)
    except Exception as e:
        print(f"Error loading cookies: {e}. Using login credentials.")
        login(driver, username, password)
        cookies = driver.get_cookies()
        save_cookies(cookies, cookies_filename)
    
    try:
        formatted_tweets = search_tweets(driver, search_by, number_of_tweets)
        if formatted_tweets:
            print("Tweets retrieved successfully.")
            return formatted_tweets
        else:
            print("No tweets retrieved.")
            return []
    finally:
        driver.quit()



if __name__ == "__main__":
    search_by = input("Enter the usernames (comma-separated): ").split(',')
    number_of_tweets = int(input("Enter the number of tweets per user: "))
    tweets = main(search_by, number_of_tweets)
    print(tweets)

