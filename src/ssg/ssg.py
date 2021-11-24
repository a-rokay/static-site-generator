import argparse
import os
import shutil
import SSGParser
import SSGUtil

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Static Site Generator")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 0.1",
        help="Show program's version number and exit",
    )
    parser.add_argument("-i", "--input", help="Pass a file or folder of files")
    parser.add_argument("-s", "--stylesheet", help="URL to a stylesheet")
    parser.add_argument(
        "-l", "--lang", help="Language to be set in root html tag", default="en"
    )
    parser.add_argument("-c", "--config", help="Config file for arguments")
    args = parser.parse_args()

    if os.path.isdir(SSGUtil.OUTPUT_FOLDER):
        shutil.rmtree(SSGUtil.OUTPUT_FOLDER)

    lang = args.lang
    input = args.input
    stylesheet = args.stylesheet

    input, lang, stylesheet = SSGUtil.get_config(args.config, input, lang, stylesheet)

    files = []
    folder = ""
    is_folder = os.path.isdir(input)

    if is_folder:
        folder = input + "/"
        files = SSGUtil.get_accepted_files(folder)
    else:
        if SSGUtil.is_file_accepted(input):
            files.append(input)
        else:
            print("Invalid file type!")
            print(
                "Current accepted file types are: "
                + ", ".join(SSGUtil.ACCEPTED_FILE_TYPES)
            )

    SSGUtil.create_output_dir()

    for file in files:
        file_location = folder + file
        title = (
            SSGParser.get_txt_title(file_location)
            if file_location.endswith(".txt")
            else None
        )
        content = SSGParser.generate_content(file_location, title)
        # Make sure content was generated (file not skipped)
        if content:
            html = SSGParser.generate_html(lang, file, title, stylesheet, content)
            SSGUtil.output_to_file(file, html)
