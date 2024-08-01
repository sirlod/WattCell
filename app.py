# -*- coding: utf-8 -*-
'''
Created on 27/07/2024

@authors: Marcin Orzech, Ashley Willow

This is a frontend of the app. 
The app allows to quickly estimate critical parameters
 of a battery cell performance
based on set of inputs from user. 
The results are reasonable, however the calculations
don't take into account all details and factors, 
especially related to power, cycle life or manufacturing.
There are also limited constraints on some values, 
but the user should always think if the inputs are realistic.
'''

# Import Python Libraries
import pandas as pd
import streamlit as st
from cell_components import (
    materials,
    Electrode,
    Separator,
    Electrolyte,
    Pouch,
    Tab,
    Cell,
)
from graphs import generate_energy_density_data, plot_energy_density

config = {'displaylogo': False}

# Initialize session state
if 'anode_free' not in st.session_state:
    st.session_state.anode_free = False


# Callback function to update session state
def is_anode_free():
    st.session_state.anode_free = st.session_state.anode_free


def page_config():
    '''Setups page settings and menu options.
    Must be called as first streamlit command.'''
    st.set_page_config(
        page_title='WattCell',
        page_icon='assets/favicon.ico',
        layout='wide',
        menu_items={
            'Get Help': None,
        },
    )


