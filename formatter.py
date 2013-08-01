class Formatter(object):
    def __init__(self, orig_cont):
        self.orig_cont = orig_cont

    def format(self, **kwargs):
        self.do_format(**kwargs)

    def do_format(self, **kwargs):
        raise NotImplementedError("need implemented in child class")

class HtmlFormatter(Formatter):
    def do_format(self, **kwargs):
        cont = self.orig_cont
        tpl = """<html>
    <head>
        <title>Results for keyword: %(keyword)s</title>
    </head>
    <body>
        %(content)s
    </body>
</html>"""
        cont_tpl = """<div>
        <h3>%(id)s: <a href="%(link)s" target="_blank">%(title)s</a></h3>
        <p>%(content)s</p>
    </div>
"""
        content = ""
        i = 1
        num = kwargs.get('num', 10)
        for item in cont:
            if i > num: break
            item.update({
                "id" : i,
                })
            content += cont_tpl % item
            i += 1
        final_cont = tpl % {"keyword" : kwargs.get("keyword", ""), "content" : content}
        fh = open(kwargs.get("site_name") + "-" + kwargs.get("keyword") + ".html", "w")
        fh.write(final_cont)
        fh.close()
        

def get_formatter(formatter_type):
    if formatter_type == "html":
        return HtmlFormatter
