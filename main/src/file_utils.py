def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def write_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)