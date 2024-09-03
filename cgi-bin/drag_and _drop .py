#!/usr/bin/env python3

import sys

# Print necessary headers
print("Content-Type: text/html\n")

# Path to the HTML file
html_file_path = '/path/to/drag_and_drop.html'

# Read the content of the HTML file
try:
    with open(html_file_path, 'r') as file:
        html_content = file.read()
except FileNotFoundError:
    html_content = "<html><body><h1>File not found: {}</h1></body></html>".format(html_file_path)

# Print the HTML content to STDOUT
sys.stdout.write(html_content)
