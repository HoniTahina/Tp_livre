import tkinter as tk
from tkinter import ttk, messagebox


class UserFormComponent:
    
    def __init__(self, parent, client_service, on_save_callback=None):
        self.client_service = client_service
        self.on_save_callback = on_save_callback
        self.current_user_id = None
        
        self.frame = ttk.LabelFrame(parent, text="Formulaire Utilisateur", padding=10)
        self._build_ui()
    
    def _build_ui(self):
        ttk.Label(self.frame, text="Nom :").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_entry = ttk.Entry(self.frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame, text="Email :").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.email_entry = ttk.Entry(self.frame, width=30)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.frame, text="Téléphone :").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.tel_entry = ttk.Entry(self.frame, width=30)
        self.tel_entry.grid(row=2, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.save_btn = ttk.Button(button_frame, text="Créer Utilisateur", 
                                   command=self.save_user)
        self.save_btn.pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Effacer", 
                  command=self.clear_form).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Aléatoire", 
                  command=self.random_user).pack(side='left', padx=5)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def random_user(self):
        name = self.client_service.gen_name()
        email = self.client_service.gen_email(name)
        tel = self.client_service.gen_num()
        success, user_id, message = self.client_service.creer_utilisateur(
            name, email, tel
        )
        
        if success:
            messagebox.showinfo("Succès", message)
            self.clear_form()
            if self.on_save_callback:
                self.on_save_callback()
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.tel_entry.delete(0, tk.END)
        self.current_user_id = None
        self.save_btn.config(text="Créer Utilisateur")
    
    def load_user(self, user_data):
        self.clear_form()
        self.current_user_id = user_data[0]
        self.name_entry.insert(0, user_data[1])
        self.email_entry.insert(0, user_data[2])
        if user_data[3]:
            self.tel_entry.insert(0, user_data[3])
        self.save_btn.config(text="Mettre à Jour Utilisateur")
    
    def save_user(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        tel = self.tel_entry.get().strip()
        
        if not name or not email:
            messagebox.showerror("Erreur", "Nom et Email requis")
            return
        
        try:
            if self.current_user_id:
                success, message = self.client_service.mettre_a_jour_utilisateur(
                    self.current_user_id, name, email, tel
                )
            else:
                success, user_id, message = self.client_service.creer_utilisateur(
                    name, email, tel
                )
            
            if success:
                messagebox.showinfo("Succès", message)
                self.clear_form()
                if self.on_save_callback:
                    self.on_save_callback()
            else:
                messagebox.showerror("Erreur", message)
                
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
