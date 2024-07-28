# -*- coding: utf-8 -*-
'''
Created on 27/07/2024

@author: Marcin Orzech
'''

# Import Python Libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from cell_components import materials, Electrode, Separator, Electrolyte, Pouch, Tab, Cell


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

    st.header('Cell Properties:')
    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.write('### Cathode:')
        cathode_am = st.selectbox('Cathode active material',['Prussian Blue'])
        cathode_binder = st.selectbox('Binder type',['PVDF', 'CMC+SBR'])
        porosity = st.slider('Porosity (%)', 0, 100, value=25)/100
        voltage = st.number_input('Voltage (V)',0.0,value=materials[cathode_am]['voltage'])
        capacity = st.number_input('Capacity (Ah/kg)',0,value=materials[cathode_am]['capacity'])
        density_am = st.number_input('Active material density',0.0,value=materials[cathode_am]['density'])
        thickness = st.number_input('Cathode thickness (um)', 0, value=25)/10000
        width = st.number_input('Cathode width (mm)', 0, value=43)
        height = st.number_input('Cathode height (mm)', 0, value=56)
        cathode_cc = st.selectbox('Cathode current collector',['Al', 'Cu'])
        cathode_cc_thickness = st.number_input('Current collector thickness (um)',
                                                value=materials[cathode_cc]['thickness'])/10000


        st.write('#### Mass ratios:')
        c_am = st.number_input('AM', 0, 100, value=96)/100
        c_carbon = st.number_input('carbon', 0, (100-int(c_am*100)), value=(100-int(c_am*100)))/100
        c_binder = st.number_input('binder', value=int((1 - c_am - c_carbon)*100), disabled=True)/100

    cathode = Electrode(
        active_material=cathode_am,
        mass_ratio={'am': c_am, 'carbon': c_carbon, 'binder': c_binder},
        binder=cathode_binder,
        porosity=porosity,
        voltage=voltage,
        capacity=capacity,
        density_am=density_am,
        width=width,
        height=height,
        thickness=thickness,
        current_collector=cathode_cc,
        cc_thickness=cathode_cc_thickness
    )

    with c2:
        st.write('### Anode:')
        anode_am = st.selectbox('Anode active material',['Hard Carbon'])
        anode_binder = st.selectbox('Binder type',['PVDF', 'CMC+SBR'], index=1, key='anode_binder')
        anode_porosity = st.slider('Porosity (%)', 0, 100, value=25, key='anode_por')/100
        anode_voltage = st.number_input('Voltage (V)',0.0,value=materials[anode_am]['voltage'], key='anode_V')
        anode_capacity = st.number_input('Capacity (Ah/kg)',0,value=materials[anode_am]['capacity'], key='anode_cap')
        anode_density_am = st.number_input('Active material density',0.0,value=materials[anode_am]['density'], key='anode_am_d')
        anode_thickness = st.number_input('Anode Thickness (um)', 0, value=25)/1000
        st.info(f'Anode width (mm): {cathode.width + 2}')
        st.info(f'Anode height (mm): {cathode.height + 2}')
        anode_cc = st.selectbox('Anode current collector',['Al', 'Cu'])
        anode_cc_thickness = st.number_input('Current collector thickness (um)', 
                                            value=materials[anode_cc]['thickness'],
                                            key='anode_cc_thickness')/10000

        st.write('#### Mass ratios:')
        a_am = st.number_input('AM', 0, 100, value=96, key='anode_am')/100
        a_carbon = st.number_input('carbon', 0, (100-int(a_am*100)), value=(100-int(a_am*100)), key='anode_c')/100
        a_binder = st.number_input('binder', value=int((1 - a_am - a_carbon)*100), key='anode_b', disabled=True)/100

    anode = Electrode(
        active_material=anode_am,
        current_collector=anode_cc,
        mass_ratio={'am': a_am, 'carbon': a_carbon, 'binder': a_binder},
        binder=anode_binder,
        porosity=anode_porosity,
        voltage=anode_voltage,
        capacity=anode_capacity,
        density_am=anode_density_am,
        width=cathode.width + 2,
        height=cathode.height + 2,
        thickness=anode_thickness,
        cc_thickness=anode_cc_thickness
    )

    with c3:
        st.write('### Separator:')
        separator_name = st.selectbox('Separator name', ['Celgard 2325'])
        separator_thickness = st.number_input('Separator thickness (um)', value=materials[separator_name]['thickness']) / 1000
        separator_porosity = st.slider('Separator porosity (%)', 0, 100,
                                        value=int(materials[separator_name]['porosity']*100)) / 100
        separator_density = st.number_input('Separator density (g/cm³)',
                                            value=materials[separator_name]['density'])

    separator = Separator(
        material=separator_name,
        width=anode.width,
        height=anode.height + 2,
        thickness=separator_thickness,
        porosity=separator_porosity,
        density=separator_density
    )

    with c3:
        st.write('### Electrolyte:')
        electrolyte_type = st.selectbox('Electrolyte type', materials['electrolytes'].keys())
        electrolyte_density = st.number_input('Electrolyte density (g/cm³)', 
                                            value=materials['electrolytes'][electrolyte_type]['density'])
        
        electrolyte = Electrolyte(
        material=electrolyte_type,
        density=electrolyte_density
    )

    with c3:
        st.write('### Pouch:')
        pouch_thickness = st.number_input('Pouch thickness (um)', value=materials['pouch']['thickness']) / 1000
        pouch_density = st.number_input('Pouch density (g/cm³)', value=materials['pouch']['density'])

        st.write('### Tabs properties:')
        tabs_material = st.selectbox('Tabs material', materials['tabs'].keys())
        tabs_height = st.number_input('Tabs height (mm)', value=80)
        tabs_width = st.number_input('Tabs width (mm)', value=8)
        tabs_thickness = st.number_input('Tabs thickness (mm)',
                                        value=materials['tabs'][tabs_material]['thickness']) / 10
        

    pouch = Pouch(
        width=separator.width + materials['pouch']['extra_width'],
        height=separator.height + materials['pouch']['extra_height'],
        thickness=pouch_thickness,
        density=pouch_density
    )
    tabs = Tab(
        material=tabs_material,
        height=tabs_height,
        width=tabs_width,
        thickness=tabs_thickness
    )

    df_cell = pd.DataFrame([cathode, anode, separator, electrolyte, pouch, tabs],
                        index=['cathode', 'anode', 'separator', 'electrolyte', 'pouch', 'tabs']).T
    
    st.dataframe(df_cell,use_container_width=True)

    battery = Cell(cathode, anode, separator, electrolyte, pouch, tabs)

    return battery

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



page_config()
input_values()
# calculate_energy(input_values())
