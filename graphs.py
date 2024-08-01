import numpy as np
import plotly.graph_objects as go
import pandas as pd
from copy import deepcopy

def generate_energy_density_data(cell, parameter, start, end, steps, anodefree):
    x_values = np.linspace(start, end, steps)
    results = pd.DataFrame()

    for x in x_values:
        # Create a deep copy of the cell to avoid modifying the original
        cell_copy = deepcopy(cell)

        if parameter == 'Number of layers':
            cell_copy.layers_number = int(x)
        elif parameter == 'Cathode thickness (um)':
            cell_copy.cathode.thickness = x / 10000  # Convert um to cm
        elif parameter == 'Cathode porosity (%)':
            cell_copy.cathode.porosity = x / 100  # Convert percentage to decimal
        elif parameter == 'Cathode capacity (mAh/g)':
            cell_copy.cathode.capacity = x
        
        cell_copy.anode.calculate_composite_density()
        cell_copy.cathode.calculate_composite_density()
        cell_copy.cathode.calculate_areal_capacity()
        cell_copy.calculate_anode_properties()
        cell_copy.calculate_energy_density()
        if anodefree:
            cell_copy.anode_free_energy()

        df = pd.DataFrame([cell_copy])
        df[parameter] = x
        results = pd.concat([results, df], ignore_index=True)

    return results

def plot_energy_density(df, parameter):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=df[parameter], y=df['gravimetric_energy_density'], 
                             mode='lines', name='Gravimetric Energy Density'))
    fig.add_trace(go.Scatter(x=df[parameter], y=df['volumetric_energy_density'], 
                             mode='lines', name='Volumetric Energy Density'))
    
    fig.update_layout(
        title=f'Energy Density vs {parameter.capitalize()}',
        xaxis_title=parameter.capitalize(),
        yaxis_title='Energy Density',
        legend_title='Energy Density Type'
    )
    
    return fig
