# I have provided my temporary Instagram account's credentials if you get login error in chrome then please use your temporary instagram accout's credentials. in Line 35,36. :)
from flask import Flask, render_template, request
import time
import pickle
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)
def save_credentials(username, password):
    with open('credentials.txt', 'w') as file:
        file.write(f"{username}\n{password}")

def load_credentials():
    if not os.path.exists('credentials.txt'):
        return None

    with open('credentials.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[0].strip(), lines[1].strip()

    return None

def prompt_credentials():
    username = "mlscpacc"
    password = "@MLproject"
    save_credentials(username, password)
    return username, password

def login(bot, login_username, password):
    bot.get('https://www.instagram.com/accounts/login/')
    time.sleep(1)
    try:
        element = bot.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div[2]/button")
        element.click()
    except NoSuchElementException:
        print("[Info] - Instagram did not require to accept cookies this time.")

    print("[Info] - Logging in...")
    username_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username_input.clear()
    username_input.send_keys(login_username)
    password_input.clear()
    password_input.send_keys(password)

    login_button = WebDriverWait(bot, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()
    time.sleep(10)

def scrape_followers(bot, username, user_input):
    bot.get(f'https://www.instagram.com/{username}/')
    time.sleep(3.5)
    if bot.find_elements(By.XPATH, "//span[text()='this account is private']"):
        print("[Info] - This account is private. Cannot fetch followers.")
        return
    
    try:
        WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))).click()
        time.sleep(2)
        print(f"[Info] - Scraping followers for {username}...")
    
        users = set()
        prev_users_count = 0
        consecutive_empty_scrolls = 0
        max_consecutive_empty_scrolls = 5
        loading_timeout = 15 
        loading_start_time = time.time()

        while len(users) < user_input:
            followers = bot.find_elements(By.XPATH, "//a[contains(@href, '/')]")

            for i in followers:
                href = i.get_attribute('href')
                if href:
                    profile_name = href.split("/")[3]
                    users.add(profile_name)

            if len(users) == prev_users_count:
                consecutive_empty_scrolls += 1
            else:
                consecutive_empty_scrolls = 0

            if consecutive_empty_scrolls >= max_consecutive_empty_scrolls:
                break

            prev_users_count = len(users)

            ActionChains(bot).send_keys(Keys.END).perform()
            time.sleep(1)

            if bot.execute_script("return document.readyState") == "complete":
                consecutive_empty_scrolls = 0
            else:
                time.sleep(2)  
            if time.time() - loading_start_time > loading_timeout:
                print("[Info] - Loading timeout reached. Stopping scraping.")
                break

            if time.time() - loading_start_time > 3 and not bot.execute_script("return document.readyState") == "complete":
                print("[Info] - Page loading took too long. Stopping scraping.")
                break

        users = list(users)[:user_input] 
        
        print(f"[Info] - Saving followers for {username}...")
        with open(f'file.txt', 'a') as file:
            file.write('\n'.join(users) + "\n")
            
    except Exception as e:
        print(f"[Error] - An error occurred while scraping followers: Private Account or an error at Instagram's end")


def remove_usernames(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        filtered_lines = [line.strip() for line in lines if line.strip() not in ['technologies', 'legal', 'docs', 'reels', 'explore', 'blog', 'about', 'direct']]

        with open('file.txt', 'w') as file:
            file.write('\n'.join(filtered_lines))

        print("Usernames removed and filtered data saved to 'file.txt'.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

def scrape(username):
    credentials = load_credentials()

    if credentials is None:
        login_username, password = prompt_credentials()
    else:
        login_username, password = credentials

    user_input = 500  # It is limited to scrape 500 followers only you can increase if you want big dataset but that will take more time

    scrape_username = username
    chrome_path = './chrome/chrome.exe'
    service = Service()
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_path
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(service=service, options=options)
    bot.set_page_load_timeout(15) 

    login(bot, login_username, password)

    scrape_followers(bot, scrape_username, user_input)

    bot.quit()

    remove_usernames('file.txt')
#merged 2nd script here that will collect data from list of followers of target username that we entered
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import pickle 

def calculate_ratio(username):
    total_chars = len(username)
    num_chars = sum(c.isdigit() for c in username)
    if total_chars == 0:
        return 0
    return num_chars / total_chars

def get_user_data(username):
    url = f'https://www.instagram.com/{username}/'
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            follower_count_tag = soup.find('meta', attrs={'name': 'description'})
            if follower_count_tag:
                content = follower_count_tag.get('content', '')
                content_parts = content.split(',')
                if len(content_parts) >= 3:
                    follower_count = content_parts[1].split()[0]
                    following_count = content_parts[2].split()[0]
                    post_count = content_parts[0].split()[0]
                    nums_in_username = calculate_ratio(username)
                    return {
                        "numsinusername": nums_in_username,
                        "posts": post_count,
                        "followers": follower_count,
                        "following": following_count,
                        "ratio": int(follower_count) / (int(following_count) + 1),
                    }
                else:
                    print(f"Failed to extract necessary data for {username}")
            else:
                print(f"Failed to find meta description for {username}")
        else:
            print(f"Failed to fetch {url}: {response.status_code}")
    except Exception as e:
        print(f"Error fetching data for {username}: {e}")
    return None

def save_to_csv(user_data):
    with open("user_data.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["numsinusername", "posts", "followers", "following", "ratio"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in user_data:
            writer.writerow(data)

def drop_rows_with_letter(csv_file):
    df = pd.read_csv(csv_file)

    for column in df.columns:
        # it drops rows where the column contains 'K' or 'M'
        df = df[~df[column].astype(str).str.contains('[KM]', na=False)]
    df.to_csv(csv_file, index=False)

def main():
    with open('file.txt', 'r') as f:
        usernames = [line.strip() for line in f]

    user_data = []
    for username in usernames:
        data = get_user_data(username)
        if data:
            user_data.append(data)

    save_to_csv(user_data)
    csv_file = "user_data.csv"
    drop_rows_with_letter(csv_file)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    tdata= pd.read_csv("user_data.csv")
    with open("RF.pkl",'rb') as f:
        rfc=pickle.load(f)

    from sklearn.metrics import accuracy_score
    rfpred = rfc.predict(tdata)
    percentage_fake_followers = (sum(rfpred) / len(rfpred)) * 50
    print("Percentage of fake followers:", percentage_fake_followers,"%")
    return percentage_fake_followers
import multiprocessing
def run_function_with_timeout():
    # Start the function in a separate process
    process = multiprocessing.Process(target=main)
    process.start()

    # Wait for the specified timeout
    timeout = 10  # Timeout in seconds
    process.join(timeout)

    # If the process is still alive after the timeout, terminate it
    if process.is_alive():
        print("Timeout reached. Terminating the function...")
        process.terminate()
        process.join()
@app.route('/', methods=['GET', 'POST'])
def index():
    global percentage_fake_followers  
    if request.method == 'POST':
        username = request.form['username']
        scrape(username)
        percentage_fake_followers = main()  
        os.remove('file.txt')  # Remove file.txt otherwise it will add existing followers to next account's data
        os.remove('user_data.csv')  # Remove user_data.csv same reason here
        return render_template('result.html', username=username, percentage_fake_followers=percentage_fake_followers)
    return render_template('index.html')



if __name__ == '__main__':
    TIMEOUT = 15
    app.run(debug=True, host='0.0.0.0')