def design_cell():

    st.header('Cell Properties:')
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.write('### Cathode:')
        cathode_am = st.selectbox(
            'Cathode active material', materials['cathodes'].keys()
        )
        cathode_binder = st.selectbox('Binder type', materials['binders'].keys())
        porosity = st.slider('Porosity (%)', 0, 100, value=25) / 100
        voltage = st.slider(
            'Voltage (V)',
            1.0,
            5.0,
            step=0.05,
            value=materials['cathodes'][cathode_am]['voltage'],
        )
        capacity = st.number_input(
            'Capacity (mAh/g)', 0, value=materials['cathodes'][cathode_am]['capacity']
        )
        density_am = st.number_input(
            'Active material density',
            0.0,
            value=materials['cathodes'][cathode_am]['density'],
        )
        thickness = st.slider('Cathode thickness (um)', 0, 150, value=80)
        cathode_placeholder = st.empty()
        width = st.number_input('Cathode width (mm)', 0, value=43)
        height = st.number_input('Cathode height (mm)', 0, value=56)
        cathode_cc = st.selectbox(
            'Cathode current collector', materials['current_collectors'].keys()
        )
        cathode_cc_thickness = st.number_input(
            'Current collector thickness (um)',
            value=materials['current_collectors'][cathode_cc]['thickness'],
        )

        st.write('#### Mass ratios:')
        c_am = st.number_input('AM', 0, 100, value=96)
        c_carbon = st.number_input(
            'carbon', 0, (100 - c_am), value=int((100 - c_am) / 2)
        )
        c_binder = st.number_input(
            'binder', value=int(100 - c_am - c_carbon), disabled=True
        )

    cathode = Electrode(
        active_material=cathode_am,
        mass_ratio={
            'am': c_am / 100,
            'carbon': c_carbon / 100,
            'binder': c_binder / 100,
        },
        binder=cathode_binder,
        porosity=porosity,
        voltage=voltage,
        capacity=capacity,
        density_am=density_am,
        width=width / 10,
        height=height / 10,
        thickness=thickness / 10000,
        current_collector=cathode_cc,
        cc_thickness=cathode_cc_thickness / 10000,
    )

    with c2:
        st.write('### Anode:')
        anode_am = st.selectbox('Anode active material', materials['anodes'].keys())
        anode_binder = st.selectbox(
            'Binder type', materials['binders'].keys(), index=1, key='anode_binder'
        )
        anode_porosity = (
            st.slider(
                'Porosity (%)',
                0,
                100,
                value=25,
                key='anode_por',
                disabled=st.session_state.anode_free,
            )
            / 100
        )
        anode_voltage = st.slider(
            'Voltage (V)',
            0.0,
            3.0,
            step=0.05,
            value=materials['anodes'][anode_am]['voltage'],
            key='anode_V',
        )
        anode_capacity = st.number_input(
            'Capacity (mAh/g)',
            0,
            value=materials['anodes'][anode_am]['capacity'],
            key='anode_cap',
        )
        anode_density_am = st.number_input(
            'Active material density',
            0.0,
            value=materials['anodes'][anode_am]['density'],
            key='anode_am_d',
        )
        placeholder = st.empty()
        st.info(f'Anode width (mm): {cathode.width*10 + 2:.0f}')
        st.info(f'Anode height (mm): {cathode.height*10 + 2:.0f}')
        anode_cc = st.selectbox(
            'Anode current collector', materials['current_collectors'].keys()
        )
        anode_cc_thickness = st.number_input(
            'Current collector thickness (um)',
            value=materials['current_collectors'][anode_cc]['thickness'],
            key='anode_cc_thickness',
        )

        st.write('#### Mass ratios:')
        a_am = st.number_input(
            'AM', 0, 100, value=96, key='anode_am', disabled=st.session_state.anode_free
        )
        a_carbon = st.number_input(
            'carbon',
            0,
            (100 - a_am),
            value=int((100 - a_am) / 2),
            key='anode_c',
            disabled=st.session_state.anode_free,
        )
        a_binder = st.number_input(
            'binder', value=int(100 - a_am - a_carbon), key='anode_b', disabled=True
        )

    anode = Electrode(
        active_material=anode_am,
        current_collector=anode_cc,
        mass_ratio={
            'am': a_am / 100,
            'carbon': a_carbon / 100,
            'binder': a_binder / 100,
        },
        binder=anode_binder,
        porosity=anode_porosity,
        voltage=anode_voltage,
        capacity=anode_capacity,
        density_am=anode_density_am,
        width=cathode.width + 0.2,
        height=cathode.height + 0.2,
        cc_thickness=anode_cc_thickness / 10000,
    )

    with c3:
        st.write('### Separator:')
        separator_name = st.selectbox('Separator name', materials['separators'].keys())
        separator_thickness = st.number_input(
            'Separator thickness (um)',
            value=materials['separators'][separator_name]['thickness'],
        )
        separator_porosity = (
            st.slider(
                'Separator porosity (%)',
                0,
                100,
                value=int(materials['separators'][separator_name]['porosity'] * 100),
            )
            / 100
        )
        separator_density = st.number_input(
            'Separator density (g/cm³)',
            value=materials['separators'][separator_name]['density'],
        )

    separator = Separator(
        material=separator_name,
        width=anode.width,
        height=anode.height + 0.2,
        thickness=separator_thickness / 10000,
        porosity=separator_porosity,
        density=separator_density,
    )

    with c3:
        '---'
        st.write('### Electrolyte:')
        electrolyte_type = st.selectbox(
            'Electrolyte type', materials['electrolytes'].keys()
        )
        electrolyte_density = st.number_input(
            'Electrolyte density (g/cm³)',
            value=materials['electrolytes'][electrolyte_type]['density'],
        )
        electrolyte_excess = st.slider('Excess electrolyte (%)', 0, 50, value=0) / 100
        calc_elec = st.empty()

        electrolyte = Electrolyte(
            material=electrolyte_type,
            density=electrolyte_density,
            volume_excess=electrolyte_excess,
        )

    with c4:
        st.write('### Cell Configuration:')
        anode_free = st.checkbox(
            'Anode free cell',
            key='anode_free',
            on_change=is_anode_free,
            help='Will set n/p to 1, porosity of anode to 0% and anode AM mass ratio to 100%',
        )
        layers_number = st.slider('Number of layers', 1, 40, value=20, step=1)
        cell_t_placeholder = st.empty()
        n_p_ratio = st.slider(
            'N/P Ratio', 0.0, 1.5, value=1.1, step=0.05, disabled=anode_free
        )
        ice = st.slider('Initial Coulombic Efficiency (%)', 50, 100, value=93) / 100

        '---'
        st.write('### Pouch:')
        pouch_thickness = st.number_input(
            'Pouch thickness (um)', value=materials['pouch']['thickness']
        )
        pouch_density = st.number_input(
            'Pouch density (g/cm³)', value=materials['pouch']['density']
        )

        '---'
        st.write('### Tabs:')
        tabs_material_cathode = st.selectbox(
            'Cathode tab material', materials['tabs'].keys()
        )
        tabs_material_anode = st.selectbox(
            'Anode tab material', materials['tabs'].keys()
        )
        tabs_height = st.number_input('Tabs height (mm)', value=80)
        tabs_width = st.number_input('Tabs width (mm)', value=8)
        tabs_thickness = st.number_input('Tabs thickness (mm)', value=0.2)

    pouch = Pouch(
        width=separator.width + materials['pouch']['extra_width'],
        height=separator.height + materials['pouch']['extra_height'],
        thickness=pouch_thickness / 10000,
        density=pouch_density,
    )
    tabs = Tab(
        material_cathode=tabs_material_cathode,
        material_anode=tabs_material_anode,
        height=tabs_height / 10,
        width=tabs_width / 10,
        thickness=tabs_thickness / 10,
    )

    designed_cell = Cell(
        cathode,
        anode,
        separator,
        electrolyte,
        pouch,
        tabs,
        layers_number,
        n_p_ratio,
        ice,
    )

    if anode_free:
        recalculate_anodefree_energy(designed_cell)

    # insert calculated cell values to the layout
    with cathode_placeholder.container():
        st.info(f'AM mass loading (mg/cm2): {cathode.am_mass_loading:.1f}')
        st.info(f'Areal capacity (mAh/cm2): {cathode.areal_capacity:.1f}')
    with placeholder.container():
        st.info(f'Anode Thickness (um): {anode.thickness*10000:.0f}')
        st.info(f'AM mass loading (mg/cm2): {anode.am_mass_loading:.1f}')
        st.info(f'Areal capacity (mAh/cm2): {anode.areal_capacity:.1f}')
    with calc_elec.container():
        st.info(f'Volume: {electrolyte.volume:.2f} mL')
        st.info(f'Volume per Ah: {electrolyte.volume_per_ah:.2f} mL/Ah')
    with cell_t_placeholder.container():
        st.info(f'Cell thickness: {designed_cell.total_thickness:.1f} mm')

    return designed_cell


