import os
from app.loop import Loop


if __name__ == "__main__":

    dir  = 'file_text_test'
    file = 'entrada.txt'

    dir_file = os.path.join(dir, file)
    time     = 10 

    loop = Loop(file, time)
    loop.mainLoop()