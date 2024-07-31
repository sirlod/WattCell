import numpy as np
import plotly.graph_objects as go
import pandas as pd

def generate_energy_density_data(cell, parameter, start, end, steps, anodefree):
    x_values = np.linspace(start, end, steps)
    gravimetric_energy_density = []
    volumetric_energy_density = []
    
    for x in x_values:
        if parameter == 'Number of layers':
            cell.layers_number = int(x)
        elif parameter == 'Cathode thickness (um)':
            cell.cathode.thickness = x / 10000  # Convert um to cm
        elif parameter == 'Cathode porosity (%)':
            cell.cathode.porosity = x / 100  # Convert percentage to decimal
        elif parameter == 'Cathode capacity (mAh/g)':
            cell.cathode.capacity = x
        
        cell.anode.calculate_composite_density()
        cell.cathode.calculate_composite_density()
        cell.cathode.calculate_areal_capacity()
        cell.calculate_anode_properties()
        cell.calculate_energy_density()
        if anodefree:
            cell.anode_free_energy()
        
        gravimetric_energy_density.append(cell.gravimetric_energy_density)
        volumetric_energy_density.append(cell.volumetric_energy_density)
    
    return x_values, gravimetric_energy_density, volumetric_energy_density

def plot_energy_density(x_values, gravimetric_energy_density, volumetric_energy_density, parameter):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=x_values, y=gravimetric_energy_density, 
                             mode='lines', name='Gravimetric Energy Density'))
    fig.add_trace(go.Scatter(x=x_values, y=volumetric_energy_density, 
                             mode='lines', name='Volumetric Energy Density'))
    
    fig.update_layout(
        title=f'Energy Density vs {parameter.capitalize()}',
        xaxis_title=parameter.capitalize(),
        yaxis_title='Energy Density',
        legend_title='Energy Density Type'
    )
    
    return fig

def save_data_to_csv(x_values, gravimetric_energy_density, volumetric_energy_density, parameter):
    df = pd.DataFrame({
        parameter: x_values,
        'Gravimetric Energy Density (Wh/kg)': gravimetric_energy_density,
        'Volumetric Energy Density (Wh/L)': volumetric_energy_density
    })

    return df.to_csv().encode("utf-8")