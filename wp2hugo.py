#!/usr/bin/env python3

import sys
from pprint import pprint
from lxml import etree


class WordpressXMLParser:
    def __init__(self, xml_file):
        self.tree = etree.parse(xml_file)
        self.ns = self.tree.getroot().nsmap

    def get_meta(self):
        return {
            "title": self.tree.xpath("/rss/channel/title/text()")[0],
            "link": self.tree.xpath("/rss/channel/link/text()")[0],
            "description": self.tree.xpath("/rss/channel/description/text()")[0],
            "pub_date": self.tree.xpath("/rss/channel/pubDate/text()")[0],
            "language": self.tree.xpath("/rss/channel/language/text()")[0],
        }

    def get_categories(self):
        categories = self.tree.xpath('/rss/channel/wp:category', namespaces=self.ns)
        rslt = []

        for cat in categories:
            rslt.append({
                "term_id": cat.xpath("wp:term_id/text()", namespaces=self.ns)[0],
                "nicename": cat.xpath("wp:category_nicename/text()", namespaces=self.ns)[0],
                "name": cat.xpath("wp:cat_name/text()", namespaces=self.ns)[0],
            })

        return rslt

    def get_tags(self):
        tags = self.tree.xpath('/rss/channel/wp:tag', namespaces=self.ns)
        rslt = []

        for tag in tags:
            rslt.append({
                "term_id": tag.xpath("wp:term_id/text()", namespaces=self.ns)[0],
                "nicename": tag.xpath("wp:tag_slug/text()", namespaces=self.ns)[0],
                "name": tag.xpath("wp:tag_name/text()", namespaces=self.ns)[0],
            })

        return rslt

    def get_public_posts(self):
        posts = self.tree.xpath("/rss/channel/item[wp:post_type='post' and wp:status!='draft']", namespaces=self.ns)
        rslt = []

        for post in posts:
            rslt.append({
                "title": post.xpath("title/text()")[0],
                "link": post.xpath("link/text()")[0],
                "creator": post.xpath("dc:creator/text()", namespaces=self.ns)[0],
                "content": post.xpath("content:encoded/text()", namespaces=self.ns)[0],
                "post_date_gmt": post.xpath("wp:post_date_gmt/text()", namespaces=self.ns)[0],
                "post_name": post.xpath("wp:post_name/text()", namespaces=self.ns)[0],
                "post_status": post.xpath("wp:status/text()", namespaces=self.ns)[0],
                "categories": post.xpath("category[@domain='category']/text()"),
                "tags": post.xpath("category[@domain='post_tag']/text()"),
            })

        return rslt

    def get_drafts(self):
        posts = self.tree.xpath("/rss/channel/item[wp:post_type='post' and wp:status='draft']", namespaces=self.ns)
        rslt = []

        for post in posts:
            rslt.append({
                "title": post.xpath("title/text()")[0],
                "link": post.xpath("link/text()")[0],
                "creator": post.xpath("dc:creator/text()", namespaces=self.ns)[0],
                "content": post.xpath("content:encoded/text()", namespaces=self.ns)[0],
                "post_date_gmt": post.xpath("wp:post_date_gmt/text()", namespaces=self.ns)[0],
                "post_status": post.xpath("wp:status/text()", namespaces=self.ns)[0],
                "categories": post.xpath("category[@domain='category']/text()"),
                "tags": post.xpath("category[@domain='post_tag']/text()"),
            })

        return rslt


def main():
    wp_xml_parser = WordpressXMLParser(sys.argv[1])

    meta = wp_xml_parser.get_meta()
    cats = wp_xml_parser.get_categories()
    tags = wp_xml_parser.get_tags()
    posts = wp_xml_parser.get_public_posts()
    drafts = wp_xml_parser.get_drafts()

    pprint(drafts[-1])

if __name__ == '__main__':
    main()

