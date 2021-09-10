# Python Static Site Generator (SSG)
Uses python to generate static **html** files from a single **txt** or folder of **txt** files. 

# Features
* Supports stylesheets. Pass the url of the stylesheet to ```-s``` or ```--stylesheet``` (See usage).
* Supports titles. If the first line is followed by two blank lines, it will be encased in an ```<h1>``` tag and set in ```<head>```.
* A new line in the input file constitutes the end of a paragraph.

# Example

###### example.txt
```
Custom title


This is a short paragraph.

This is a longer example
of a paragraph.
```

Becomes:

###### example.html
```html
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Custom title</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">{stylesheet}
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
```
ssg.py -i text.txt
ssg.py -i folder
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

# Author
[Ahmad Rokay](https://dev.to/ar)
