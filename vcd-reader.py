import re

class VcdReader:
    
    def __init__(self, filename):
        file = fopen(filename, "r")
        while True:
            line = readline()
            if len(line) == 0:
                break
            line = line.strip()
            mtime = re.search('^#(\d+)$', line)
            mwire = re.search('^$', line) # TODO
        fclose(file)
