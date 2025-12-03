import tkinter as tk
from tkinter import ttk, messagebox
from presentation.components.loan_list_component import LoanListComponent


class ReturnTab:
    
    def __init__(self, parent, services):
        self.emprunt_service = services['emprunt']
        self.stats_emprunt_service = services['stats_emprunt']
        self.views_service = services['views']
        
        self.frame = ttk.Frame(parent)
        self._build_ui()
    
    def _build_ui(self):
        self.loan_list = LoanListComponent(
            self.frame, 
            self.stats_emprunt_service,
            self.views_service
        )
        self.loan_list.pack(fill='both', expand=True)
        
        ttk.Button(self.frame, text="Retourner le Livre Sélectionné", 
                  command=self.return_book,
                  style='Accent.TButton').pack(pady=10)
    
    def get_frame(self):
        return self.frame
    
    def return_book(self):
        loan_values = self.loan_list.get_selected_loan()
        if not loan_values:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un emprunt")
            return
        
        location_id = loan_values[0]
        
        success, message = self.emprunt_service.retourner_livre(location_id)
        
        if success:
            messagebox.showinfo("Succès", message)
            self.loan_list.show_all_loans()
        else:
            messagebox.showerror("Erreur", message)
