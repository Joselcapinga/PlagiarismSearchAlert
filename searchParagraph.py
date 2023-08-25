from googlesearch import search
import requests

class SearchParagraph:

    def search_paragraph(self, text):

        search_query = f'"{text}"'

        results = search(search_query, num=1, lang="pt-BR", stop=1)

        for result in results:
            response = requests.get(result)
            if response.status_code == 200:
                return response.text

        return ""
