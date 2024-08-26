# -*- coding: utf-8 -*-
'''
Created on 27/07/2024

@authors: Marcin Orzech, Ashley Willow

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
    Cylindrical,
    Prismatic,
    Tab,
    Cell,
)
from graphs import generate_energy_density_data, plot_energy_density

config = {'displaylogo': False}

# Initialize session state
if 'anode_free' not in st.session_state:
    st.session_state.anode_free = False
if 'cell_format' not in st.session_state:
    st.session_state.cell_format = 'Pouch'

# Callback function to update session state
def is_anode_free():
    st.session_state.anode_free = st.session_state.anode_free


def set_cell_format():
    st.session_state.cell_format = st.session_state.cell_format


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


def read_file(name):
    with open(name, "r") as file:
        text = file.read()
    return text


def design_cell():

    st.header('Cell Properties:')
    c1, c2, c3, c4 = st.columns(4)

    # collect user inputs
    with c1:
        st.write('### Cathode:')
        cathode_am = st.selectbox(
            'Cathode active material', materials['cathodes'].keys()
        )
        cathode_binder = st.selectbox(
            'Binder type', materials['binders'].keys()
            )
        porosity = st.slider('Porosity (%)', 0, 100, value=25) / 100
        voltage = st.slider(
            'Voltage (V)', 1.0, 5.0, step=0.05,
            value=materials['cathodes'][cathode_am]['voltage']
        )
        capacity = st.number_input(
            'Capacity (mAh/g)', 0, value=materials['cathodes'][cathode_am]['capacity'],
            help='First cycle charge capacity'
        )
        density_am = st.number_input(
            'Active material density',
            0.0,
            value=materials['cathodes'][cathode_am]['density'],
        )
        thickness = st.slider(
            'Cathode thickness (um)', 0, 150, value=80,
            help='Thickness of the coating'
            )
        cathode_placeholder = st.empty()
        if st.session_state.cell_format == 'Pouch':
            width = st.number_input('Cathode width (mm)', 0, value=150)
            height = st.number_input('Cathode height (mm)', 0, value=400)
        else:
            width = 0
            height = 0
        cathode_cc = st.selectbox(
            'Cathode current collector', materials['current_collectors'].keys(),
            help='For cathode almost always Aluminium foil is used'
        )
        cathode_cc_thickness = st.number_input(
            'Current collector thickness (um)',
            value=materials['current_collectors'][cathode_cc]['thickness']
        )

        st.write('#### Mass ratios:')
        c_am = st.number_input(
            'AM', 0, 100, value=95, help='Active Material'
            )
        c_carbon = st.number_input(
            'carbon', 0, (100 - c_am), value=int((100 - c_am) / 2)
        )
        c_binder = st.number_input(
            'binder', value=int(100 - c_am - c_carbon), disabled=True,
            help='Value calculated'
        )

    # write inputs into the object
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

    # collect user inputs
    with c2:
        st.write('### Anode:')
        anode_am = st.selectbox('Anode active material', materials['anodes'].keys())
        anode_binder = st.selectbox(
            'Binder type', materials['binders'].keys(), index=1, key='anode_binder'
        )
        anode_porosity = (
            st.slider(
                'Porosity (%)', 0, 100, value=25,
                key='anode_por', disabled=st.session_state.anode_free
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
            help='First cycle charge capacity'
        )
        anode_density_am = st.number_input(
            'Active material density',
            0.0,
            value=materials['anodes'][anode_am]['density'],
            key='anode_am_d',
        )
        # calculated values will be inserted in layout here
        anode_placeholder = st.empty()
        anode_cc = st.selectbox(
            'Anode current collector', materials['current_collectors'].keys(),
            help='Typically Cu for Li-ion and Al for Na-ion'
        )
        anode_cc_thickness = st.number_input(
            'Current collector thickness (um)',
            value=materials['current_collectors'][anode_cc]['thickness'],
            key='anode_cc_thickness',
        )

        st.write('#### Mass ratios:')
        a_am = st.number_input(
            'AM', 0, 100, value=96, key='anode_am',
            help='Active Material',
            disabled=st.session_state.anode_free
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
            'binder', value=int(100 - a_am - a_carbon),
            key='anode_b', disabled=True,
            help='Value calculated'
        )

    # write inputs into the object
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

    # collect user inputs
    with c3:
        st.write('### Separator:')
        separator_name = st.selectbox(
            'Separator name', materials['separators'].keys()
            )
        separator_thickness = st.number_input(
            'Separator thickness (um)',
            value=materials['separators'][separator_name]['thickness'],
        )
        separator_porosity = (
            st.slider(
                'Separator porosity (%)', 0, 100,
                value=int(materials['separators'][separator_name]['porosity'] * 100),
            )
            / 100
        )
        separator_density = st.number_input(
            'Separator density (g/cm³)',
            value=materials['separators'][separator_name]['density'],
        )

    # write inputs into the object
    separator = Separator(
        material=separator_name,
        width=anode.width,
        height=anode.height + 0.2,
        thickness=separator_thickness / 10000,
        porosity=separator_porosity,
        density=separator_density,
    )

    # collect user inputs
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

        cell_format_selector = st.radio(
            'Cell Format',
            ['Pouch', 'Cylindrical', 'Prismatic'],
            key='cell_format',
            on_change=set_cell_format,
            horizontal=True
            )
        if st.session_state.cell_format == 'Prismatic':
            structure = st.radio('Cell structure', ['Wound', 'Z-stacked'], label_visibility='hidden')
        '---'

        anode_free = st.checkbox(
            'Anode free cell',
            key='anode_free',
            on_change=is_anode_free,
            help='''
            Will set n/p to 1,
            porosity of anode to 0% and anode AM mass ratio to 100%. 
            User still has to select correct Anode active material 
            (Li or Na metal).
            ''',
        )
        if st.session_state.cell_format == 'Pouch':
            layers_number = st.slider('Number of layers', 1, 40, value=30, step=1)
        cell_t_placeholder = st.empty()  # placeholder to insert calculated thickness
        n_p_ratio = st.slider(
            'N/P Ratio', 0.0, 1.5, value=1.1, step=0.05, disabled=anode_free
        )
        ice = st.slider(
            'Initial Coulombic Efficiency (%)', 50, 100, value=93,
            help='Consider first cycle loses of both cathode and anode.'
            ) / 100
        extra_mass = st.number_input(
            'Extra mass (g)', value=3,
            help='Unaccounted mass of the tape, tabs (except pouch), vents, seals, and other small components'
            )

        '---'
        if st.session_state.cell_format == 'Pouch':
            st.write('### Pouch:')
            pouch_thickness = st.number_input(
                'Pouch thickness (um)', value=materials['formats']['pouch']['thickness']
            )
            pouch_density = st.number_input(
                'Pouch density (g/cm³)', value=materials['formats']['pouch']['density']
            )

            '---'
            st.write('### Tabs:')
            tabs_material_cathode = st.selectbox(
                'Cathode tab material', materials['tabs'].keys(),
                help='Typically Aluminium for cathode'
            )
            tabs_material_anode = st.selectbox(
                'Anode tab material', materials['tabs'].keys(),
                help='Typically Nickel for anode'
            )
            tabs_height = st.number_input('Tabs height (mm)', value=20)
            tabs_width = st.number_input('Tabs width (mm)', value=50)
            tabs_thickness = st.number_input('Tabs thickness (mm)', value=0.5)
        elif st.session_state.cell_format == 'Cylindrical':
            st.write('### Cylindrical can:')
            cell_type = st.selectbox('Cell size', materials['formats']['cylindrical'])
            cylinder_diameter = st.number_input(
                'Diameter (mm)', value=materials['formats']['cylindrical'][cell_type]['diameter']
                )
            cylinder_height = st.number_input(
                'Height (mm)', value=materials['formats']['cylindrical'][cell_type]['height']
                )
            cylinder_can_thickness = st.number_input(
                'Can thickness (mm)', value=materials['formats']['cylindrical'][cell_type]['can_thickness']
                )
            can_material = st.radio('Can material', materials['can_density'])
            cylinder_can_density = st.number_input('Can density (g/cm³)', value=materials['can_density'][can_material])
            cylinder_mandrel_diam = st.number_input(
                'Mandrel diameter (mm)', value=materials['formats']['cylindrical'][cell_type]['mandrel_dia']
                )
            cylinder_headspace = st.number_input(
                'Headspace (mm)', value=materials['formats']['cylindrical'][cell_type]['headspace']
                )
        elif st.session_state.cell_format == 'Prismatic':
            st.write('### Prismatic can:')
            prismatic_width = st.number_input('Can width (mm)', value=173)
            prismatic_height = st.number_input('Can height (mm)', value=115)
            prismatic_depth = st.number_input('Can depth (mm)', value=45)
            prismatic_can_thickness = st.number_input('Can wall thickness (mm)', value=1.1)
            can_material = st.radio('Can material', materials['can_density'], index=1)
            prismatic_can_density = st.number_input('Can density (g/cm³)', value=materials['can_density'][can_material])
            prismatic_headspace = st.number_input('Headspace (mm)', value=5)

            '---'
            st.write('### Tabs:')
            tabs_material_cathode = st.selectbox(
                'Cathode tab material', materials['tabs'].keys(),
                help='Typically Aluminium for cathode'
            )
            tabs_material_anode = st.selectbox(
                'Anode tab material', materials['tabs'].keys(),
                help='Typically Nickel for anode'
            )
            tabs_height = st.number_input('Tabs height (mm)', value=20)
            tabs_width = st.number_input('Tabs width (mm)', value=30)
            tabs_thickness = st.number_input('Tabs thickness (mm)', value=0.5)

    # write inputs into the object
    if st.session_state.cell_format == 'Pouch':
        cell_format = Pouch(
            width=separator.width + materials['formats']['pouch']['extra_width'],
            height=separator.height + materials['formats']['pouch']['extra_height'],
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

    elif st.session_state.cell_format == 'Cylindrical':
        cell_format = Cylindrical(
            diameter=cylinder_diameter / 10,
            height=cylinder_height / 10,
            can_thickness=cylinder_can_thickness / 10,
            can_density=cylinder_can_density,
            mandrel_diam=cylinder_mandrel_diam / 10,
            headspace=cylinder_headspace / 10
        )
        tabs = Tab()
        layers_number = None
    elif st.session_state.cell_format == 'Prismatic':
        cell_format = Prismatic(
            structure=structure,
            width=prismatic_width / 10,
            height=prismatic_height / 10,
            depth=prismatic_depth / 10,
            can_thickness=prismatic_can_thickness / 10,
            can_density=prismatic_can_density,
            headspace=prismatic_headspace / 10
        )
        tabs = Tab(
            material_cathode=tabs_material_cathode,
            material_anode=tabs_material_anode,
            height=tabs_height / 10,
            width=tabs_width / 10,
            thickness=tabs_thickness / 10,
        )
        layers_number = None  # Layers will be calculated in the Cell class


    designed_cell = Cell(
        cathode,
        anode,
        separator,
        electrolyte,
        cell_format,
        tabs,
        layers_number,
        n_p_ratio,
        ice,
        extra_mass
    )

    if anode_free:
        recalculate_anodefree_energy(designed_cell)

    # insert calculated cell values to the layout
    with cathode_placeholder.container():
        st.info(f'AM mass loading: {cathode.am_mass_loading:.1f} mg/cm2')
        st.info(f'Areal capacity: {cathode.areal_capacity:.1f} mAh/cm2')
        if not st.session_state.cell_format == 'Pouch':
            st.info(f'Cathode height: {cathode.height*10:.0f} mm')
            st.info(f'Cathode length: {cathode.width*10:.0f} mm')
    with anode_placeholder.container():
        st.info(f'Anode Thickness: {anode.thickness*10000:.0f} um')
        st.info(f'AM mass loading: {anode.am_mass_loading:.1f} mg/cm2')
        st.info(f'Areal capacity: {anode.areal_capacity:.1f} mAh/cm2')
        st.info(f'Anode height: {anode.height*10:.0f} mm')
        st.info(f'Anode width(length): {anode.width*10:.0f} mm')
    with calc_elec.container():
        st.info(f'Volume: {electrolyte.volume:.2f} mL')
        st.info(f'Volume per Ah: {electrolyte.volume_per_ah:.2f} mL/Ah')
    with cell_t_placeholder.container():
        if st.session_state.cell_format == 'Pouch':
            st.info(f'Cell thickness: {designed_cell.total_thickness:.1f} mm')
        else:
            designed_cell.total_thickness = None

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
        'Cathode thickness (um)',
        'Cathode porosity (%)',
        'Cathode capacity (mAh/g)',
        'Cathode voltage (V)'
    ]
    if st.session_state.cell_format == 'Pouch':
        for p in [
            'Cell size (height of cathode)',
            'Number of layers'
            ]:
            parameters.insert(0, p)
        # parameters = [
        #     'Number of layers',
        #     'Cell size (height of cathode)'    
        #     ] + parameters
    if st.session_state.cell_format == 'Cylindrical':
        for p in ['Extra mass (g)']:
            parameters.insert(0, p)
    if st.session_state.cell_format == 'Prismatic':
        for p in ['Can size (height) (mm)']:
            parameters.insert(0, p)

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

st.title('WattCell')
'---'
# ABOUT = read_file("readme.md")
# st.markdown(ABOUT)

battery = design_cell()
print_cell_metrics(battery)
with st.expander('Designed cell - all data'):
    df = pd.DataFrame([battery])
    st.dataframe(df, use_container_width=True)

'---'
energy_density_graph(battery)


