import sys

class Properties:
    props = None

    def load_properties(self, filepath, sep='=', comment_char='#'):
        self.props = {}
        with open(filepath, "rt") as f:
            for line in f:
                l = line.strip()
                if l and not l.startswith(comment_char):
                    key_value = l.split(sep)
                    key = key_value[0].strip()
                    value = sep.join(key_value[1:]).strip().strip('"') 
                    self.props[key] = value 

    def get(self, propertyName):
        return self.props[propertyName]
		

if __name__ == "__main__":
	properties = Properties()
	properties.load_properties('locations.properties')
	print (properties.get(sys.argv[1]))