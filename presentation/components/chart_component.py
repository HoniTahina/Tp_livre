import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import numpy as np


class ChartComponent:
    
    def __init__(self, parent, views_service):
        self.views_service = views_service
        self.frame = ttk.Frame(parent)
        self._build_ui()
    
    def _build_ui(self):
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="📚 Top Livres", 
                  command=self.show_top_books_chart).pack(side='left', padx=5)
        ttk.Button(button_frame, text="👥 Activité Clients", 
                  command=self.show_client_activity_chart).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📊 Vue d'Ensemble", 
                  command=self.show_overview_dashboard).pack(side='left', padx=5)
        
        self.chart_frame = ttk.Frame(self.frame)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
    
    def _clear_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
    
    def show_top_books_chart(self):
        self._clear_chart()
        books = self.views_service.meilleurs_livres(15)
        
        if not books:
            ttk.Label(self.chart_frame, text="Aucune donnée disponible").pack()
            return
        
        titles = [book[1][:35] + '...' if len(book[1]) > 35 else book[1] for book in books]
        counts = [book[2] for book in books]
        
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(books)))
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(titles, counts, color=colors, edgecolor='black', linewidth=0.5)

        for i, (bar, count) in enumerate(zip(bars, counts)):
            width = bar.get_width()
            ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                   f'{count}', ha='left', va='center', fontweight='bold', fontsize=9)
        
        ax.set_xlabel('Nombre de Prêts', fontsize=12, fontweight='bold')
        ax.set_title('Top 15 des Livres les Plus Empruntés', fontsize=14, fontweight='bold', pad=20)
        ax.invert_yaxis()
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        avg = np.mean(counts)
        ax.axvline(avg, color='red', linestyle='--', linewidth=2, alpha=0.7, label=f'Moyenne: {avg:.1f}')
        ax.legend(loc='lower right')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def show_client_activity_chart(self):
        self._clear_chart()
        clients = self.views_service.livres_empruntes_par_client()
        
        if not clients:
            ttk.Label(self.chart_frame, text="Aucune donnée disponible").pack()
            return
        
        clients = sorted(clients, key=lambda x: x[2], reverse=True)[:20]
        names = [client[1] for client in clients]
        counts = [client[2] for client in clients]
        
        colors = ['#d32f2f' if c >= np.percentile(counts, 75) else 
                 '#f57c00' if c >= np.percentile(counts, 50) else 
                 '#fbc02d' if c >= np.percentile(counts, 25) else 
                 '#388e3c' for c in counts]
        
        fig, ax = plt.subplots(figsize=(14, 8))
        bars = ax.bar(range(len(names)), counts, color=colors, edgecolor='black', linewidth=0.8)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        ax.set_xticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha='right')
        ax.set_ylabel('Nombre de Livres Empruntés', fontsize=12, fontweight='bold')
        ax.set_title('Top 20 Clients par Activité de Prêt', fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#d32f2f', label='Très actif (75%+)'),
            Patch(facecolor='#f57c00', label='Actif (50-75%)'),
            Patch(facecolor='#fbc02d', label='Modéré (25-50%)'),
            Patch(facecolor='#388e3c', label='Peu actif (<25%)')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def show_overview_dashboard(self):
        self._clear_chart()
        
        loans = self.views_service.emprunts_en_cours()
        active_members = self.views_service.membres_actifs()
        
        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(2, 1, hspace=0.4)

        ax_loans = fig.add_subplot(gs[0, 0])
        if loans:
            from datetime import datetime
            dates = []
            for loan in loans:
                try:
                    if loan[6]:
                        if isinstance(loan[6], str):
                            date = datetime.strptime(loan[6], '%Y-%m-%d')
                        else:
                            date = loan[6]
                        dates.append(date)
                except:
                    pass
            
            if dates:
                dates_sorted = sorted(dates)
                loan_counts = list(range(1, len(dates_sorted) + 1))
                scatter = ax_loans.scatter(dates_sorted, loan_counts, alpha=0.6, s=50, c=loan_counts, cmap='cool')
                ax_loans.plot(dates_sorted, loan_counts, alpha=0.3, linewidth=2)
                ax_loans.set_xlabel('Date')
                ax_loans.set_ylabel('Nombre cumulé de prêts')
                ax_loans.set_title('Chronologie des Prêts en Cours')
                ax_loans.grid(alpha=0.3)
                fig.autofmt_xdate()

        ax_members = fig.add_subplot(gs[1, 0])
        if active_members:
            member_types = {}
            for member in active_members:
                mtype = member[4] if len(member) > 4 else 'Unknown'
                member_types[mtype] = member_types.get(mtype, 0) + 1
            
            if member_types:
                types = list(member_types.keys())
                counts = list(member_types.values())
                colors_bar = plt.cm.Pastel1(range(len(types)))
                bars = ax_members.bar(types, counts, color=colors_bar, edgecolor='black')
                
                for bar in bars:
                    height = bar.get_height()
                    ax_members.text(bar.get_x() + bar.get_width()/2., height,
                                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
                
                ax_members.set_ylabel('Nombre de membres')
                ax_members.set_title('Types de Membres')
                ax_members.grid(axis='y', alpha=0.3)

        plt.suptitle('Tableau de Bord Bibliothèque', fontsize=16, fontweight='bold', y=0.995)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)