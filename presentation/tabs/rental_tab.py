import tkinter as tk
from tkinter import ttk, messagebox
from presentation.components.client_info_component import ClientInfoComponent
from presentation.components.book_list_component import BookListComponent


class RentalTab:
    
    def __init__(self, parent, services):
        self.emprunt_service = services['emprunt']
        self.membres_service = services['membres']
        self.livre_recherche_service = services['livre_recherche']
        
        self.frame = ttk.Frame(parent)
        self._build_ui()
    
    def _build_ui(self):
        self.client_info = ClientInfoComponent(
            self.frame, 
            self.emprunt_service, 
            self.membres_service
        )
        self.client_info.pack(fill='x', padx=10, pady=10)
        
        self.book_list = BookListComponent(
            self.frame, 
            self.livre_recherche_service
        )
        self.book_list.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Button(self.frame, text="Louer le Livre Sélectionné", 
                  command=self.rent_book, 
                  style='Accent.TButton').pack(pady=10)
    
    def get_frame(self):
        return self.frame
    
    def rent_book(self):
        try:
            client_id = self.client_info.get_client_id()
            
            book_values = self.book_list.get_selected_book()
            if not book_values:
                messagebox.showwarning("Avertissement", "Veuillez sélectionner un livre")
                return
            
            book_id = book_values[0]
            
            success, message = self.emprunt_service.louer_livre(client_id, book_id)
            
            if success:
                messagebox.showinfo("Succès", message)
                self.book_list.load_books()
            else:
                messagebox.showerror("Erreur", message)
                
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un ID client valide")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
