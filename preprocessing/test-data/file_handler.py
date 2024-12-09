#high risk
# file_handler.py
def write_to_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)

def read_from_file(filename):
    with open(filename, "r") as f:
        return f.read()

def delete_file(filename):
    import os
    os.remove(filename)
