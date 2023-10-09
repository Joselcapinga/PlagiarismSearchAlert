from googlesearch import search
import requests
import json


class Similar():


    def CheckConteudoLink(self, link, query):
        
        try:

            data = {
                'link':  link,
                'query': query
            }
            
            url = 'http://localhost:8080/processar_link'
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers)

            if response.status_code != 200:
                return []
            
            json_data = response.json()
            mensagem = json_data.get('mensagem')    

            return mensagem

        except:
            return []

    def LinksSimilar(self, query, numLinks = 5):
        
        search_results = []
                
        for i in search(query, tld="co.in", num= 10, stop= numLinks, pause= 2): 
           
            # if self.CheckConteudoLink(i, query) == True:
            #     search_results.append("Parágrafo encontrado no link abaixo")
            #     search_results.append(i)
                
            # else:
            #     search_results.append("Verifica o link abaixo com suposta similaridade: ")
                search_results.append(i)

        return search_results