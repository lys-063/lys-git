class EntityTracker():
    def __init__(self):
        self.db_root = 'db/'
        self.entities = {
            '<name>': None,
            '<cuisine>': None,
            '<location>': None,
            '<number>': None,
            '<price>': None,
            '<phone>': None,
            '<post_code>': None
        }
        f = open(self.db_root + 'names.txt', 'r')
        names = f.read()
        self.names = eval(names)
        f = open(self.db_root + 'cuisines.txt', 'r')
        cuisines = f.read()
        self.cuisines = eval(cuisines)
        f = open(self.db_root + 'locations.txt', 'r')
        locations = f.read()
        self.locations = eval(locations)
        f = open(self.db_root + 'prices.txt', 'r')
        prices = f.read()
        self.prices = eval(prices)
        f = open(self.db_root + 'phones.txt', 'r')
        phones = f.read()
        self.phones = eval(phones)
        f = open(self.db_root + 'post_codes.txt', 'r')
        post_codes = f.read()
        self.post_codes = eval(post_codes)
        f.close()

    def extract_entity(self, sentence):
        s = []
        for word in sentence:
            if word in self.names:
                self.entities['<name>'] = word
                s.append('<name>')
            elif word in self.cuisines:
                self.entities['<cuisine>'] = word
                s.append('<cuisine>')
            elif word in self.locations:
                self.entities['<location>'] = word
                s.append('<location>')
            elif word in self.prices:
                self.entities['<price>'] = word
                s.append('<price>')
            elif word in self.phones:
                self.entities['<phone>'] = word
                s.append('<phone>')
            elif word in self.post_codes:
                self.entities['<post_code>'] = word
                s.append('<post_code>')
            else:
                if '_' in word:
                    if '_cuisine' in word:
                        self.entities['<cuisine>'] = word
                        if word not in self.cuisines:
                            self.cuisines.append(word)
                        s.append('<cuisine>')
                    elif '_address' in word or '_location' in word:
                        self.entities['<location>'] = word
                        if word not in self.locations:
                            self.locations.append(word)
                        self.locations.append(word)
                        s.append('<location>')
                    elif '_price' in word:
                        self.entities['<price>'] = word
                        if word not in self.prices:
                            self.prices.append(word)
                        s.append('<price>')
                    elif '_phone' in word:
                        self.entities['<phone>'] = word
                        if word not in self.phones:
                            self.phones.append(word)
                        s.append('<phone>')
                    elif '_post_code' in word:
                        self.entities['<post_code>'] = word
                        if word not in self.post_codes:
                            self.post_codes.append(word)
                        s.append('<post_code>')
                    else:
                        self.entities['<name>'] = word
                        if word not in self.names:
                            self.names.append(word)
                        s.append('<name>')
                else:
                    s.append(word)
        return s

    def load_entity(self, sentence):
        s = []
        '''
        '<name>': None,
        '<cuisine>': None,
        '<location>': None,
        '<price>': None,
        '<phone>': None,
        '<post_code>': None
        '''
        for word in sentence:
            if word == '<name>':
                s.append(self.entities['<name>'])
            elif word == '<cuisine>':
                s.append(self.entities['<cuisine>'])
            elif word == '<location>':
                s.append(self.entities['<location>'])
            elif word == '<price>':
                s.append(self.entities['<price>'])
            elif word == 'phone':
                s.append(self.entities['<phone>'])
            elif word == 'post_code':
                s.append(self.entities['<post_code>'])
            else:
                s.append(word)
        return ' '.join(s)

    def update_db(self):
        root = self.db_root
        f = open(root + 'names.txt', 'w')
        self.names.sort()
        f.write(str(self.names))
        f.close()
        f = open(root + 'cuisines.txt', 'w')
        self.cuisines.sort()
        f.write(str(self.cuisines))
        f.close()
        f = open(root + 'locations.txt', 'w')
        f.write(str(self.locations))
        f.close()
        f = open(root + 'prices.txt', 'w')
        f.write(str(self.prices))
        f.close()
        f = open(root + 'phones.txt', 'w')
        self.phones.sort()
        f.write(str(self.phones))
        f.close()
        f = open(root + 'post_codes.txt', 'w')
        self.post_codes.sort()
        f.write(str(self.post_codes))
        f.close()
