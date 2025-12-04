import tkinter as tk
from presentation.library_app import LibraryApp
# from infrastructure.livre_service import LivreService

def main():
    # livre_service = LivreService()
    # livre_service.seed_livre_from_csv('./data/books.csv')

    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
