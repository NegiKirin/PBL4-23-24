class Sorter:
    def __init__(self, sortName = None, sortBy = None):
        self.sortName = sortName
        self.sortBy = sortBy

class Searcher:
    def __init__(self, searchName = None, search = None):
        self.searchName = searchName
        self.search = search
class PageRequest:
    def __init__(self, page = None, maxPageItem = None):
        self.page = page
        self.maxPageItem = maxPageItem
        self.sorter = Sorter()
        self.searcher = Searcher()
    def getOffset(self):
        if self.page != None and self.maxPageItem != None:
            return (self.page-1)*self.maxPageItem
        return None
