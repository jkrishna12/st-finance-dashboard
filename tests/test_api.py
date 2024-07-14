import os
from dotenv import load_dotenv, find_dotenv
from src.api_connection import *
import pytest

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

        return deployment_key

T212_API_KEY = get_secret('T212_API_KEY')


def test_get_portfolio():

    portfolio_reponse = get_portfolio(T212_API_KEY)

    assert portfolio_reponse.status_code == 200
    
    assert portfolio_reponse.headers["Content-Type"] == 'application/json'

    portfolio_data = portfolio_reponse.json()

    assert len(portfolio_data[0]) == 11

    return


