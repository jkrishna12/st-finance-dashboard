# import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

try:

    T212_API_KEY = os.getenv('T212_API_KEY')

    print(T212_API_KEY)

except:

    T212_API_KEY = 'hello'

    print(T212_API_KEY)