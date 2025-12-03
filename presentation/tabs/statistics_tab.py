import tkinter as tk
from tkinter import ttk
from presentation.components.chart_component import ChartComponent


class StatisticsTab:
    
    def __init__(self, parent, services):
        self.views_service = services['views']
        
        self.frame = ttk.Frame(parent)
        self._build_ui()
    
    def _build_ui(self):
        self.chart = ChartComponent(
            self.frame, 
            self.views_service
        )
        self.chart.pack(fill='both', expand=True)
    
    def get_frame(self):
        return self.frame
