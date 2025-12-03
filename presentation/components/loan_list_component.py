import tkinter as tk
from tkinter import ttk, messagebox


class LoanListComponent:
    
    def __init__(self, parent, stats_emprunt_service, views_service):
        self.stats_emprunt_service = stats_emprunt_service
        self.views_service = views_service
        
        self.frame = ttk.Frame(parent)
        self._build_ui()
    
    def _build_ui(self):
        search_frame = ttk.LabelFrame(self.frame, text="Rechercher des Emprunts", padding=10)
        search_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(search_frame, text="ID Client :").grid(row=0, column=0, padx=5)
        self.client_entry = ttk.Entry(search_frame, width=20)
        self.client_entry.grid(row=0, column=1, padx=5)
        ttk.Button(search_frame, text="Afficher les Emprunts", 
                  command=self.show_client_loans).grid(row=0, column=2, padx=5)
        
        ttk.Button(search_frame, text="Afficher Tous les Emprunts Actifs", 
                  command=self.show_all_loans).grid(row=0, column=3, padx=5)
        
        loan_frame = ttk.LabelFrame(self.frame, text="Emprunts Actifs", padding=10)
        loan_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID Emprunt', 'ID Livre', 'Client', 'Titre', 'Date de Prêt')
        self.tree = ttk.Treeview(loan_frame, columns=columns, show='tree headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(loan_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def show_client_loans(self):
        try:
            client_id = int(self.client_entry.get())
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            loans = self.stats_emprunt_service.emprunts_client(client_id)
            
            for loan in loans:
                if loan[4] is None:
                    self.tree.insert('', 'end', values=(
                        loan[0], loan[1], client_id, loan[2], loan[3]
                    ))
                    
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un ID client valide")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def show_all_loans(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        loans = self.views_service.emprunts_en_cours()
        
        for loan in loans:
            self.tree.insert('', 'end', values=(
                loan[0], loan[1], loan[4], loan[3], loan[6]
            ))
    
    def get_selected_loan(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])['values']
