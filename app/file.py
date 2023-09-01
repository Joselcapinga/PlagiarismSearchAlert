class File:
    

    def create(self, fileMonitoring, fileSavedParagraphs):
        import os
        if not os.path.exists(fileMonitoring):
            with open(fileMonitoring, "w") as fileInput:
                pass
        if not os.path.exists(fileSavedParagraphs):
            with open(fileSavedParagraphs, "w") as fileInput:
                pass

    def ReadFile(self, file):
        with open(file, "r") as fileInput:
            content = fileInput.read()
            return content

    def WriteFile(self, content, file):
        try:
            with open(file, "w") as fileOut:
                fileOut.write(content)
                return 1
        except FileNotFoundError:
            return 0
        except IOError:
            return -1

    # identificar frases no arquivo
    def IdentifyParagraphs(self, contents):
        
        try:
            sentences = []
            current_sentence = ''
            sentence_delimiters = ['.', '!', '?']

            for char in contents:
                current_sentence += char
                if char in sentence_delimiters:
                    sentences.append(current_sentence.strip())
                    current_sentence = ''

            if current_sentence:
                sentences.append(current_sentence.strip())

            return sentences

        except FileNotFoundError:
            return []


    def CompareFiles(self, file1_path, file2_path):
        try:
            with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
                content1 = file1.read()
                content2 = file2.read()

                if content1 == content2:
                    return 1
                else:
                    return 0

        except FileNotFoundError:
            return -1

    def FileDiff(self, file1_path, file2_path):
        try:
            content1 = []
            content2 = []
            with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
                content1 = file1.readlines()
                content2 = file2.readlines()
                # Encontra as linhas diferentes entre os dois arquivos
                diff_lines = [line for line in content1 if line not in content2]
                return diff_lines
                
        except FileNotFoundError:
            return -1


    def SaveParagraphsToFile(self, file, paragraphs, links = None):
        try:

            if links is None:

                with open(file, "a") as fileOut:
                    fileOut.write(paragraphs + '\n')
            else:
                with open(file, "a") as fileOut:
                    fileOut.write(paragraphs + '\n')
                    for link in links:
                        fileOut.write(link + '\n')
                    fileOut.write('\n\n')
            return 1
        except FileNotFoundError:
            return 0
        except IOError:
            return -1
        
        