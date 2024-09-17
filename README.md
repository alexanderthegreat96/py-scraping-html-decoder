# HtmlDecoder

`HtmlDecoder` is a Python class designed to help web scrapers manage and process dynamically generated HTML class names. It transforms HTML content by replacing dynamic class names with consistent, predictable class names, making it easier to work with web scraping data. The class also provides options to clean up the HTML and generate a JSON representation of its structure.

## Features

- **Consistent Class Names:** Replace dynamic, unpredictable class names with static, consistent names for easier parsing.
- **HTML Parsing:** Parse and modify HTML content with BeautifulSoup.
- **Tag and Attribute Manipulation:** Replace class and ID attributes with new, predictable structures and remove style attributes.
- **Remove Unnecessary Tags:** Remove unwanted tags such as `<script>`, `<style>`, and others.
- **Comment Removal:** Eliminate all comments from the HTML content.
- **JSON Representation:** Generate a JSON tree structure of the HTML for easier analysis and manipulation.
- **Minification:** Option to return a minified version of the HTML to reduce size and improve processing speed.
- **Dump to File:** Optionally save the modified HTML to a file for further inspection or processing.

## Installation

To use `HtmlDecoder`, you need to have Python installed. You can then install the required libraries using pip:

```bash
pip install beautifulsoup4


## Usage
```pyhon
from html_decoder import HtmlDecoder

html_content = "<html>...</html>"  # Your HTML content here
tag_map = {"div": "container", "p": "paragraph"}  # Optional mapping of tags to class names

decoder = HtmlDecoder(html=html_content, tag_map=tag_map)



from html_decoder import HtmlDecoder

html_content = """
<html>
<head><title>Example</title></head>
<body>
    <div class="dynamic-class">
        <p>Sample paragraph</p>
    </div>
</body>
</html>
"""

tag_map = {"div": "container", "p": "text"}

decoder = HtmlDecoder(html=html_content, tag_map=tag_map)

# Get beautified HTML
print("Beautified HTML:")
print(decoder.get_html(beautify=True))

# Get minified HTML and save to file
print("Minified HTML:")
print(decoder.get_html(beautify=False, dump=True))

# Get JSON representation
print("JSON Representation:")
print(decoder.get_json())
```

