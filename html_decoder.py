from bs4 import BeautifulSoup, Comment
import json
import re


class HtmlDecoder:
    def __init__(self, html: str = None, tag_map: dict = None) -> None:
        """
        Initializes the HtmlDecoder with the optional tag map.

        :param html: The input HTML string to parse and modify.
        :param tag_map: A dictionary for mapping tag names to class names.
        """
        self._html = html

        self.tag_map = (
            tag_map
            if tag_map
            else {
                "div": "container",
                "p": "p",
                "span": "span",
                "ul": "ul",
                "li": "li",
                "ol": "ol",
                "table": "table",
                "tr": "tr",
                "td": "td",
                "th": "th",
                "a": "link",
                "img": "img",
                "section": "section",
            }
        )

        self.tags_to_remove = [
            "script",
            "style",
            "meta",
            "link",
            "svg",
            "iframe",
            "embed",
            "object",
            "noscript",
            "audio",
            "video",
            "track",
            "area",
            "map",
            "canvas",
            "applet",
            "param",
            "source",
            "base",
            "picture",
            "lazy-image-container",
        ]

        self.attributes_to_ignore = ["title", "target", "style"]

    def _remove_comments(self, soup):
        """
        Removes all comments from the BeautifulSoup object.

        :param soup: The BeautifulSoup object to process.
        """
        comments = soup.find_all(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

    def _get_class_name(self, tag, parent_classes):
        """
        Constructs the class name for the tag based on its type and its parent’s class names.
        Limits the depth of hierarchy to avoid overly long class names.

        :param tag: The current tag being processed.
        :param parent_classes: A list of class names of the parent tags.
        :return: The constructed class name.
        """
        tag_type = self.tag_map.get(tag.name, "default")
        limited_classes = parent_classes + [tag_type]
        return "-".join(limited_classes) + "-class"

    def _replace_attributes(self, tag, parent_classes):
        """
        Replaces the class and id attributes of a tag by prefixing them with 'fixed-' and their mapped value,
        and removes style attributes.

        :param tag: The current tag being processed.
        :param parent_classes: A list of class names of the parent tags.
        """
        class_name = self._get_class_name(tag, parent_classes)

        if "class" in tag.attrs:
            tag["class"] = [class_name]
        else:
            tag["class"] = [class_name]

        if self.attributes_to_ignore:
            for attr in self.attributes_to_ignore:
                if attr in tag.attrs:
                    del tag[attr]

    def _traverse_and_replace(self, tag, parent_classes):
        """
        Recursively traverses the HTML tree, replacing class and id attributes,
        and removing any unnecessary tags.

        :param tag: The current tag being processed.
        :param parent_classes: A list of class names of the parent tags.
        """
        if tag.name in self.tags_to_remove:
            tag.decompose()
            return

        self._replace_attributes(tag, parent_classes)

        current_classes = parent_classes + [self.tag_map.get(tag.name, "default")]

        children = []
        for child in tag.find_all(True, recursive=False):
            child_json = self._traverse_and_replace(child, current_classes)
            if child_json:
                children.append(child_json)

        return {
            "tag": tag.name,
            "class": tag.get("class", []),
            "attributes": {
                k: v for k, v in tag.attrs.items() if k not in self.attributes_to_ignore
            },
            "children": children,
        }

    def _generate_json(self) -> dict:
        """
        Generates a JSON representation of the HTML structure.

        :return: The JSON representation of the HTML structure.
        """
        if not self._html:
            raise ValueError("HTML content is not provided")

        soup = BeautifulSoup(self._html, "html.parser")
        self._remove_comments(soup)

        json_structure = []
        for tag in soup.find_all(True, recursive=False):
            tag_json = self._traverse_and_replace(tag, [])
            if tag_json:
                json_structure.append(tag_json)

        return json_structure

    def _minify_html(self, minified_html: str) -> str:
        minified_html = re.sub(r"\s+", " ", minified_html)
        minified_html = re.sub(r">\s<", "><", minified_html)
        minified_html = re.sub(r"(?<!\S)\s+|(?<=\S)\s+(?!\S)", "", minified_html)
        minified_html = re.sub(r"\s*([\[\]{}()|^$*+?.\\])\s*", r"\1", minified_html)
        minified_html = re.sub(r"<([a-z][a-z0-9]*)[^>]*>\s*</\1>", "", minified_html)
        minified_html = minified_html.strip()

        return minified_html

    def _dump_to_file(self, html: str = None) -> None:
        with open("dump.html", "w+") as f:
            f.write(html)
            f.close()

    def get_html(self, beautify: bool = False, dump=False) -> str:
        """
        Parses the HTML, replacing all class and id attributes, removing unnecessary tags,
        and comments, and removing style attributes.

        :param beautify: If True, returns the beautified (indented) HTML.
        :return: The modified HTML as a string.
        """
        if not self._html:
            raise ValueError("HTML content is not provided")

        soup = BeautifulSoup(self._html, "html.parser")

        self._remove_comments(soup)

        for tag in soup.find_all(True, recursive=False):
            self._traverse_and_replace(tag, [])

        result = soup.prettify() if beautify else self._minify_html(str(soup))
        if dump:
            self._dump_to_file(result)
        return result

    def get_json(self) -> str:
        """
        Returns a JSON representation of the HTML structure.

        :return: The JSON representation as a string.
        """
        json_structure = self._generate_json()
        return json.dumps(json_structure, indent=2)