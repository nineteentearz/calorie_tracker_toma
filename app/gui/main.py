"""
Точка входа в GUI приложение.
"""
from .controllers import AppController
from .auth_window import run_auth

def main():
    run_auth()

if __name__ == "__main__":
    main()