import argparse
import os
import shutil
import re

OUTPUT_FOLDER = "dist"
ACCEPTED_FILE_TYPES = [".txt", ".md"]

html_skeleton = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">{stylesheet}
</head>
<body>
{content}
</body>
</html>
"""

# Returns a list of files with acceptable file types by filtering all files in folder_name
def get_all_files(folder_name):
    all_files = os.listdir(folder_name)
    filtered_files = filter(lambda f: filter_files(f), all_files)
    return list(filtered_files)

def filter_files(filename):
    for type in ACCEPTED_FILE_TYPES:
        if filename.endswith(type):
            return True
    return False

# Returns None if no title is found
def get_txt_title(file_location):
    title = None
    first_3_lines = []
    i = 0
    
    # Read file line by line, up to line 3
    with open(file_location, "r", encoding="utf8") as input_file:
        while(line := input_file.readline()):
        
            if(i == 3):
                break
                
            cleaned_line = line.rstrip()
            first_3_lines.append(cleaned_line)
            i += 1
    
    # Check if title criteria is met
    if(len(first_3_lines) == 3):
        if(first_3_lines[0] and not first_3_lines[1] and not first_3_lines[2]):
            title = first_3_lines[0]

    return title

# Returns html content, including title, if set
def generate_content(file_location, title):
    if(not filter_files(file_location)):
        return

    titled_format = "<h1>{}</h1>\n\n\n{}"
    content = ""
    
    with open(file_location, "r", encoding="utf8") as input_file:
        content = input_file.read()
    
    # Skip the first 3 lines if there's a title
    if(title):
        content = content.split("\n", 3)[3]
    
    # old paragraph algo, might create unclosed <p> tags
    # content = "<p>" + content
    # content = content.replace("\n\n", "</p>\n\n<p>")
    # content = content + "\n</p>"

    if file_location.endswith(".md"):
        title, content = process_markdown(content, title)

    content = paragraphWrap(content)
    
    if(title):
        content = titled_format.format(title, content)
        
    return content

def paragraphWrap(content):
    newContent = []
    for paragraph in content.split("\n\n"):
        newContent.append("<p>{}</p>".format(paragraph))
    return "\n\n".join(newContent)

def process_markdown(content, title):
    content = re.sub(r'(__[^\r\n]*__)|(\*\*[^\r\n]*\*\*)', lambda s: "<b>{}</b>".format(s[0][2:-2]), content)
    print(content)
    content = re.sub(r'(_[^\n\r]+_)|(\*[\n\r]*\*)', lambda s: "<i>{}</i>".format(s[0][1:-1]), content)

    headerRegex = r'(<.*>)?#{1,5}\s\S.*\r?\n'
    firstline = content.split("\n", 2)[0]
    if (re.search(headerRegex, firstline)):
        title = firstline[firstline.rfind("# ") + 1:]
    
    content = re.sub(headerRegex, headerWrap, content)
    return title, content

def headerWrap(content):
    headerSize = content[0][0: content[0].find(" ")].count('#')
    return "<h{size}>{content}</h{size}>\n".format(size=headerSize, content=re.sub(r'(<.*>)?#+\s', "", content[0][0: content[0].find("\n")]))

# Inserts title, stylesheet, and content to html_skeleton, returns the result
def generate_html(file_name, title, stylesheet, content):
    ss_tag = ""
    
    if(stylesheet):
        ss_tag = '\n\t<link rel="stylesheet" href="{}">'.format(stylesheet)
        
    return html_skeleton.format(title=title if title else file_name, stylesheet=ss_tag, content=content)
    
def output_to_file(file_name, html):
    # Create output folder if it doesn't exist
    if(not os.path.isdir(OUTPUT_FOLDER)):
        os.mkdir(OUTPUT_FOLDER)
    
    file_location = OUTPUT_FOLDER + "/" + file_name.replace(file_name[file_name.rfind("."):], ".html")
    with open(file_location, "w", encoding="utf8") as output_file:
        output_file.write(html)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Static site generator")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1", help="show program's version number and exit")
    parser.add_argument("-i", "--input", help="pass a .txt file or folder of .txt files", required=True)
    parser.add_argument("-s", "--stylesheet", help="URL to a stylesheet")
    args = parser.parse_args()
    
    if(os.path.isdir(OUTPUT_FOLDER)):
        shutil.rmtree(OUTPUT_FOLDER)

    input = args.input
    stylesheet = args.stylesheet
    
    files = []
    folder = ""
    is_folder = os.path.isdir(input)
    
    if(is_folder):
        folder = input + "/"
        files = get_all_files(folder)
    else:
        if filter_files(input):
            files.append(input)
        else:
            print("Invalid file type!")
            print("Current accepted file types are: " + ", ".join(ACCEPTED_FILE_TYPES))
    
    for file in files:
        file_location = folder + file
        title = get_txt_title(file_location) if file_location.endswith(".txt") else None
        content = generate_content(file_location, title)
        # Make sure content was generated (file not skipped)
        if(content):
            html = generate_html(file, title, stylesheet, content)
            output_to_file(file, html)
