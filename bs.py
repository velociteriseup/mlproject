import csv
from concurrent.futures import ThreadPoolExecutor
import instaloader
from instaloader import Profile

def convert_to_int(value):
    try:
        if value.endswith('K'):
            return int(float(value[:-1]) * 1000)
        elif value.endswith('M'):
            return int(float(value[:-1]) * 1000000)
        else:
            return int(value.replace(',', ''))
    except ValueError:
        return 0

def login(username, password):
    loader = instaloader.Instaloader()

    try:
        loader.load_session_from_file(username)
    except FileNotFoundError:
        loader.context.log("Session file does not exist - Logging in.")
        loader.context.log("Writing session file.")
        loader.context.login(username, password)
        loader.save_session_to_file()

    return loader

def get_account_data(username, loader):
    try:
        profile = Profile.from_username(loader.context, username)

        follower_count = profile.followers
        following_count = profile.followees
        posts_count = profile.mediacount

        total_chars = len(username)
        numbers_count = sum(c.isdigit() for c in username)
        percentage_of_numbers = (numbers_count / total_chars) * 100 if total_chars > 0 else 0

        ratio = following_count / follower_count if follower_count != 0 else 0

        bio_length = len(profile.biography)

        return [percentage_of_numbers, posts_count, follower_count, following_count, ratio, bio_length]
    except Exception as e:
        print(f"Error fetching data for {username}: {e}")
        return [0, 0, 0, 0, 0, 0]

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["numsinusername", "posts", "followers", "following", "ratio", "biolength"])
        writer.writerows(data)

def main():
    filename = "file.txt"

    # Provide your temporary Instagram username and password
    username = "Projectmlig"
    password = "@mlcheck2"
    loader = login(username, password)

    try:
        with open(filename, 'r') as file:
            usernames = [line.strip() for line in file]

        account_data = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            for data in executor.map(get_account_data, usernames, [loader] * len(usernames)):
                account_data.append(data)

        # This Saves the data to CSV file which is our test data
        save_to_csv(account_data, "fetched_data.csv")

        print("Data saved to 'fetched_data.csv'.")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

if __name__ == "__main__":
    main()
