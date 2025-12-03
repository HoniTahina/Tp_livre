import tkinter as tk
from tkinter import ttk, messagebox


class MemberCardComponent:
    
    def __init__(self, parent, membres_service, on_update_callback=None):
        self.membres_service = membres_service
        self.on_update_callback = on_update_callback
        self.selected_user_id = None
        
        self.frame = ttk.LabelFrame(parent, text="Gestion des Cartes Membres", padding=10)
        self._build_ui()
        self._load_member_types()
    
    def _build_ui(self):
        ttk.Label(self.frame, text="ID Client :").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.user_id_entry = ttk.Entry(self.frame, width=15)
        self.user_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(self.frame, text="Charger Infos", 
                  command=self.load_member_info).grid(row=0, column=2, padx=5, pady=5)
        
        self.info_label = ttk.Label(self.frame, text="", foreground="blue", wraplength=400)
        self.info_label.grid(row=1, column=0, columnspan=3, pady=10, sticky='w')
        
        ttk.Label(self.frame, text="Type de Membre :").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(self.frame, textvariable=self.type_var, 
                                       state='readonly', width=27)
        self.type_combo.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='w')
        
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Créer Carte", 
                  command=self.create_card).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Désactiver Carte", 
                  command=self.deactivate_card).pack(side='left', padx=5)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def _load_member_types(self):
        try:
            types = self.membres_service.types_membre()
            self.member_types = {f"{t[1]} (Max {t[2]} livres)": t[0] for t in types}
            self.type_combo['values'] = list(self.member_types.keys())
            if self.type_combo['values']:
                self.type_combo.current(0)
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du chargement des types de membre : {str(e)}")
    
    def set_user_id(self, user_id):
        self.user_id_entry.delete(0, tk.END)
        self.user_id_entry.insert(0, str(user_id))
        self.load_member_info()
    
    def load_member_info(self):
        try:
            user_id = int(self.user_id_entry.get())
            self.selected_user_id = user_id
            
            member_info = self.membres_service.info_membre(user_id)
            
            if not member_info:
                self.info_label.config(
                    text="❌ Client introuvable",
                    foreground="red"
                )
                return
            
            has_card = member_info[3] is not None and member_info[6] == 1
            
            if has_card:
                info_text = (f"✅ {member_info[1]}\n"
                           f"Email : {member_info[2]}\n"
                           f"Type de Membre : {member_info[4]}\n"
                           f"Livres Autorisés : {member_info[5]}\n"
                           f"Statut : Actif")
                self.info_label.config(text=info_text, foreground="green")
            else:
                info_text = (f"ℹ️ {member_info[1]}\n"
                           f"Email : {member_info[2]}\n"
                           f"Statut : Pas de carte membre active")
                self.info_label.config(text=info_text, foreground="orange")
                
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un ID client valide")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def create_card(self):
        if not self.selected_user_id:
            messagebox.showwarning("Avertissement", "Veuillez d'abord charger un client")
            return
        
        selected_type = self.type_var.get()
        type_id = self.member_types.get(selected_type, 1)
        
        try:
            success, message = self.membres_service.creer_carte_membre(
                self.selected_user_id, type_id
            )
            
            if success:
                messagebox.showinfo("Succès", message)
                self.load_member_info()
                if self.on_update_callback:
                    self.on_update_callback()
            else:
                messagebox.showerror("Erreur", message)
                
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
    
    def deactivate_card(self):
        if not self.selected_user_id:
            messagebox.showwarning("Avertissement", "Veuillez d'abord charger un client")
            return
        
        confirm = messagebox.askyesno(
            "Confirmer", 
            "Êtes-vous sûr de vouloir désactiver cette carte membre ?"
        )
        if not confirm:
            return
        
        try:
            success, message = self.membres_service.desactiver_carte_membre(
                self.selected_user_id
            )
            
            if success:
                messagebox.showinfo("Succès", message)
                self.load_member_info()
                if self.on_update_callback:
                    self.on_update_callback()
            else:
                messagebox.showerror("Erreur", message)
                
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def refresh_types(self):
        try:
            types = self.membres_service.types_membre()
            self.member_types = {f"{t[1]} (Max {t[3]} livres)": t[0] for t in types}
            self.type_combo['values'] = list(self.member_types.keys())
            if self.type_combo['values']:
                self.type_combo.current(0)
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du rechargement des types : {str(e)}")