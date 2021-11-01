import SSGUtil
import markdown
from pygments.formatters import HtmlFormatter

html_skeleton = """<!doctype html>
<html lang="{lang}">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="../assets/css/pygments.css">{stylesheet}
</head>
<body>
{content}
</body>
</html>
"""


# Returns None if no title is found
def get_txt_title(file_location):
    title = None
    first_3_lines = []
    i = 0

    # Read file line by line, up to line 3
    with open(file_location, "r", encoding="utf8") as input_file:
        while line := input_file.readline():

            if i == 3:
                break

            cleaned_line = line.rstrip()
            first_3_lines.append(cleaned_line)
            i += 1

    # Check if title criteria is met
    if len(first_3_lines) == 3:
        if first_3_lines[0] and not first_3_lines[1] and not first_3_lines[2]:
            title = first_3_lines[0]

    return title


# Returns html content, including title, if set
def generate_content(file_location, title):
    if not SSGUtil.is_file_accepted(file_location):
        return

    titled_format = "<h1>{}</h1>\n\n\n{}"
    content = ""

    with open(file_location, "r", encoding="utf8") as input_file:
        content = input_file.read()

    if file_location.endswith(".md"):
        # Formatter for code blocks
        formatter = HtmlFormatter(cssclass="codehilite")
        # Will not add if the asset already exists
        SSGUtil.add_asset("css", "pygments.css", formatter.get_style_defs())

        content = process_markdown(content)
    else:
        # Skip the first 3 lines if there's a title
        if title:
            content = content.split("\n", 3)[3]

        content = "<p>" + content
        content = content.replace("\n\n", "</p>\n\n<p>")
        content = content + "\n</p>"

        if title:
            content = titled_format.format(title, content)

    return content


def process_markdown(content):
    return markdown.markdown(
        content, extensions=["fenced_code", "codehilite", "tables"]
    )


# Inserts title, stylesheet, and content to html_skeleton, returns the result
def generate_html(lang, file_name, title, stylesheet, content):
    ss_tag = ""

    if stylesheet:
        ss_tag = '\n\t<link rel="stylesheet" href="{}">'.format(stylesheet)

    return html_skeleton.format(
        lang=lang,
        title=title if title else file_name,
        stylesheet=ss_tag,
        content=content,
    )
