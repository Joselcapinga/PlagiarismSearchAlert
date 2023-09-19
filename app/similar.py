from googlesearch import search

class Similar():

    def LinksSimilar(self, query, numLinks = 5):
        
        search_results = []
        for i in search(query, num= 10, stop= numLinks, pause= 2):
            search_results.append(i)
        return search_results