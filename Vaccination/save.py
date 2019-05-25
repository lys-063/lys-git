def save(path, data):
    f = open(path + 'data.txt', 'w')
    f.write(data)
    f.close()
