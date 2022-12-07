from PIL import Image
import re
import requests
import sys


def modify_html(url, course, year, lesson):
    """Modify raw html to get desired PDF using xhtml2pdf module"""

    template = get_template()
    content = extract_content(url)
    footer = f'<div id="footer_content">CS50/{course}/{year}/{lesson} (Page: <pdf:pagenumber>)</div>'

    return template + footer + content


def get_template():
    """Template html file as a string"""

    template = ""

    with open("template.html") as file:
        for line in file:
            template += line

    return template


def extract_content(url):
    """Extracting only the required content from html and convert it to a string"""

    try:
        html = requests.get(url, timeout=0.900)

        # Check if request response status is ok
        if html.status_code != requests.codes.ok:
            sys.exit("hmm... something is not right")

    except requests.exceptions.Timeout:
        sys.exit("cs50.harvard.edu took too long to respond")

    html = edit_tags(html.text, url)

    # Extracting from html's h1 tag onwards until </body> tag
    if matches := re.search(
        r'.+(<h1.+</body>).+',
        html,
        re.DOTALL,
    ):
        extracted_html = matches.group(1)

    return extracted_html.replace("â", "'")


def edit_tags(html, url):
    '''Remove or replace html tags to suit pdf format'''

    # Replace img src with full url path
    html = re.sub(r'<img.src="(.+)".alt=".+">', rf'<img src="{url}/\1">', html)

    # Removing video tags
    html = re.sub(r'<div class="ratio.+></iframe></div>', " ", html)

    # Removing demo
    html = re.sub(r'<h2.id="demo">Demo</h2>', " ", html)
    html = re.sub(r'<script async="".+</script>', " ", html
    )

    return html


def main():
    ...


if __name__ == "__main__":
    main()