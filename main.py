from infrastructure.livre_service import LivreService


def main():
    livre_service = LivreService()
    livre_service.seed_livre_from_csv('./data/books.csv')

if __name__ == "__main__":
    main()
