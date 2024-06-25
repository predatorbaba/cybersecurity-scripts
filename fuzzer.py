import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

visited_urls = set()
curr_timestamp = time.time()
file_name = f"fuzzer-results-{curr_timestamp}.txt"

def fuzzer(url, keyword):
    try:
        response = requests.get(url)
    except:
        return
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        anchor_tags = soup.find_all("a")
        url_list = []
        for tag in anchor_tags:
            href_link = tag.get("href")
            if href_link not in url_list and href_link != "":
                url_list.append(href_link)
                
        for u in url_list:
            if u not in visited_urls:
                visited_urls.add(u)
                joined_url = urljoin(url, u)
                if keyword in joined_url:
                    print(joined_url)
                    with open(file_name, "a") as file:
                        file.write(joined_url)
                        file.write("\n")
                        file.close()
                    fuzzer(joined_url, keyword)
                    
            

target_url = input("Enter Target URL: ")
target_keyword = input("Enter Target Keyword: ")
print(f"Provided Target URL is {target_url} and Keyword is {target_keyword}\n")
fuzzer(target_url, target_keyword)