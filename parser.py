from bs4 import BeautifulSoup


def parse_date(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    active_date = soup.find('li', {"class": "active"})
    if active_date:
        return active_date.get('data-id')
