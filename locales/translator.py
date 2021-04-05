from gettext import GNUTranslations
import itertools

from babel.messages.frontend import CommandLineInterface
import babel.support
from lxml import etree
import os

def simplify(text):
    before = "".join(itertools.takewhile(lambda x: x.isspace(), text))
    after = "".join(reversed(list(itertools.takewhile(lambda x: x.isspace(), reversed(text)))))
    middle = " ".join([x.strip() for x in text.strip().split("\n")])
    return (before, middle, after) if middle != "" else None


def process(fname, translate):
    """
    For all translatable string in the HTML file fname, call the translate function with it, and put the return
    value of translate inside the tree.
    :param fname: HTML file path
    :param translate:  translate function. takes a string to be translated and a line number, returns a translated string.
    :returns: translated HTML
    """
    tree = etree.parse(fname, parser=etree.HTMLParser())
    for element in tree.iter():
        if element.tag not in ["script"] and element.text is not None and (text := simplify(element.text)) is not None:
            element.text = text[0] + translate(text[1], element.sourceline) + text[2]
        if element.tail is not None and (text := simplify(element.tail)) is not None:
            element.tail = text[0] + translate(text[1], element.sourceline) + text[2]
        if element.tag == "input" and "placeholder" in element.attrib:
            element.attrib["placeholder"] = translate(element.attrib["placeholder"], element.sourceline)
        if element.tag == "a":
            element.attrib["href"] = translate(element.attrib["href"], element.sourceline)
        if element.tag == "form":
            element.attrib["action"] = translate(element.attrib["action"], element.sourceline)
    return etree.tostring(tree, method="html", pretty_print=True, encoding='unicode')


def pybabel_extract_html(fileobj, keywords, comment_tags, options):
    out = []
    def translate(s, l):
        out.append((l or 0, "_", s, []))
        return s
    process(fileobj, translate)
    return out


if __name__ == '__main__':
    files = ["index.html", "qr.html", "r.html", "s.html"]
    lang = {"fr": "", "nl": "n"}
    for lang, prefix in lang.items():
        CommandLineInterface().run(['pybabel', 'compile', '-i', f"../locales/{lang}.po", '-o', f"../locales/{lang}.mo", '-l', lang])
        translator = babel.support.Translations(open(f"../locales/{lang}.mo", "rb"))
        def translate(s, l):
            return translator.gettext(s)
        for f in files:
            open(f"../{prefix}{f}", "w").write(process(open(f"../base/{f}", 'r'), translate))
        os.remove(f"../locales/{lang}.mo")
