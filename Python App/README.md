# Velocite Instascan: Instagram Fake Followers Checker

Velocite Instascan is a Flask web application developed to assist brands in evaluating the authenticity of Instagram influencers' followers. It provides insights into the percentage of followers that might be fake by analyzing the followers of a specific Instagram account.

## Installation

To use this app, simply follow these steps:
(follow steps 1-4 for the first time only)
1. **Clone Repository**: Clone or download this repository to your computer.
2. **Download Chrome**: Download chrome.rar folder from here https://bitly.cx/bfG move this rar to Python app folder and click on it and extract here.  

3. **Open Terminal**: Open Terminal in "Python App" folder. 

4. **Install Dependencies**: Install the required dependencies, You can do this by running this command in terminal `pip install Flask selenium webdriver-manager pandas requests beautifulsoup4 scikit-learn`.

5. **Launch the App**: Launch the Flask app by entering `python app.py` in terminal.

6. **Access the App**: Open your web browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000). Alternatively, click the link provided in the terminal when you run `python app.py`.

7. **Enter Instagram Username**: Enter the Instagram username of the influencer you want to analyze.(Account should not be private)

8. **Check Fake Followers**: Click the "Check Fake Followers" button once and wait 1-2 minutes for result.

9. **View Results**: The app will gather information about the followers of the specified Instagram account and assess their authenticity. Once the analysis is complete, you'll see the percentage of potentially fake followers displayed.

*Note: If you encounter any login issues in Automated Chrome or VALUE ERROR, you can use your own temporary Instagram account credentials in Line 34 and 35 of the `app.py` file.*

## Disclaimer

Velocite Instascan is created for educational and research purposes only. It relies on web scraping techniques and may be affected by changes in Instagram's website structure or policies. Please use this tool responsibly and always comply with Instagram's terms of service.

**Created by Rishabh Acharya**
