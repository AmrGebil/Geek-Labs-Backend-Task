import requests
from bs4 import BeautifulSoup
import re
import time

def scrape_twitter_account(account_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
    }
    response = requests.get(account_url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to fetch Twitter account:", account_url)
        return None

def extract_stock_mentions(html_content, stock_symbol):
    soup = BeautifulSoup(html_content, 'html.parser')
    cashtag_links = soup.find_all('a', {"class": re.compile(r'css-1qaijid')})
    mentions_count = 0
    for link in cashtag_links:
        link_text = link.get_text()
        if f"${stock_symbol}" in link_text:
            mentions_count += 1
    return mentions_count

def main():
    twitter_accounts = [
        "https://twitter.com/Mr_Derivatives",
        "https://twitter.com/warrior_0719",
        "https://twitter.com/ChartingProdigy",
        "https://twitter.com/allstarcharts",
        "https://twitter.com/yuriymatso",
        "https://twitter.com/TriggerTrades",
        "https://twitter.com/AdamMancini4",
        "https://twitter.com/CordovaTrades",
        "https://twitter.com/Barchart",
        "https://twitter.com/RoyLMattox"
    ]

    stock_symbol = input("Enter stock symbol (without $ sign): ")
    interval = int(input("Enter time interval for scraping (in minutes): "))

    while True:
        total_mentions = 0
        for account in twitter_accounts:
            html_content = scrape_twitter_account(account)
            if html_content:
                mentions_count = extract_stock_mentions(html_content, stock_symbol)
                total_mentions += mentions_count
                print(f"{account}: {mentions_count} mentions of ${stock_symbol}")

        print(f"\n${stock_symbol} was mentioned {total_mentions} times in the last {interval} minutes.\n")
        time.sleep(interval * 60)

if __name__ == "__main__":
    main()


