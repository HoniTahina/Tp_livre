import tkinter as tk
from tkinter import ttk


class UserListComponent:
    
    def __init__(self, parent, client_service, on_select_callback=None):
        self.client_service = client_service
        self.on_select_callback = on_select_callback
        
        self.frame = ttk.LabelFrame(parent, text="Tous les Utilisateurs", padding=10)
        self._build_ui()
        self.load_users()
    
    def _build_ui(self):
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Rafraîchir", 
                  command=self.load_users).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Modifier Sélectionné", 
                  command=self.edit_selected).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Gérer Carte Membre", 
                  command=self.manage_card).pack(side='left', padx=5)
        
        columns = ('ID', 'Nom', 'Email', 'Téléphone', 'Type Membre', 'Statut', 'Emprunts Actifs')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='tree headings', height=15)
        
        self.tree.column('#0', width=0, stretch=False)
        self.tree.column('ID', width=50)
        self.tree.column('Nom', width=150)
        self.tree.column('Email', width=180)
        self.tree.column('Téléphone', width=100)
        self.tree.column('Type Membre', width=120)
        self.tree.column('Statut', width=80)
        self.tree.column('Emprunts Actifs', width=100)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.tree.bind('<Double-1>', lambda e: self.edit_selected())
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            users = self.client_service.tous_les_clients()
            
            for user in users:
                user_id = user[0]
                name = user[1]
                email = user[2]
                tel = user[3] if user[3] else "-"
                member_type = user[5] if user[5] else "Pas de Carte"
                status = "Actif" if user[6] == 1 else "Inactif" if user[6] == 0 else "-"
                active_loans = user[7] if user[7] else 0
                
                tags = ()
                if user[6] == 1:
                    tags = ('actif',)
                elif user[6] == 0:
                    tags = ('inactif',)
                
                self.tree.insert('', 'end', values=(
                    user_id, name, email, tel, member_type, status, active_loans
                ), tags=tags)
            
            self.tree.tag_configure('actif', background='#e8f5e9')
            self.tree.tag_configure('inactif', background='#ffebee')
            
        except Exception as e:
            print(f"Erreur lors du chargement des utilisateurs : {e}")
    
    def get_selected_user(self):
        selection = self.tree.selection()
        if not selection:
            return None
        return self.tree.item(selection[0])['values']
    
    def edit_selected(self):
        user_data = self.get_selected_user()
        if user_data and self.on_select_callback:
            self.on_select_callback('edit', user_data)
    
    def manage_card(self):
        user_data = self.get_selected_user()
        if user_data and self.on_select_callback:
            self.on_select_callback('card', user_data)
