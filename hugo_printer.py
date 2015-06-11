import yaml
import os
import logging
import html2text


class HugoPrinter:
    def __init__(self, *args, **kwargs):
        accept_attributes = ["meta", "categories", "tags", "posts", "drafts", "basedir"]

        for attr in accept_attributes:
            setattr(self, attr, None)

        for k, v in kwargs.items():
            if k in accept_attributes:
                setattr(self, k, v)

        if self.basedir:
            self.basedir = os.path.join(self.basedir, "hugo")
        else:
            self.basedir = os.path.join('.', "hugo")

        self.config_path = os.path.join(self.basedir, "config.yaml")
        self.post_dir = os.path.join(self.basedir, "content/post")

        self.__prepare_dir(self.basedir)
        self.__prepare_dir(self.post_dir)

    def __prepare_dir(self, dir_path):
        if not os.path.exists(dir_path):
            logging.warn("Directory %s not exists, creating it now..." % dir_path)
            os.makedirs(dir_path)
        elif not os.path.isdir(dir_path):
            logging.critical("%s is existing and not a dir" % dir_path)
            raise ValueError("%s is existing and not a dir" % dir_path)

    def author(self):
        try:
            return self.meta["author"]["name"]
        except KeyError:
            return ""

    def gen_config(self):
        if self.meta is None:
            return

        conf = {
            "baseurl": self.meta["baseurl"],
            "title": self.meta["title"],
            "languageCode": self.meta["language"],
            "params": {
                "Description": self.meta["description"],
                "Author": self.meta["author"]["name"],
                "AuthorEmail": self.meta["author"]["email"],
            },
        }

        with open(self.config_path, "w") as fp:
            fp.write(yaml.dump(conf, default_flow_style=False, explicit_start=True, allow_unicode=True))

    def gen_posts(self, download_assets=False):
        if self.posts is None:
            return

        for p in self.posts:
            meta_info = {
                "title": p["title"],
                "author": p["creator"],
                "categories": p["categories"],
                "tags": p["tags"],
                "date": 'T'.join(p["post_date"].split(' ')),
            }

            page_path = os.path.join(self.post_dir, "%s-%s.md" % (p["post_date"].split(" ")[0], p["post_name"]))

            more_tag = '<!--more-->'
            content = more_tag.join([self.__convert_to_markdown(data) for data in p["content"].split(more_tag)])

            with open(page_path, "w") as fp:
                fp.write(yaml.dump(meta_info, default_flow_style=False, explicit_start=True, allow_unicode=True))
                fp.write("---\n")
                fp.write(content)

    def __convert_to_markdown(self, content):
        if "<br" in content or '<p' in content:
            return html2text.html2text(content).strip()
        else:
            return content.strip()




