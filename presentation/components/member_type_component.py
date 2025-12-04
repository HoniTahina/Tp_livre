import tkinter as tk
from tkinter import ttk, messagebox

class MemberTypeComponent:
    
    def __init__(self, parent, membres_service, on_update_callback=None):
        self.membres_service = membres_service
        self.on_update_callback = on_update_callback
        self.selected_type_id = None
        
        self.frame = ttk.LabelFrame(parent, text="Gestion des Types de Membres", padding=10)
        self._build_ui()
        self.load_types()
    
    def _build_ui(self):
        self.tree = ttk.Treeview(self.frame, columns=("Type", "Prix", "MaxLivres"), show='headings')
        self.tree.heading("Type", text="Type")
        self.tree.heading("Prix", text="Prix")
        self.tree.heading("MaxLivres", text="Livres Autorisés")
        self.tree.pack(fill='x', pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_type)

        form_frame = ttk.Frame(self.frame)
        form_frame.pack(fill='x', pady=5)
        
        ttk.Label(form_frame, text="Type:").grid(row=0, column=0, padx=5, pady=2)
        self.type_entry = ttk.Entry(form_frame, width=20)
        self.type_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Prix:").grid(row=1, column=0, padx=5, pady=2)
        self.prix_entry = ttk.Entry(form_frame, width=20)
        self.prix_entry.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(form_frame, text="Max Livres:").grid(row=2, column=0, padx=5, pady=2)
        self.max_entry = ttk.Entry(form_frame, width=20)
        self.max_entry.grid(row=2, column=1, padx=5, pady=2)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', pady=5)
        ttk.Button(button_frame, text="Ajouter", command=self.add_type).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Modifier", command=self.edit_type).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Supprimer", command=self.delete_type).pack(side='left', padx=5)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def load_types(self):
        self.tree.delete(*self.tree.get_children())
        try:
            types = self.membres_service.types_membre()
            for t in types:
                self.tree.insert("", "end", iid=t[0], values=(t[1], t[2], t[3]))
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du chargement des types : {str(e)}")

    def on_select_type(self, event):
        selection = self.tree.selection()
        if selection:
            self.selected_type_id = int(selection[0])
            values = self.tree.item(selection[0], 'values')
            self.type_entry.delete(0, tk.END)
            self.type_entry.insert(0, values[0])
            self.prix_entry.delete(0, tk.END)
            self.prix_entry.insert(0, values[1])
            self.max_entry.delete(0, tk.END)
            self.max_entry.insert(0, values[2])

    def add_type(self):
        try:
            type_name = self.type_entry.get()
            prix = float(self.prix_entry.get())
            max_livres = int(self.max_entry.get())
            success, msg = self.membres_service.ajouter_type_membre(type_name, prix, max_livres)
            if success:
                messagebox.showinfo("Succès", msg)
                self.load_types()
                if self.on_update_callback:
                    self.on_update_callback()
            else:
                messagebox.showerror("Erreur", msg)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def edit_type(self):
        if not self.selected_type_id:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un type")
            return
        try:
            type_name = self.type_entry.get()
            prix = float(self.prix_entry.get())
            max_livres = int(self.max_entry.get())
            success, msg = self.membres_service.modifier_type_membre(
                self.selected_type_id, type_name, prix, max_livres
            )
            if success:
                messagebox.showinfo("Succès", msg)
                self.load_types()
                if self.on_update_callback:
                    self.on_update_callback()
            else:
                messagebox.showerror("Erreur", msg)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def delete_type(self):
        if not self.selected_type_id:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un type")
            return
        confirm = messagebox.askyesno("Confirmer", "Supprimer ce type ?")
        if not confirm:
            return
        try:
            success, msg = self.membres_service.supprimer_type_membre(self.selected_type_id)
            if success:
                messagebox.showinfo("Succès", msg)
                self.load_types()
                if self.on_update_callback:
                    self.on_update_callback()
                self.selected_type_id = None
                self.type_entry.delete(0, tk.END)
                self.prix_entry.delete(0, tk.END)
                self.max_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Erreur", msg)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
