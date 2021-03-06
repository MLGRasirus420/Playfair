import hashlib
import sys
import os


def get_hash(file):
        BLOCK_SIZE = 65536 # The size of each read from the file
        file_hash = hashlib.sha3_512() # Create the hash object, can use something other than `.sha256()` if you wish
        with open(file, 'rb') as f: # Open the file to read it's bytes
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file
        return (file_hash.hexdigest()) # Get the hexadecimal digest of the hash

file = 'testovacisoubor.txt'
print(get_hash(file))
path = sys.argv[0]
head, tail = os.path.split(path)
print('head:' + head)
print(tail)
print(path)