import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

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
    try:
        WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))).click()
        time.sleep(2)
        print(f"[Info] - Scraping followers for {username}...")

        users = set()
        prev_users_count = 0
        consecutive_empty_scrolls = 0
        max_consecutive_empty_scrolls = 5
        loading_timeout = 40  
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
        return True
    except Exception as e:
        print(f"[Error] - Error scraping followers: {str(e)}")
        return False


def scrape():
    credentials = [
        ("Projectmlinsta", "@mlcheck1")
    ]

    user_input = 500  

    scrape_username = input("Enter the Instagram username you want to scrape followers of: ")

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    # options.add_argument("--headless") uncomment this if you want to run the script in linux.
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)


    for username, password in credentials:
        bot = webdriver.Chrome(service=service, options=options)
        bot.set_page_load_timeout(15) # Set the page load timeout to 15 seconds

        login(bot, username, password)
        if scrape_followers(bot, scrape_username, user_input):
            break 
        else:
            print("[Info] - Waiting for 3 seconds before trying next account...")
            time.sleep(3)

        bot.quit()

if __name__ == '__main__':
    TIMEOUT = 15
    scrape()
