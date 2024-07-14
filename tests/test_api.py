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

def get_secret(key):
    """
    This function dynamically retrieves a secret value based on the environment.
    """
    load_dotenv()

    env = os.getenv('ENVIRONMENT')
    print(env)

    if env == 'local':  # Check for local environment variable
    # Load from .env file (assuming it's present locally)


        local_key = os.getenv(key)

        print(f"local key {local_key}")

        return local_key
  
    elif env == 'deployment':
    # Access from GitHub secrets during deployment (assuming environment variable is set)

        deployment_key = os.getenv(key)

        print(f"deployment key {deployment_key}")

        for i in deployment_key:
            print(i)

        return deployment_key

T212_API_KEY = get_secret('TEST')