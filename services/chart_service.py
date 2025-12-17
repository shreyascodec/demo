"""
Chart service for creating visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
import pandas as pd

class ChartService:
    """Service for creating charts and visualizations"""
    
    @staticmethod
    def create_pie_chart(data: List[Dict[str, Any]], values_key: str, names_key: str, title: str):
        """Create a pie chart"""
        fig = go.Figure(data=[go.Pie(
            labels=[item[names_key] for item in data],
            values=[item[values_key] for item in data],
            hole=0.3,
            marker=dict(colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'])
        )])
        
        fig.update_layout(
            title=title,
            showlegend=True,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    @staticmethod
    def create_bar_chart(data: List[Dict[str, Any]], x_key: str, y_key: str, title: str, color: str = '#3b82f6'):
        """Create a bar chart"""
        fig = go.Figure(data=[go.Bar(
            x=[item[x_key] for item in data],
            y=[item[y_key] for item in data],
            marker_color=color,
            text=[item[y_key] for item in data],
            textposition='auto',
        )])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_key.replace('_', ' ').title(),
            yaxis_title=y_key.replace('_', ' ').title(),
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_line_chart(data: List[Dict[str, Any]], x_key: str, y_keys: List[str], title: str):
        """Create a line chart"""
        fig = go.Figure()
        
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
        
        for i, y_key in enumerate(y_keys):
            fig.add_trace(go.Scatter(
                x=[item[x_key] for item in data],
                y=[item[y_key] for item in data],
                mode='lines+markers',
                name=y_key.replace('_', ' ').title(),
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_key.replace('_', ' ').title(),
            yaxis_title='Count',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_area_chart(data: List[Dict[str, Any]], x_key: str, y_keys: List[str], title: str):
        """Create an area chart"""
        fig = go.Figure()
        
        colors = ['#3b82f6', '#10b981', '#8b5cf6']
        
        for i, y_key in enumerate(y_keys):
            fig.add_trace(go.Scatter(
                x=[item[x_key] for item in data],
                y=[item[y_key] for item in data],
                mode='lines',
                name=y_key.replace('_', ' ').title(),
                fill='tonexty' if i > 0 else 'tozeroy',
                line=dict(color=colors[i % len(colors)], width=2),
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_key.replace('_', ' ').title(),
            yaxis_title='Count',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_gauge_chart(value: float, title: str, max_value: float = 100):
        """Create a gauge chart"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            delta={'reference': max_value * 0.8},
            gauge={
                'axis': {'range': [None, max_value]},
                'bar': {'color': "#3b82f6"},
                'steps': [
                    {'range': [0, max_value * 0.5], 'color': "#fef3c7"},
                    {'range': [max_value * 0.5, max_value * 0.8], 'color': "#dbeafe"},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    @staticmethod
    def create_stacked_bar_chart(data: List[Dict[str, Any]], x_key: str, y_keys: List[str], title: str):
        """Create a stacked bar chart"""
        fig = go.Figure()
        
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
        
        for i, y_key in enumerate(y_keys):
            fig.add_trace(go.Bar(
                name=y_key.replace('_', ' ').title(),
                x=[item[x_key] for item in data],
                y=[item[y_key] for item in data],
                marker_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            title=title,
            barmode='stack',
            xaxis_title=x_key.replace('_', ' ').title(),
            yaxis_title='Count',
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig

