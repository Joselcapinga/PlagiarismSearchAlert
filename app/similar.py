class Similar:

    def Jaccard(self, paragrafo, paragrafos_encontrados):

        paragrafo2 = ''
        for p in paragrafos_encontrados:
            paragrafo2+= p

        # Dividir as strings em conjuntos de tokens (palavras)
        set1 = set(paragrafo.split())
        set2 = set(paragrafo2.split())

        # calcular a interseção

        intersection = len(set1.intersection(set2))

        # calcular a união
        uniao = len(set1) + len(set2) - intersection

        # calucar a união
        similaridade  = intersection / uniao
        similaridade = similaridade * 100
        return f"Percentual de similaridade: {similaridade: .2f} %."
    
    