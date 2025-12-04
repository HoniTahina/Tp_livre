import tkinter as tk
from tkinter import ttk, messagebox
from presentation.components.member_type_component import MemberTypeComponent
from presentation.components.user_form_component import UserFormComponent
from presentation.components.member_card_component import MemberCardComponent
from presentation.components.user_list_component import UserListComponent


class UserManagementTab:
    
    def __init__(self, parent, services):
        self.client_service = services['client']
        self.membres_service = services['membres']
        
        self.frame = ttk.Frame(parent)
        self._build_ui()
    
    def _build_ui(self):
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        
        self.user_form = UserFormComponent(
            left_frame,
            self.client_service,
            on_save_callback=self.on_user_saved
        )
        self.user_form.pack(fill='x', pady=(0, 10))
        
        self.member_card = MemberCardComponent(
            left_frame,
            self.membres_service,
            on_update_callback=self.on_card_updated
        )
        self.member_card.pack(fill='x')

        self.member_type = MemberTypeComponent(
            left_frame,
            self.membres_service,
            on_update_callback=self.combined_update
        )
        self.member_type.pack(fill='x', pady=(10, 0))
        
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        self.user_list = UserListComponent(
            right_frame,
            self.client_service,
            on_select_callback=self.on_user_selected
        )
        self.user_list.pack(fill='both', expand=True)
    
    def get_frame(self):
        return self.frame
    
    def on_user_saved(self):
        self.user_list.load_users()
    
    def on_card_updated(self):
        self.user_list.load_users()

    def combined_update(self):
        self.member_card.refresh_types()
        self.on_card_updated()
    
    def on_user_selected(self, action, user_data):
        if action == 'edit':
            self.user_form.load_user(user_data)
        elif action == 'card':
            user_id = user_data[0]
            self.member_card.set_user_id(user_id)
