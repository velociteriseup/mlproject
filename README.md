# Instagram Fake Followers Detection System

An automated solution for detecting fake Instagram followers using machine learning and web scraping. This project combines the power of Selenium for Instagram automation, BeautifulSoup for data extraction, and a Random Forest Classifier for predicting the authenticity of followers.

---

##  Project Objectives
- **Automate Instagram Data Collection**: Efficiently scrape and analyze Instagram account data.
- **Detect Fake Followers**: Use machine learning to identify potentially fake or bot accounts.
- **Present Results**: Display the percentage of fake followers in an intuitive web interface.

---

##  Key Features

- **Instagram Automation**: Automates login and follower scraping using Selenium.
- **Data Filtering**: Cleans and filters user data to ensure accurate predictions.
- **Machine Learning Integration**: Utilizes a pre-trained Random Forest Classifier for follower classification.
- **Web Application Interface**: Provides a user-friendly interface built with Flask.
- **Timeout and Error Handling**: Implements robust mechanisms for handling page load delays and unexpected errors.

---

## Tech Stack

### **Languages & Frameworks:**
- Python
- Flask
- Selenium
- BeautifulSoup
- Pandas
- Scikit-Learn

### **Tools:**
- ChromeDriver (for Selenium)
- WebDriver Manager

### **Machine Learning Model:**
- Random Forest Classifier (pre-trained in jupyter notebook and stored as `RF.pkl`)

---

## Workflow

1. **User Input:**
   - Enter the target Instagram username in the web application.
2. **Scraping Followers:**
   - Selenium logs in and scrapes followers and their information.
   - Data is saved to `file.txt`.
3. **Data Processing:**
   - Filter irrelevant usernames and clean the dataset.
   - Extract key metrics (posts, followers count, following count, following ratios, nums in username, length of bio).
4. **Fake Follower Prediction:**
   - Predicts the percentage of fake followers using the Random Forest Classifier.
   - Displays the result in the web interface.
5. **Data Cleanup:**
   - Deletes temporary files after processing to ensure a clean slate for future tasks.

---

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/Instagram-Fake-Followers-Detection.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Instagram-Fake-Followers-Detection
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download ChromeDriver:
   - [Download ChromeDriver](https://sites.google.com/chromium.org/driver/)
   - Place it in the `chrome` folder.
5. Run the Flask application:
   ```bash
   python app.py
   ```

---

## 🔧 Usage Instructions

1. Open the browser and navigate to `http://127.0.0.1:5000`.
2. Enter the Instagram username to analyze.
3. Click on submit to start the analysis.
4. View the results with the percentage of fake followers.

---

## 📂 Project Structure

```plaintext
.
|-- app.py                 # Flask application and main logic
|-- credentials.txt         # Stores Instagram login credentials
|-- file.txt                # Temporary storage for scraped followers
|-- RF.pkl                  # Pre-trained Random Forest Classifier
|-- templates/              # HTML templates for Flask
|   |-- index.html
|   |-- result.html
|-- requirements.txt        # List of Python dependencies
|-- user_data.csv           # Temporary CSV for storing scraped user data
|-- chrome/
|   |-- chrome.exe          # ChromeDriver for Selenium
```

---

## Security Note

- Instagram credentials are temporarily stored in `credentials.txt`. Handle with care and do not expose sensitive information.

---

