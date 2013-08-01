from bs4 import BeautifulSoup as BS

root = BS(open("out.html"))
print root.find_all(class_="title_9")
