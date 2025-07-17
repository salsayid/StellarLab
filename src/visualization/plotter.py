# src/visualization/plotter.py

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_results_plotly(results):
    """
    Generates and returns an interactive Plotly figure.
    Args:
        results (dict): The dictionary of simulation data.
    Returns:
        go.Figure: A Plotly figure object.
    """
    time = results['time']
    stage = results['stage']

    # Create subplots
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=('Altitude vs. Time', 'Velocity vs. Time', 'Mass vs. Time', 'Thrust vs. Time')
    )

    # Add traces
    fig.add_trace(go.Scatter(x=time, y=results['altitude'], name='Altitude (km)', mode='lines', line=dict(color='cyan')), row=1, col=1)
    fig.add_trace(go.Scatter(x=time, y=results['velocity'], name='Velocity (m/s)', mode='lines', line=dict(color='lime')), row=2, col=1)
    fig.add_trace(go.Scatter(x=time, y=results['mass'], name='Mass (kg)', mode='lines', line=dict(color='magenta')), row=3, col=1)
    fig.add_trace(go.Scatter(x=time, y=results['thrust'], name='Thrust (N)', mode='lines', line=dict(color='yellow')), row=4, col=1)

    # Add stage separation lines
    stage_changes = np.where(np.diff(stage) != 0)[0]
    for change_idx in stage_changes:
        fig.add_vline(
            x=time[change_idx], 
            line_width=2, 
            line_dash="dash", 
            line_color="gray",
            annotation_text=f"Stage {stage[change_idx]} Sep",
            annotation_position="top right"
        )

    # Update layout
    fig.update_layout(
        title_text='StellarLab Mission Simulation Results',
        template='plotly_dark',
        height=900,
        showlegend=False
    )

    # Update y-axis titles
    fig.update_yaxes(title_text="Altitude (km)", row=1, col=1)
    fig.update_yaxes(title_text="Velocity (m/s)", row=2, col=1)
    fig.update_yaxes(title_text="Mass (kg)", row=3, col=1)
    fig.update_yaxes(title_text="Thrust (N)", row=4, col=1)
    fig.update_xaxes(title_text="Time (s)", row=4, col=1)

    return fig


# Kept for legacy CLI usage, but with a cooler theme
def plot_results_matplotlib(results):
    """
    Generates and displays plots for the simulation results using Matplotlib.
    Args:
        results (dict): The dictionary of simulation data.
    """
    plt.style.use('dark_background') # Use a dark theme
    time = results['time']
    altitude = results['altitude']
    velocity = results['velocity']
    mass = results['mass']
    thrust = results['thrust']
    stage = results['stage']

    fig, axs = plt.subplots(4, 1, figsize=(12, 18), sharex=True)
    fig.suptitle('StellarLab Mission Simulation Results', fontsize=16)

    # Plot 1: Altitude vs. Time
    axs[0].plot(time, altitude, 'c-', label='Altitude')
    axs[0].set_ylabel('Altitude (km)')
    axs[0].grid(True, alpha=0.3)
    axs[0].legend()

    # Plot 2: Velocity vs. Time
    axs[1].plot(time, velocity, 'g-', label='Velocity')
    axs[1].set_ylabel('Velocity (m/s)')
    axs[1].grid(True, alpha=0.3)
    axs[1].legend()

    # Plot 3: Mass vs. Time
    axs[2].plot(time, mass, 'm-', label='Total Mass')
    axs[2].set_ylabel('Mass (kg)')
    axs[2].grid(True, alpha=0.3)
    axs[2].legend()

    # Plot 4: Thrust vs. Time
    axs[3].plot(time, thrust, 'y-', label='Thrust')
    axs[3].set_ylabel('Thrust (N)')
    axs[3].set_xlabel('Time (s)')
    axs[3].grid(True, alpha=0.3)
    axs[3].legend()

    # Add vertical lines for stage separations
    stage_changes = np.where(np.diff(stage) != 0)[0]
    for ax in axs:
        for change_idx in stage_changes:
            ax.axvline(x=time[change_idx], color='gray', linestyle='--', linewidth=1.5, label=f'Stage Sep.')
    
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.show()
