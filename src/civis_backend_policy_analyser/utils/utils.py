from bs4 import BeautifulSoup


def strip_html_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    clean_text = soup.get_text()
    return clean_text