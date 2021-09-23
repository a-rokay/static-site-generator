# Python Static Site Generator (SSG)
Uses python to generate static **html** files from a single **txt** or folder of **txt** files. 

# Prerequisites
* Python3

# Features
* Supports stylesheets. Pass the url of the stylesheet to ```-s``` or ```--stylesheet``` (See usage).
* Supports titles. If the first line is followed by two blank lines, it will be encased in an ```<h1>``` tag and set in ```<head>```.
* A blank line in the input file constitutes the end of a paragraph.
* Markdown files (`.md`) is supported for __bold text__ (`__example__` or `**example**`), _italic text_ (`_example_` or `*example*`) and headers (`# example` will become `<h1>example</h1>`)

# Example

###### example.txt
```
Custom title


This is a short paragraph.

This is a longer example
of a paragraph.
```

Becomes:

###### ./dist/example.html
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Custom title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<h1>Custom title</h1>


<p>This is a short paragraph.</p>

<p>This is a longer example
of a paragraph.</p>
</body>
</html>
```

# Usage
1. Passing a single text file:
```
ssg.py -i text.txt
```
2. Passing a folder. Only **txt** files will be parsed:
```
ssg.py -i folder
```
3. Passing a folder *and* providing a stylesheet:
```
ssg.py -i folder -s https://example.com/with/css.css
```

# Help
```
usage: ssg.py [-h] [-v] -i INPUT [-s STYLESHEET]

Static site generator

optional arguments:
  -h, --help                                show this help message and exit
  -v, --version                             show program's version number and exit
  -i INPUT, --input INPUT                   pass a .txt file or folder of .txt files
  -s STYLESHEET, --stylesheet STYLESHEET    URL to a stylesheet
```

##### --help/-h
Displays a list of arguments and what they do (above).

##### --version/-v
Displays the program name and version.

##### --input/-i
Required argument. Used to provide an input folder or file. Only **txt** files will be parsed in folders. See usage #1 and #2.

##### --stylesheet/-s
Optional argument. Pass a url to a stylesheet. See usage #3.

# Author
[Ahmad Rokay](https://dev.to/ar)
