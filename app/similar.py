from googlesearch import search
import requests
import difflib
import time

class Similar():


    # Função para calcular a porcentagem de semelhança entre duas strings
    def similarity_percentage(self, query, content):
        
        query = query.lower()
        content = content.lower()
        seq = difflib.SequenceMatcher(None, query, content)
        return seq.ratio() * 100
    
    
    # Itera pelos links e verifica a porcentagem de semelhança
    def ConteudoSite(self, link, query):

        percentage = 0.0

        # try:
        response = requests.get(link)
        content = response.text
        percentage = self.similarity_percentage(query, content)
        # print(f"Link: {link}")
        # print(f"Porcentagem de semelhança: {percentage:.2f}%")
        # print("-" * 50) 
        # except Exception as e:
        return f"Porcentagem de semelhança: {percentage:.2f}%"
        
        # return percentage

    # 
    def LinksSimilar(self, query, numLinks = 5):
        
        search_results = []
                
        for i in search(query, num= 10, stop= numLinks, pause= 2): 
            percentual = self.ConteudoSite(i, query)
            search_results.append(i)
            search_results.append(percentual)
        return search_results

