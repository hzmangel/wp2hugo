#!/usr/bin/env python3

import sys
from pprint import pprint
from lxml import etree
import html2text

from wp_parser import WordpressXMLParser
from hugo_printer import HugoPrinter


def main():
    wp_xml_parser = WordpressXMLParser(sys.argv[1])

    wp_site_info = {
        "meta": wp_xml_parser.get_meta(),
        "cats": wp_xml_parser.get_categories(),
        "tags": wp_xml_parser.get_tags(),
        "posts": wp_xml_parser.get_public_posts(),
        "drafts": wp_xml_parser.get_drafts(),
    }

    hugo_printer = HugoPrinter(**wp_site_info)
    hugo_printer.gen_config()

if __name__ == '__main__':
    main()

