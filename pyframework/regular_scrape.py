import requests

from bs4 import BeautifulSoup


def scrape(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        extracted_content = soup.title.string
    except Exception:
        extracted_content = ""
        pass

    try:
        # Example: Extract all paragraphs from the webpage
        paragraphs = soup.find_all('p')
        for i, paragraph in enumerate(paragraphs, start=1):
            extracted_content += f"<p> {i}: {paragraph.text} </p>"

        # Extract all lists from the webpage
        # lists = soup.find_all(['ul', 'ol'])
        # for i, list_ in enumerate(lists, start=1):
        #     extracted_content += f"\n<ul> {i}:"
        #     items = list_.find_all('li')
        #     for j, item in enumerate(items, start=1):
        #         extracted_content += f"\n <li> {i}.{j}: {item.text} </li>"
        #     extracted_content += "\n</ul>"

        extracted_content += soup.get_text(separator='\n', strip=True)
    except Exception:
        pass

    return extracted_content
