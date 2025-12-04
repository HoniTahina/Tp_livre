import sys
import tkinter as tk
from presentation.library_app import LibraryApp
from infrastructure.livre_service import LivreService


def run_gui():
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()


def seed_database():
    service = LivreService()
    service.seed_livre_from_csv("./data/books.csv")
    print("Database seeded from CSV.")


def main():
    if len(sys.argv) == 1:
        run_gui()
        return

    cmd = sys.argv[1].lower()

    if cmd == "seed":
        seed_database()
    elif cmd == "gui":
        run_gui()
    else:
        print("Unknown command. Use:")
        print("  python main.py seed")
        print("  python main.py gui")


if __name__ == "__main__":
    main()
