import os

if (os.environ.get('RPK_SOURCE') == None):
    print("Warning: Cannot found rpk source file, partial check-in need it.")

