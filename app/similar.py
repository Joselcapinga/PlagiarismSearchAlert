from googlesearch import search

class Similar():

    def LinksSimilar(self, query):
        
        search_results = []
        for i in search(query, num= 10, stop= 3, pause= 2):
            search_results.append(i)
        return search_results