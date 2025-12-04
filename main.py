import random
from infrastructure.livre_service import LivreService
from infrastructure.client_service import ClientService


def main():
    #livre_service = LivreService()
    client_service = ClientService()
    #livre_service.seed_livre_from_csv('./data/books.csv')
    client_service.seed_client()
if __name__ == "__main__":
    main()
