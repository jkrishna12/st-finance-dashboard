import os
from dotenv import load_dotenv, find_dotenv
# from src.api_connection import *
import pytest

# load_dotenv(find_dotenv())

# try:

#     T212_API_KEY = os.getenv('T212_API_KEY')

#     print(T212_API_KEY)

# except:

#     T212_API_KEY = 'hello'
#     print("except block")
#     print(T212_API_KEY)

# @pytest.mark.skip(reason="not testing this")
# def test_get_portfolio():

#     portfolio_reponse = get_portfolio(T212_API_KEY)

#     assert portfolio_reponse.status_code == 200
    
#     assert portfolio_reponse.headers["Content-Type"] == 'application/json'

#     portfolio_data = portfolio_reponse.json()

#     assert len(portfolio_data[0]) == 11

#     return

def test_github_secrets():

    load_dotenv(find_dotenv())

    try:
        print('try block')

        TEST_KEY = os.getenv('TEST')

        print(TEST_KEY)

    except:
        print('except block')

        TEST_KEY = os.environ["test_var"]

        print(TEST_KEY)

load_dotenv(find_dotenv())

try:
    print('try block')

    TEST_KEY = os.getenv('TEST')

    print(TEST_KEY)

except:
    print('except block')

    TEST_KEY = os.environ["test_var"]

    print(TEST_KEY)