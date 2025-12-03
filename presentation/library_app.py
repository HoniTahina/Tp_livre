from tkinter import ttk
from infrastructure.emprunt_service import EmpruntService
from infrastructure.client_service import ClientService
from infrastructure.livre_recherche_service import LivresRechercheService
from infrastructure.membres_service import ServiceMembre
from infrastructure.stats_emprunt_service import StatsEmpruntsService
from infrastructure.views_service import ViewsService
from presentation.tabs.rental_tab import RentalTab
from presentation.tabs.return_tab import ReturnTab
from presentation.tabs.statistics_tab import StatisticsTab
from presentation.tabs.user_management_tab import UserManagementTab


class LibraryApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Système de Prêt de Livre")
        self.root.geometry("1200x700")
        
        self.services = self._init_services()
        
        self._setup_style()
        self._create_notebook()
        self._create_tabs()
    
    def _init_services(self):
        return {
            'emprunt': EmpruntService(),
            'client': ClientService(),
            'livre_recherche': LivresRechercheService(),
            'membres': ServiceMembre(),
            'stats_emprunt': StatsEmpruntsService(),
            'views': ViewsService()
        }
    
    def _setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
    
    def _create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    def _create_tabs(self):
        rental_tab = RentalTab(self.notebook, self.services)
        self.notebook.add(rental_tab.get_frame(), text='📚 Louer un Livre')
        
        return_tab = ReturnTab(self.notebook, self.services)
        self.notebook.add(return_tab.get_frame(), text='📥 Retourner un Livre')
        
        stats_tab = StatisticsTab(self.notebook, self.services)
        self.notebook.add(stats_tab.get_frame(), text='📊 Statistiques')

        user_mgmt_tab = UserManagementTab(self.notebook, self.services)
        self.notebook.add(user_mgmt_tab.get_frame(), text='👤 Gestion des Utilisateurs')
    
    def __del__(self):
        if hasattr(self, 'services') and 'client' in self.services:
            self.services['client'].close()
