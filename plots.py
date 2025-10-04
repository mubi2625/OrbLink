import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List

def plot_snr_vs_time(df_ground: pd.DataFrame, df_crosslink: pd.DataFrame) -> go.Figure:
    """
    Create interactive plot of SNR vs time for both constellation types.
    
    Args:
        df_ground: Ground-station-only simulation results
        df_crosslink: Crosslinked simulation results
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Ground station only - average SNR per time step
    gs_avg = df_ground.groupby('time_minutes')['snr_dB'].mean().reset_index()
    fig.add_trace(go.Scatter(
        x=gs_avg['time_minutes'],
        y=gs_avg['snr_dB'],
        mode='lines',
        name='Ground Station Only',
        line=dict(color='#FF6B6B', width=2),
        hovertemplate='Time: %{x:.1f} min<br>SNR: %{y:.1f} dB<extra></extra>'
    ))
    
    # Crosslinked - average SNR per time step
    cl_avg = df_crosslink.groupby('time_minutes')['snr_dB'].mean().reset_index()
    fig.add_trace(go.Scatter(
        x=cl_avg['time_minutes'],
        y=cl_avg['snr_dB'],
        mode='lines',
        name='Crosslinked',
        line=dict(color='#4ECDC4', width=2),
        hovertemplate='Time: %{x:.1f} min<br>SNR: %{y:.1f} dB<extra></extra>'
    ))
    
    # Add threshold line
    fig.add_hline(y=10, line_dash="dash", line_color="gray", 
                  annotation_text="Threshold (10 dB)")
    
    fig.update_layout(
        title='Signal-to-Noise Ratio Over Time',
        xaxis_title='Time (minutes)',
        yaxis_title='SNR (dB)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def plot_latency_vs_time(df_ground: pd.DataFrame, df_crosslink: pd.DataFrame) -> go.Figure:
    """
    Create interactive plot of latency vs time for both constellation types.
    
    Args:
        df_ground: Ground-station-only simulation results
        df_crosslink: Crosslinked simulation results
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Ground station only
    gs_latency = df_ground.groupby('time_minutes')['latency_ms'].mean().reset_index()
    fig.add_trace(go.Scatter(
        x=gs_latency['time_minutes'],
        y=gs_latency['latency_ms'],
        mode='lines',
        name='Ground Station Only',
        line=dict(color='#FF6B6B', width=2),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 107, 0.2)',
        hovertemplate='Time: %{x:.1f} min<br>Latency: %{y:.1f} ms<extra></extra>'
    ))
    
    # Crosslinked
    cl_latency = df_crosslink.groupby('time_minutes')['latency_ms'].mean().reset_index()
    fig.add_trace(go.Scatter(
        x=cl_latency['time_minutes'],
        y=cl_latency['latency_ms'],
        mode='lines',
        name='Crosslinked',
        line=dict(color='#4ECDC4', width=2),
        fill='tozeroy',
        fillcolor='rgba(78, 205, 196, 0.2)',
        hovertemplate='Time: %{x:.1f} min<br>Latency: %{y:.1f} ms<extra></extra>'
    ))
    
    fig.update_layout(
        title='Communication Latency Over Time',
        xaxis_title='Time (minutes)',
        yaxis_title='Latency (ms)',
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig

def plot_availability(df_ground: pd.DataFrame, df_crosslink: pd.DataFrame) -> go.Figure:
    """
    Create bar chart comparing availability metrics.
    
    Args:
        df_ground: Ground-station-only simulation results
        df_crosslink: Crosslinked simulation results
        
    Returns:
        Plotly figure object
    """
    # Calculate metrics
    gs_coverage = df_ground['is_feasible'].mean() * 100
    cl_coverage = df_crosslink['is_feasible'].mean() * 100
    
    gs_uptime = df_ground['coverage'].mean() * 100
    cl_uptime = df_crosslink['coverage'].mean() * 100
    
    fig = go.Figure(data=[
        go.Bar(
            name='Ground Station Only',
            x=['Coverage %', 'Uptime %'],
            y=[gs_coverage, gs_uptime],
            marker_color='#FF6B6B',
            text=[f'{gs_coverage:.1f}%', f'{gs_uptime:.1f}%'],
            textposition='outside'
        ),
        go.Bar(
            name='Crosslinked',
            x=['Coverage %', 'Uptime %'],
            y=[cl_coverage, cl_uptime],
            marker_color='#4ECDC4',
            text=[f'{cl_coverage:.1f}%', f'{cl_uptime:.1f}%'],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title='Coverage and Availability Comparison',
        yaxis_title='Percentage (%)',
        barmode='group',
        template='plotly_white',
        height=400,
        yaxis_range=[0, 110]
    )
    
    return fig

def plot_cost_comparison(cost_summary: Dict) -> go.Figure:
    """
    Create cost comparison visualization.
    
    Args:
        cost_summary: Cost summary dictionary from cost_model
        
    Returns:
        Plotly figure object
    """
    # Prepare data
    categories = ['Ground Station<br>Only', 'Crosslinked']
    costs = [
        cost_summary['gs_only_capex'],
        cost_summary['crosslinked_capex']
    ]
    
    # Create bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=categories,
        y=costs,
        marker_color=['#FF6B6B', '#4ECDC4'],
        text=[f'${costs[0]/1e6:.1f}M', f'${costs[1]/1e6:.1f}M'],
        textposition='outside',
        hovertemplate='%{x}<br>Cost: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Total CapEx Comparison',
        yaxis_title='Cost (USD)',
        template='plotly_white',
        height=400,
        showlegend=False
    )
    
    return fig

def plot_cost_breakdown(cost_summary: Dict) -> go.Figure:
    """
    Create stacked bar chart showing cost breakdown.
    
    Args:
        cost_summary: Cost summary dictionary from cost_model
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Ground Station Only breakdown
    gs_only = cost_summary['gs_only_breakdown']
    fig.add_trace(go.Bar(
        name='Ground Stations',
        x=['Ground Station Only'],
        y=[gs_only['Ground Stations']],
        marker_color='#95E1D3',
        hovertemplate='Ground Stations: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Satellites',
        x=['Ground Station Only'],
        y=[gs_only['Satellites']],
        marker_color='#FFB6B9',
        hovertemplate='Satellites: $%{y:,.0f}<extra></extra>'
    ))
    
    # Crosslinked breakdown
    cl = cost_summary['crosslinked_breakdown']
    fig.add_trace(go.Bar(
        name='Ground Stations',
        x=['Crosslinked'],
        y=[cl['Ground Stations']],
        marker_color='#95E1D3',
        showlegend=False,
        hovertemplate='Ground Stations: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Satellites',
        x=['Crosslinked'],
        y=[cl['Satellites']],
        marker_color='#FFB6B9',
        showlegend=False,
        hovertemplate='Satellites: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='ISL Hardware',
        x=['Crosslinked'],
        y=[cl['ISL Hardware']],
        marker_color='#4ECDC4',
        hovertemplate='ISL Hardware: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Cost Breakdown by Component',
        yaxis_title='Cost (USD)',
        barmode='stack',
        template='plotly_white',
        height=400
    )
    
    return fig

def plot_link_type_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Create pie chart showing distribution of link types.
    
    Args:
        df: Simulation results dataframe
        
    Returns:
        Plotly figure object
    """
    link_counts = df['link_type'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=link_counts.index,
        values=link_counts.values,
        hole=0.3,
        marker_colors=['#4ECDC4', '#FF6B6B'],
        textinfo='label+percent',
        hovertemplate='%{label}<br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title='Link Type Distribution',
        template='plotly_white',
        height=400
    )
    
    return fig

def plot_satellite_coverage_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Create heatmap showing coverage per satellite over time.
    
    Args:
        df: Simulation results dataframe
        
    Returns:
        Plotly figure object
    """
    # Pivot data for heatmap
    pivot_data = df.pivot_table(
        values='is_feasible',
        index='satellite_id',
        columns='time_step',
        aggfunc='mean'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='Viridis',
        hovertemplate='Satellite: %{y}<br>Time Step: %{x}<br>Coverage: %{z:.2f}<extra></extra>',
        colorbar=dict(title='Coverage')
    ))
    
    fig.update_layout(
        title='Satellite Coverage Over Time',
        xaxis_title='Time Step',
        yaxis_title='Satellite ID',
        template='plotly_white',
        height=400
    )
    
    return fig

def plot_distance_distribution(df_ground: pd.DataFrame, df_crosslink: pd.DataFrame) -> go.Figure:
    """
    Create histogram comparing link distance distributions.
    
    Args:
        df_ground: Ground-station-only simulation results
        df_crosslink: Crosslinked simulation results
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Ground station distances
    fig.add_trace(go.Histogram(
        x=df_ground['distance_m'] / 1000,  # Convert to km
        name='Ground Station Only',
        marker_color='#FF6B6B',
        opacity=0.7,
        nbinsx=30
    ))
    
    # Crosslink distances
    fig.add_trace(go.Histogram(
        x=df_crosslink['distance_m'] / 1000,  # Convert to km
        name='Crosslinked',
        marker_color='#4ECDC4',
        opacity=0.7,
        nbinsx=30
    ))
    
    fig.update_layout(
        title='Link Distance Distribution',
        xaxis_title='Distance (km)',
        yaxis_title='Frequency',
        barmode='overlay',
        template='plotly_white',
        height=400
    )
    
    return fig

