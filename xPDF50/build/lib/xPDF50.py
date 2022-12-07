from prepare import modify_html
from xhtml2pdf import pisa
import argparse
import re
import sys


"""
    Given a url of a cs50's web page with a project, a problem or lecture notes
    xPDF50 returns a clean PDF file of the main content of that page.

"""


def main():
    # User request at the command-line
    user_request = get_input()

    if url := is_valid(user_request):

        # Data related to user request
        course, year, material_name = unpack(url)

        # Altered html to get desired PDF
        html = modify_html(url, course, year, material_name)

        # Ship the pdf
        get_pdf(html, f"x{material_name.capitalize()}.pdf")


def get_input():
    """Gets input from user"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url",
        type=str,
        help="url of a web page containing cs50's problem|project|notes",
    )

    args = parser.parse_args()

    return args.url.lower()


def is_valid(url):
    """If contains cs50's domain, return as a full url path"""

    if matches := re.search(
        r"^(?:https://)?(?:www\.)?(cs50.harvard.edu/.+)$",
        url,
    ):

        # Ensure that a full url path is returned
        return f"https://{matches.group(1)}".removesuffix("/")

    else:
        sys.exit("hmm... looks like an invalid url    Try: project.py -h")


def unpack(url):
    """Extract and match data from the url"""

    if "notes" in url:
        try:
            matches = re.search(
                r"^https://.+/(.+)/(\d\d\d\d)/notes/(\d)$",
                url,
            )
            course, year, lesson_number = (
                matches.group(1),
                matches.group(2),
                matches.group(3),
            )

        except (AttributeError):
            return handle_uncharted(url)
        else:
            return course, year, f"lecture{lesson_number}"

    elif "psets" in url or "projects" in url:
        try:
            matches = re.search(
                r"^https://.+/(.+)/(\d\d\d\d)/.+/\d/(.+)$",
                url,
            )
            course, year, problem_or_project_name = (
                matches.group(1),
                matches.group(2),
                matches.group(3),
            )

        except (AttributeError):
            return handle_uncharted(url)
        else:
            return course, year, f"{problem_or_project_name}"
    elif "project" in url:
        return handle_uncharted(url)
    else:
        # If url is an unanticipated one
        sys.exit("Sorry... xPDF50 doesn't recognize this CS50 page    Try: project.py -h")


def handle_uncharted(url):
    """Handling data of unanticipated url with cs50.harvard.edu domain"""

    last_part = lambda path: path.split("/")[-1]

    return ".....", ".....", f"{last_part(url)}"


def get_pdf(source_html, output_filename):
    """Convert html to a pdf file using xhtml2pdf module"""

    pisa.showLogging()

    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(source_html, dest=result_file)

    # close output file
    result_file.close()

    # return False on success and True on errors
    return pisa_status.err


if __name__ == "__main__":
    main()
