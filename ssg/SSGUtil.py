import json
import os

OUTPUT_FOLDER = "dist"
ACCEPTED_FILE_TYPES = [".txt", ".md"]

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
    
def output_to_file(file_name, html):
    # Create output folder if it doesn't exist
    if(not os.path.isdir(OUTPUT_FOLDER)):
        os.mkdir(OUTPUT_FOLDER)
    
    file_location = OUTPUT_FOLDER + "/" + file_name.replace(file_name[file_name.rfind("."):], ".html")
    with open(file_location, "w", encoding="utf8") as output_file:
        output_file.write(html)

def get_config(config, input, lang, stylesheet):
    # Check to see if config file exists.
    if config:
        with open(config) as f:
            try:
                data = json.load(f)
                if len(data) == 0:
                    print("\nConfig File is empty!\n")
                    exit(1)
            except (json.decoder.JSONDecodeError) as err:
                print("\nError parsing Config File: {0}\n".format(err))
                exit(1)
        # For each command from JSON config file, set local variables
        for i in data:
            if i == "input" or i == "i":
                input = data[i]
            elif i == "stylesheet" or i == "s":
                stylesheet = data[i]
            elif i == "lang" or i == "l":
                lang = data[i]
        if input == None:
            print("No input file specified")
            exit(1)
    return input, lang, stylesheet