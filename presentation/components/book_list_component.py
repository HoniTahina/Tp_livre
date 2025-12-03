import tkinter as tk
from tkinter import ttk


class BookListComponent:
    
    def __init__(self, parent, livre_recherche_service):
        self.livre_recherche_service = livre_recherche_service
        
        self.frame = ttk.LabelFrame(parent, text="Sélection de Livres", padding=10)
        self._build_ui()
        self.load_books()
    
    def _build_ui(self):
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill='x', pady=5)
        
        ttk.Label(search_frame, text="Recherche :").pack(side='left', padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search_frame, text="Rechercher", 
                  command=self.load_books).pack(side='left', padx=5)

        columns = ('ID', 'Titre', 'Auteur', 'Année', 'Stock')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='tree headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def load_books(self):
        search_term = self.search_entry.get()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        books = self.livre_recherche_service.rechercher_livres(search_term)
        
        for book in books:
            self.tree.insert('', 'end', values=book)
    
    def get_selected_book(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])['values']
