class File:
    
    def ReadNewlines(self, file_out, last_position):
        
        with open(file_out, 'r') as file:
            file.seek(last_position)
            new_content = file.read()
            new_lines   = new_content.split('. ') + new_content.split('! ') + new_content.split('? ')
            return new_lines, file.tell()
