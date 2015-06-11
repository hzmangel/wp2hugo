from lxml import etree


class WordpressXMLParser:
    def __init__(self, xml_file):
        self.tree = etree.parse(xml_file)
        self.ns = self.tree.getroot().nsmap

    def get_meta(self):
        return {
            "title": str(self.tree.xpath("/rss/channel/title/text()")[0]),
            "baseurl": str(self.tree.xpath("/rss/channel/link/text()")[0]),
            "description": str(self.tree.xpath("/rss/channel/description/text()")[0]),
            "language": str(self.tree.xpath("/rss/channel/language/text()")[0]),
            "author": {
                "name": str(self.tree.xpath("/rss/channel/wp:author/wp:author_display_name/text()", namespaces=self.ns)[0]),
                "email": str(self.tree.xpath("/rss/channel/wp:author/wp:author_email/text()", namespaces=self.ns)[0]),
            }
        }

    def get_categories(self):
        categories = self.tree.xpath('/rss/channel/wp:category', namespaces=self.ns)
        rslt = []

        for r in categories:
            rslt.append({
                "term_id": str(r.xpath("wp:term_id/text()", namespaces=self.ns)[0]),
                "nicename": str(r.xpath("wp:category_nicename/text()", namespaces=self.ns)[0]),
                "name": str(r.xpath("wp:cat_name/text()", namespaces=self.ns)[0]),
            })

        return rslt

    def get_tags(self):
        tags = self.tree.xpath('/rss/channel/wp:tag', namespaces=self.ns)
        rslt = []

        for r in tags:
            rslt.append({
                "term_id": str(r.xpath("wp:term_id/text()", namespaces=self.ns)[0]),
                "nicename": str(r.xpath("wp:tag_slug/text()", namespaces=self.ns)[0]),
                "name": str(r.xpath("wp:tag_name/text()", namespaces=self.ns)[0]),
            })

        return rslt

    def get_public_posts(self):
        posts = self.tree.xpath("/rss/channel/item[wp:post_type='post' and wp:status!='draft']", namespaces=self.ns)
        rslt = []

        for r in posts:
            rslt.append({
                "title": str(r.xpath("title/text()")[0]),
                "link": str(r.xpath("link/text()")[0]),
                "creator": str(r.xpath("dc:creator/text()", namespaces=self.ns)[0]),
                "content": str(r.xpath("content:encoded/text()", namespaces=self.ns)[0]),
                "post_date": str(r.xpath("wp:post_date/text()", namespaces=self.ns)[0]),
                "post_name": str(r.xpath("wp:post_name/text()", namespaces=self.ns)[0]),
                "post_status": str(r.xpath("wp:status/text()", namespaces=self.ns)[0]),
                "categories": [str(foo) for foo in r.xpath("category[@domain='category']/text()")],
                "tags": [str(foo) for foo in r.xpath("category[@domain='post_tag']/text()")],
            })

        return rslt

    def get_drafts(self):
        drafts = self.tree.xpath("/rss/channel/item[wp:post_type='post' and wp:status='draft']", namespaces=self.ns)
        rslt = []

        for r in drafts:
            rslt.append({
                "title": str(r.xpath("title/text()")[0]),
                "link": str(r.xpath("link/text()")[0]),
                "creator": str(r.xpath("dc:creator/text()", namespaces=self.ns)[0]),
                "content": str(r.xpath("content:encoded/text()", namespaces=self.ns)[0]),
                "post_date": str(r.xpath("wp:post_date/text()", namespaces=self.ns)[0]),
                "post_status": str(r.xpath("wp:status/text()", namespaces=self.ns)[0]),
                "categories": [str(foo) for foo in r.xpath("category[@domain='category']/text()")],
                "tags": [str(foo) for foo in r.xpath("category[@domain='post_tag']/text()")],
            })

        return rslt


