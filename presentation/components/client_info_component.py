import tkinter as tk
from tkinter import ttk, messagebox


class ClientInfoComponent:
    
    def __init__(self, parent, emprunt_service, membres_service):
        self.emprunt_service = emprunt_service
        self.membres_service = membres_service
        
        self.frame = ttk.LabelFrame(parent, text="Informations Client", padding=10)
        self._build_ui()
    
    def _build_ui(self):
        ttk.Label(self.frame, text="ID Client :").grid(row=0, column=0, sticky='w', padx=5)
        
        self.client_id_entry = ttk.Entry(self.frame, width=20)
        self.client_id_entry.grid(row=0, column=1, padx=5)
        
        ttk.Button(self.frame, text="Vérifier l'Éligibilité", 
                  command=self.check_eligibility).grid(row=0, column=2, padx=5)
        
        self.eligibility_label = ttk.Label(self.frame, text="", foreground="blue")
        self.eligibility_label.grid(row=1, column=0, columnspan=3, pady=5)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def get_client_id(self):
        return int(self.client_id_entry.get())
    
    def check_eligibility(self):
        try:
            client_id = self.get_client_id()
            member_info = self.membres_service.info_membre(client_id)
            
            if not member_info:
                self.eligibility_label.config(
                    text="❌ Client introuvable", 
                    foreground="red"
                )
                return
            
            can_borrow = self.emprunt_service.peut_emprunter(client_id)
            
            if can_borrow:
                self.eligibility_label.config(
                    text=f"✅ {member_info[1]} peut emprunter (Type : {member_info[4]})", 
                    foreground="green"
                )
            else:
                self.eligibility_label.config(
                    text=f"❌ {member_info[1]} ne peut pas emprunter plus de livres", 
                    foreground="red"
                )
                
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un ID client valide")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
