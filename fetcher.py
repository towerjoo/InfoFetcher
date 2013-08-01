#coding:utf-8

class Fetcher(object):
    """The base class of fetcher
    """
    def __init__(self, *args, **kwargs):
        self.orig_content = ""
        self.parsed_content = []
        self.query_url = ""
        self.keyword = ""
        self.item_num = 10

        # set_preq will set the needed prequisite
        self.set_preq(*args, **kwargs)

    def set_preq(self, *args, **kwargs):
        raise NotImplementedError("Need to implement in child class")

    def fetch(self):
        self.get_content()
        self.parse_content()
        self.output_content()

    def get_content(self):
        raise NotImplementedError("Need to implement in child class")

    def parse_content(self):
        raise NotImplementedError("Need to implement in child class")
        
    def output_content(self):
        raise NotImplementedError("Need to implement in child class")
        
