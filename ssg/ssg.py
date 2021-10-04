import argparse
import os
import shutil
import re
import json

OUTPUT_FOLDER = "dist"
ACCEPTED_FILE_TYPES = [".txt", ".md"]

html_skeleton = """<!doctype html>
<html lang="{lang}">
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
def get_accepted_files(folder_name):
    all_files = os.listdir(folder_name)
    filtered_files = filter(lambda f: is_file_accepted(f), all_files)
    return list(filtered_files)

def is_file_accepted(filename):
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
    if(not is_file_accepted(file_location)):
        return

    titled_format = "<h1>{}</h1>\n\n\n{}"
    content = ""
    
    with open(file_location, "r", encoding="utf8") as input_file:
        content = input_file.read()
    
    # Skip the first 3 lines if there's a title
    if(title):
        content = content.split("\n", 3)[3]

    content = "<p>" + content
    content = content.replace("\n\n", "</p>\n\n<p>")
    content = content + "\n</p>"

    if file_location.endswith(".md"):
        content = process_markdown(content)
    
    if(title):
        content = titled_format.format(title, content)
        
    return content

def process_markdown(content):
    # Process bold markdown
    content = re.sub('\*\*([^\s\*.].*?)\*\*|__([^\s_.].*?)__', r'<strong>\1</strong>', content, flags=re.DOTALL)
    
    # Process italic markdown
    content = re.sub('\*([^\s\*.].*?)\*|_([^\s\_.].*?)_', r'<em>\1\2</em>', content, flags=re.DOTALL)
    
    # Process single backtick markdown
    content = re.sub('`([^\r\n\`].*?)`', r'<code>\1</code>', content, flags=re.DOTALL)

    # Process header markdown
    headerTag = lambda s: '{endpTag}<h{size}>{regexContent}</h{size}>{pTag}'.format(endpTag="</p>\n\n" if s.group(1)=="\n" else "", size=s.group(2).count('#'), regexContent=s.group(3), pTag="\n\n<p>" if s.group(4)=="\n" else "")
    content = re.sub(r'(|(?<!\n)\n|<p>)(#{1,5})\s(.*)(<\/p>|(?<!<\/p>)\n|$)', headerTag, content)

    return content

# Inserts title, stylesheet, and content to html_skeleton, returns the result
def generate_html(lang, file_name, title, stylesheet, content):
    ss_tag = ""
    
    if(stylesheet):
        ss_tag = '\n\t<link rel="stylesheet" href="{}">'.format(stylesheet)
        
    return html_skeleton.format(lang=lang, title=title if title else file_name, stylesheet=ss_tag, content=content)
    
def output_to_file(file_name, html):
    # Create output folder if it doesn't exist
    if(not os.path.isdir(OUTPUT_FOLDER)):
        os.mkdir(OUTPUT_FOLDER)
    
    file_location = OUTPUT_FOLDER + "/" + file_name.replace(file_name[file_name.rfind("."):], ".html")
    with open(file_location, "w", encoding="utf8") as output_file:
        output_file.write(html)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Static Site Generator")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1", help="Show program's version number and exit")
    parser.add_argument("-i", "--input", help="Pass a file or folder of files")
    parser.add_argument("-s", "--stylesheet", help="URL to a stylesheet")
    parser.add_argument("-l", "--lang", help="Language to be set in root html tag", default="en")
    parser.add_argument("-c", "--config", help="Config file for arguments")
    args = parser.parse_args()

    if(os.path.isdir(OUTPUT_FOLDER)):
        shutil.rmtree(OUTPUT_FOLDER)

    # Check to see if config file exists.
    if args.config != None:
        with open(args.config) as f:
            try:
                data = json.load(f)
                if len(data) == 0:
                    print("\nConfig File is empty!\n")
                    exit(1)
            except (FileNotFoundError, RuntimeError, json.decoder.JSONDecodeError) as err:
                print("\nError parsing Config File: {0}\n".format(err))
                exit(1)
        # For each command from JSON config file, set local parameters
        for i in data:
            if i == "input" or i == "i":
                if os.path.isfile(data[i]):
                    input = data[i]
                elif os.path.isdir(data[i]):
                    input = data[i]
                else:
                    print("\nInput File gathered from Config does not exist\n")
            elif i == "stylesheet" or i == "s":
                if os.path.isfile(data[i]):
                    stylesheet = data[i]
                else:
                    print("\nStylesheet gathered from Config does not exist\n")
            elif i == "lang" or i == "l":
                lang = data[i]
        if input == None:
            print("No input file specified")
            exit(1)
        try:
            lang, stylesheet
        except NameError:
            lang = args.lang
            stylesheet = args.stylesheet
    else:
        lang = args.lang
        input = args.input
        stylesheet = args.stylesheet
    
    files = []
    folder = ""
    is_folder = os.path.isdir(input)
    
    if(is_folder):
        folder = input + "/"
        files = get_accepted_files(folder)
    else:
        if is_file_accepted(input):
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
            html = generate_html(lang, file, title, stylesheet, content)
            output_to_file(file, html)
