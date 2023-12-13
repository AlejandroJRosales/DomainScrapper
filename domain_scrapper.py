import requests
from bs4 import BeautifulSoup

base_url = "https://your-domain.com"


def all_pages(base_url):
  print(f"scrapping all urls for: {base_url}")
  response = requests.get(base_url)
  unique_urls = {base_url}
  visited_urls = set()
  while len(unique_urls) > len(visited_urls):
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
      try:
        url = link["href"]
      except:
        continue
      if url[0] == "/" and "#" not in url:
        absolute_url = base_url + url
        unique_urls.add(absolute_url)

    unvisited_url = (unique_urls - visited_urls).pop()
    visited_urls.add(unvisited_url)
    response = requests.get(unvisited_url)

  print("Done.")
  return unique_urls


VALID_TAGS = ['p']


def get_text(url):
  print(f"scrapping: {url}")
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")

  lattex_out = ""
  indent_count = 1
  for data in soup.find_all(VALID_TAGS):
    p = data.get_text().replace("\\(", "$").replace("\\)", "$")
    for c in p:
      if ord(c) > 10:
        lattex_out += c
        indent_count = 0
      elif indent_count < 1:
        lattex_out += " "
        indent_count += 1
    indent_count = 1
    lattex_out += "\n"

  print("Done.")
  return lattex_out


all_urls = all_pages(base_url)
with open("output.txt", "w") as f:
  for url in all_urls:
    f.write(get_text(url))
    f.write("-----------\n")
  print("Entire Domain Scrapped.")
