class Article:
    def __init__(self, title, link, author, date, content, img,
                 enclosures=None):
        self.title = title
        self.link = link
        self.author = author
        self.date = date
        self.content = content
        self.img = img
        self.enclosures = enclosures
