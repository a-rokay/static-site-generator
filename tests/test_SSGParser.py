from ssg.SSGParser import get_txt_title, generate_content, generate_html
from ssg.SSGUtil import OUTPUT_FOLDER
import shutil
import os

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

OUTPUT_MD = (
    "<h1>h1</h1>\n"
    "<h2>h2</h2>\n"
    "<p><em>italics</em></p>\n"
    "<p><strong>bold</strong></p>\n"
    '<div class="codehilite"><pre><span></span><code><span class="k">def</span>'
    ' <span class="nf">function</span><span class="p">():</span>\n'
    '    <span class="k">return</span> <span class="mi">1</span>\n'
    "</code></pre></div>"
)


OUTPUT_TXT = """<h1>Silver Blaze</h1>


<p>I am afraid, Watson, that I shall have to go,” said Holmes, as we
sat down together to our breakfast one morning.
</p>"""


# 2 new lines, title should be found
def test_get_txt_title(tmp_path):
    TXT_CONTENT = """Silver Blaze
    

I am afraid, Watson, that I shall have to go,” said Holmes, as we
sat down together to our breakfast one morning."""

    (tmp_path / "test.txt").write_text(TXT_CONTENT, "UTF-8")
    title = get_txt_title(str(tmp_path) + "/test.txt")
    assert title == "Silver Blaze"


# 1 newline, title should not be found
def test_get_txt_title1(tmp_path):
    TXT_CONTENT = """Silver Blaze
    
I am afraid, Watson, that I shall have to go,” said Holmes, as we
sat down together to our breakfast one morning."""

    (tmp_path / "test.txt").write_text(TXT_CONTENT, "UTF-8")
    title = get_txt_title(str(tmp_path) + "/test.txt")
    assert title is None


# Should generate html content using markdown
def test_generate_content(tmp_path):
    OUT_FILE = str(tmp_path) + "/test.md"
    MD_CONTENT = """# h1
## h2

*italics*

**bold**

```python
def function():
    return 1
```"""

    if os.path.isdir(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)

    (tmp_path / "test.md").write_text(MD_CONTENT, "UTF-8")
    content = generate_content(OUT_FILE, None)

    assert content == OUTPUT_MD


# Should generate html content using txt file with title (2 new lines)
def test_generate_content1(tmp_path):
    OUT_FILE = str(tmp_path) + "/test.txt"
    TXT_CONTENT = """Silver Blaze


I am afraid, Watson, that I shall have to go,” said Holmes, as we
sat down together to our breakfast one morning."""

    (tmp_path / "test.txt").write_text(TXT_CONTENT, "UTF-8")
    content = generate_content(OUT_FILE, "Silver Blaze")

    assert content == OUTPUT_TXT


# Should generate html content using txt file with no title (1 new line)
def test_generate_content2(tmp_path):
    OUT_FILE = str(tmp_path) + "/test.txt"
    TXT_CONTENT = """Silver Blaze

I am afraid, Watson, that I shall have to go,” said Holmes, as we
sat down together to our breakfast one morning."""

    (tmp_path / "test.txt").write_text(TXT_CONTENT, "UTF-8")
    content = generate_content(OUT_FILE, None)

    assert content == OUTPUT_TXT.replace("h1", "p").replace("\n", "", 1)


# Should generate full html with title, stylesheet, and content
def test_generate_html():
    HTML_CONTENT = """
    <p>Hello world</p>
    """

    html = generate_html("en-US", "test.txt", "Title", "stylesheet.css", HTML_CONTENT)

    answer = html_skeleton.format(
        lang="en-US",
        title="Title",
        stylesheet='\n\t<link rel="stylesheet" href="{}">'.format("stylesheet.css"),
        content=HTML_CONTENT,
    )

    assert html == answer


# Should generate full html with no title, stylesheet, or content
def test_generate_html1():
    html = generate_html("en-US", "test.txt", None, None, None)

    answer = html_skeleton.format(
        lang="en-US",
        title="test.txt",
        stylesheet="",
        content="",
    )

    assert html == answer
