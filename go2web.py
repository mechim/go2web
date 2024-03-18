import argparse
import requests
from bs4 import BeautifulSoup


def main():
    print ("Command:")
    arg = input()
    if (arg == "u"):
        print("URL: ")
        url = input()
        print("Response: ")
        fetch_url(url)
 
    if (arg == "s"):
        print("Search Term: ")
        search = input()
        print("Results: ")
        search_web(search)
    
    if (arg == "h"):
        print(" u - html request \n s - search the web")


def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for unsuccessful requests
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(separator="\n")
        print(text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching url: {e}")


def search_web(search_term):
    # Replace this with your favorite search engine URL with "{}" as placeholder for search term
    search_url = f"https://www.google.com/search?q={search_term}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # This extracts top 10 results based on a sample google search result structure, you might need to adjust this based on your chosen search engine
        results = soup.find_all("a", href=lambda href: href and href.startswith("/url?q="))[:10]
        i = 0
        for result in results:
            i+=1
            print(i+": ")
            print(result.get_text())
    except requests.exceptions.RequestException as e:
        print(f"Error searching the web: {e}")


if __name__ == "__main__":
    main()
