# -*- coding: utf-8 -*-
'''
Created on 27/07/2024

@author: Marcin Orzech
'''

# Import Python Libraries
import pandas as pd
import streamlit as st
import plotly.express as px


config = {'displaylogo': False}

def page_config():
    '''Setups page settings and menu options.
    Must be called as first streamlit command.'''
    st.set_page_config(
        page_title='WattCalc',
        page_icon='assets/favicon.ico',
        layout='wide',
        menu_items={
            'Get Help': None,
        },
    )


def input_values():

    materials = {
        'Cu':{
            'density': 8.94
        },
        'Al':{
            'density': 2.7
        },
        'Prussian Blue': {
            'density': 1.8, # in g/cm3
            'capacity': 150, # in Ah/kg
            'voltage': 3.2
        },
        'Hard Carbon': {
            'capacity': 300,
        },
        'SuperP':{
            'density': 1.9
        },
        'PVDF':{
            'density': 1.78
        },
        'CMC+SBR':{
            'density': (1.6+0.96)/2
        }
    }


    cathode_am = st.selectbox('Cathode active material',['Prussian Blue'])
    binder_cathode = st.selectbox('Binder type',['PVDF', 'CMC+SBR'])
    porosity = st.number_input('Porosity (%)', 0, 100, value=25)/100
    voltage = st.number_input('voltage (V)',0.0,value=materials[cathode_am]['voltage'])
    capacity = st.number_input('Cathode capacity (Ah/kg)',0,value=materials[cathode_am]['capacity'])
    density_am = st.number_input('Active material density',0.0,value=materials[cathode_am]['density'])
    width = st.number_input('Cathode width (mm)', 0, value=43)
    height = st.number_input('Cathode height (mm)', 0, value=56)
    thickness = st.number_input('Cathode thickness (mm)', 0.0, value=0.025)

    # ratios
    c_am = st.number_input('AM', 0, 100, value=96)/100
    c_carbon = st.number_input('carbon', 0, 100, value=(100-int(c_am*100)))/100
    c_binder = st.number_input('binder', 0, 100, value=int((1 - c_am - c_carbon)*100))/100

    cathode = {
        'active_material': cathode_am,
        'mass_ratio': {
            'am': c_am,
            'carbon': c_carbon,
            'binder': c_binder,
        },
        'binder': binder_cathode,
        'porosity': porosity,
        'voltage': voltage,
        'capacity': capacity,
        'density_am': density_am,
        'width': width, # in mm
        'height': height, # in mm
        'thickness': thickness, # in mm
        'current_collector': 'Al',
        'tab_height': 10, # in mm
        'tab_width': 10, # in mm
    }
    volumes_cathode = {
        'am': cathode['mass_ratio']['am']/cathode['density_am'],
        'carbon': cathode['mass_ratio']['carbon']/materials['SuperP']['density'],
        'binder': cathode['mass_ratio']['binder']/materials[cathode['binder']]['density']
    }
    volume_ratios = {
        'am': volumes_cathode['am']/sum(volumes_cathode.values()),
        'carbon': volumes_cathode['carbon']/sum(volumes_cathode.values()),
        'binder': volumes_cathode['binder']/sum(volumes_cathode.values())
    }
    total_density = (1 - cathode['porosity']) * (
        volume_ratios['am']*cathode['density_am'] +
        volume_ratios['carbon']*materials['SuperP']['density'] +
        volume_ratios['binder']*materials[cathode['binder']]['density']
        )
    cathode['density_total'] = total_density

    st.write(cathode)
    anode = {
        'active_material': 'none',
        'current_collector': 'Al',
        'width': cathode['width'] + 2,
        'height': cathode['height'] + 2,
        'thickness': 0.01,  # in mm
        'tab_height': 10,  # in mm
        'tab_width': 10,  # in mm
    }

    current_collector = {
        'anode': 'Al',
        'cathode': 'Al',
        'anode_thickness': 0.01,
        'cathode_thickness': 0.01
    }

    separator = {
        'name': 'celgard 2325',
        'width': anode['width'],
        'height': anode['height'] + 2,
        'thickness': 0.025,  # in mm
        'porosity': 0.41,
        'density': 0.74  # from https://core.ac.uk/download/pdf/288499223.pdf
    }

    pouch = {
        'width': separator['width'] + 9,
        'height': separator['height'] + 20,
        'thickness': 0.113, # in mm
        'density': 1.62
    }

    tabs = {
        'material': 'Al',
        'height': 80,
        'width': 8,
        'thickness': 0.2, # in mm
    }
    tabs['density'] = materials.get(tabs['material'])['density']

    df_cell = pd.DataFrame([cathode, anode, current_collector, separator, pouch, tabs],
                        index=['cathode', 'anode', 'mass_ratio', 'separator', 'pouch', 'tabs']).T

    return df_cell

def backend_calc():
    '''
    calculate intermidiate results here
    mass of each item
    volume of each item
    volume ratios
    electrodes density
    electrodes volume (coated)
    area of electrodes
    mass of electrolyte
    total void volume
    '''

def calculate_energy(inputs):
    '''
    calculation of final values based in background calculations and inputs
    results:
    total mass
    total volume
    capacity
    energy
    specific energy
    energy density

    '''
    cell = inputs

input_values()
# calculate_energy(input_values())
