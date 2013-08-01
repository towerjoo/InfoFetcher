import urllib2

import fetcher

class Newsmth(fetcher.Fetcher):
    def set_preq(self, *args, **kwargs):
        self.query_url = kwargs.get("query_url")
        self.keyword = kwargs.get("keyword")
        self.formatter = kwargs.get('formatter', 'html')
        self.item_num = kwargs.get("item_num", 10)
        
    def get_content(self):
        url = self.query_url % {"keyword" : self.keyword}
        self.orig_content = self._get_ajax_content(url)
        #print self.orig_content

    def _get_ajax_content(self, url):
        req = urllib2.Request(url)
        req.add_header("Host", "www.newsmth.net")
        req.add_header("X-Requested-With", "XMLHttpRequest")
        req.add_header("Referer", "http://www.newsmth.net/nForum/")
        req.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17")
        fh = urllib2.urlopen(req)
        cont = fh.read()
        fh.close()
        return cont

    def parse_content(self):
        import re
        rx = """<td class="title_9"><a href="([^"]+)">([^<]+)</a>"""
        #rx = """<td class="title_9"><a href="([^"]+)">(.*?)(?=</a>)</a>"""
        matches = re.findall(rx, self.orig_content, re.U)
        replies = re.findall("""<td class="title_11 middle">([0-9]+)</td>""", self.orig_content)
        i = 1
        for link, title in matches:
            if i > self.item_num: break
            url = "http://www.newsmth.net" + link
            print "fetching %s..." % url
            content = self._get_ajax_content(url)
            conts = re.findall("""<td class="a-content"><p>(.*?)(?=</p>)</p></td>""", content)
            content = conts[0]
            out = {
                "link" : url,
                "title" : title+"(" + replies[i-1] + ")",
                "content" : content,
                }
            self.parsed_content.append(out)
            i += 1
        
        
    def output_content(self):
        import formatter
        _formatter = formatter.get_formatter(self.formatter)(self.parsed_content)
        _formatter.format(keyword=self.keyword, site_name="NewSMTH")
        
        
        
if __name__ == "__main__":
    Boards = ["AutoWorld", "PocketLife"]
    board = raw_input("Input the board:(%s)" % ",".join(["%d:%s" %(Boards.index(x), x) for x in Boards]))
    keyword = raw_input("Input keywords:")
    query_url = "http://www.newsmth.net/nForum/s/article?ajax&t1=%(keyword)s&au=&b=" + Boards[int(board)]
    _fetcher = Newsmth(query_url=query_url, keyword=keyword)
    _fetcher.fetch()