def recalculate_anodefree_energy(cell):
    cell.n_p_ratio = 1
    cell.anode.porosity = 0
    cell.anode.mass_ratio['am'] = 1
    cell.anode.mass_ratio['carbon'] = 0
    cell.anode.mass_ratio['binder'] = 0
    cell.anode.calculate_composite_density()
    cell.calculate_anode_properties()
    cell.calculate_energy_density()
    cell.anode_free_energy()


def print_cell_metrics(cell):

    with st.sidebar:
        st.write('# Calculated Cell Performance:')

        st.metric('Total Mass', f'{cell.total_mass:.2f} g')
        st.metric('Total Volume', f'{cell.total_volume:.2f} cm³')

        st.metric('Capacity', f'{cell.capacity:.2f} Ah')
        st.metric('Energy', f'{cell.energy:.2f} Wh')

        st.metric('Specific Energy', f'{cell.gravimetric_energy_density:.1f} Wh/kg')
        st.metric('Energy Density', f'{cell.volumetric_energy_density:.1f} Wh/L')


def energy_density_graph(cell):
    st.header('Energy Density Graph')
    parameters = [
        'Number of layers',
        'Cathode thickness (um)',
        'Cathode porosity (%)',
        'Cathode capacity (mAh/g)',
    ]
    parameter = st.selectbox('Select parameter to vary', parameters)

    col1, col2 = st.columns(2)

    with col1:
        start = st.number_input('Start value', value=1)
    with col2:
        end = st.number_input('End value', value=100)

    steps = st.slider('Number of steps', min_value=10, max_value=100, value=50)

    if st.button('Generate Graph'):
        df = generate_energy_density_data(
            cell, parameter, start, end, steps, st.session_state.anode_free
        )

        fig = plot_energy_density(df, parameter)
        st.plotly_chart(fig, use_container_width=True)

        st.download_button(
            label='Download data as CSV',
            data=df.to_csv().encode('utf-8'),
            file_name=f'energy_density_vs_{parameter}.csv',
            mime='text/csv',
        )


page_config()
battery = design_cell()
print_cell_metrics(battery)
'---'
energy_density_graph(battery)

df = pd.DataFrame([battery])
st.dataframe(df, use_container_width=True)
