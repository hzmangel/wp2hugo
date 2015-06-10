class HugoPrinter:
    def __init__(self, *args, **kwargs):
        accept_attributes = ["meta", "categories", "tags", "posts", "drafts", "basedir"]

        for attr in accept_attributes:
            setattr(self, attr, None)

        for k, v in kwargs.items():
            if k in accept_attributes:
                setattr(self, k, v)

