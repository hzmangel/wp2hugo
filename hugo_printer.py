import yaml
import os
import logging


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

        if not os.path.exists(self.basedir):
            logging.warn("Directory %s not exists, creating it now..." % self.basedir)
            os.makedirs(self.basedir)
        elif not os.path.isdir(self.basedir):
            logging.critical("%s is existing and not a dir" % self.basedir)
            raise ValueError("%s is existing and not a dir" % self.basedir)

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

        with open(os.path.join(self.basedir, "config.yaml"), "w") as fp:
            fp.write(yaml.dump(conf, default_flow_style=False, explicit_start=True, allow_unicode=True))

