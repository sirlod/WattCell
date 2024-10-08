# -*- coding: utf-8 -*-
'''
Created on 27/07/2024

@authors: Marcin Orzech, Ashley Willow

This code defines classes of all battery components and the cell itself.
It also has methods to perform all calculations
'''

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Any, Union
from data import materials


@dataclass
class Electrode:
    active_material: str
    mass_ratio: Dict[str, float]
    binder: str
    porosity: float
    voltage: float  # V
    capacity: float  # Ah/kg
    density_am: float  # g/cm3
    width: float  # cm
    cc_thickness: float  # cm
    current_collector: str
    height: float = 0 # cm
    thickness: float = 0  # cm
    tab_height: float = 1  # cm
    tab_width: float = 1  # cm
    density: float = field(init=False)
    am_mass_loading: float = field(init=False)  # mg/cm2
    areal_capacity: float = field(init=False)  # mAh/cm²

    def __post_init__(self):
        self.calculate_composite_density()
        self.calculate_areal_capacity()
        self.calculate_am_mass_loading()

    def calculate_composite_density(self):
        volumes = {
            'am': self.mass_ratio['am'] / self.density_am,
            'carbon': self.mass_ratio['carbon'] / materials['SuperP']['density'],
            'binder': self.mass_ratio['binder']
            / materials['binders'][self.binder]['density'],
        }
        volume_ratios = {k: v / sum(volumes.values()) for k, v in volumes.items()}
        self.density = (1 - self.porosity) * (
            volume_ratios['am'] * self.density_am
            + volume_ratios['carbon'] * materials['SuperP']['density']
            + volume_ratios['binder'] * materials['binders'][self.binder]['density']
        )

    def calculate_areal_capacity(self):
        self.areal_capacity = (
            self.density * self.thickness * self.capacity * self.mass_ratio['am']
        )

    def calculate_am_mass_loading(self):
        self.am_mass_loading = (
            self.density * self.thickness * self.mass_ratio['am'] * 1000
        )


@dataclass
class Separator:
    material: str
    width: float  # cm
    thickness: float  # cm
    porosity: float
    density: float
    height: float = 0 # cm

@dataclass
class Electrolyte:
    material: str
    density: float
    volume_excess: float = 0
    volume: float = field(init=False)
    volume_per_ah: float = field(init=False)


@dataclass
class Pouch:
    width: float  # cm
    height: float  # cm
    thickness: float  # cm
    density: float


@dataclass
class Cylindrical:
    diameter: float  # cm
    height: float  # cm
    can_thickness: float  # cm
    can_density: float  # g/cm³
    mandrel_diam: float = 0.2  # cm
    headspace: float = 0.5 # cm


@dataclass
class Prismatic:
    structure: str
    width: float  # cm
    height: float  # cm
    depth: float  # cm
    can_thickness: float  # cm
    can_density: float  # g/cm³
    headspace: float  # cm


@dataclass
class Tab:
    material_cathode: str = 'None'
    material_anode: str = 'None'
    height: float = None # cm
    width: float = None  # cm
    thickness: float = None # cm
    density_cathode: float = field(init=False)
    density_anode: float = field(init=False)

    def __post_init__(self):
        self.density_cathode = materials['tabs'].get(self.material_cathode)['density']
        self.density_anode = materials['tabs'].get(self.material_anode)['density']


@dataclass
class Cell:
    cathode: Electrode
    anode: Electrode
    separator: Separator
    electrolyte: Electrolyte
    format: Union[Pouch, Cylindrical, Prismatic]
    tabs: Tab
    layers_number: int = 30
    n_p_ratio: float = 1.1
    ice: float = 0.93
    extra_mass: float = 4

    # attributes to store calculation results
    volumetric_energy_density: float = field(init=False)
    gravimetric_energy_density: float = field(init=False)
    energy: float = field(init=False)
    capacity: float = field(init=False)
    total_mass: float = field(init=False)
    total_volume: float = field(init=False)
    total_thickness: float = field(init=False)

    def __post_init__(self):
        self.calculate_anode_properties()
        self.calculate_energy_density()

    def calculate_anode_properties(self):
        required_anode_capacity = self.cathode.areal_capacity * self.n_p_ratio

        # Calculate required anode thickness
        self.anode.thickness = required_anode_capacity / (
            self.anode.density * self.anode.capacity * self.anode.mass_ratio['am']
        )

        # Recalculate anode areal capacity and mass loading
        self.anode.calculate_areal_capacity()
        self.anode.calculate_am_mass_loading()

    def calculate_energy_density(self):
        '''
        calculation of final values inputs
        results:
        total mass
        total volume
        capacity
        energy
        specific energy
        energy density
        '''
        if isinstance(self.format, Pouch):
            self.calculate_pouch_energy()
        elif isinstance(self.format, Cylindrical):
            self.calculate_cylindrical_energy()
        elif isinstance(self.format, Prismatic):
            self.calculate_prismatic_energy()

        # Calculate volume of electrolyte per Ah
        self.electrolyte.volume_per_ah = (
            self.electrolyte.volume / self.capacity
        )  # cm³/Ah

        # Calculate energy
        cell_voltage = self.cathode.voltage - self.anode.voltage
        self.energy = self.capacity * cell_voltage  # in Wh

        # Calculate energy density and specific energy
        self.volumetric_energy_density = self.energy / self.total_volume * 1000  # Wh/L
        self.gravimetric_energy_density = self.energy / self.total_mass * 1000  # Wh/kg


    def calculate_pouch_energy(self):
        # Calculate volumes of individual item (cm3)
        cathode_volume = (
            self.cathode.width
            * self.cathode.height
            * self.cathode.thickness
            * 2
            * self.layers_number
        )
        anode_volume = (
            self.anode.width
            * self.anode.height
            * self.anode.thickness
            * 2
            * (self.layers_number + 1)  # Extra anode layer
        )
        separator_volume = (
            self.separator.width
            * self.separator.height
            * self.separator.thickness
            * 2
            * self.layers_number
        )
        pouch_volume = (
            self.format.width * self.format.height * self.format.thickness * 2
        )
        anode_cc_volume = (
            (self.layers_number + 1)  # Extra anode current collector
            * (
                self.anode.width * self.anode.height
                + (self.anode.tab_height * self.anode.tab_width)
            )
            * self.anode.cc_thickness
        )
        cathode_cc_volume = (
            self.layers_number
            * (
                self.cathode.width * self.cathode.height
                + self.cathode.tab_height * self.cathode.tab_width
            )
            * self.cathode.cc_thickness
        )

        # Calculate masses (g)
        cathode_mass = cathode_volume * self.cathode.density
        anode_mass = anode_volume * self.anode.density
        separator_mass = separator_volume * self.separator.density
        pouch_mass = pouch_volume * self.format.density
        cathode_cc_mass = (
            cathode_cc_volume
            * materials['current_collectors'][self.cathode.current_collector]['density']
        )
        anode_cc_mass = (
            anode_cc_volume
            * materials['current_collectors'][self.anode.current_collector]['density']
        )
        tabs_mass = (
            self.tabs.height
            * self.tabs.width
            * self.tabs.thickness
            * (self.tabs.density_cathode + self.tabs.density_anode)
        )

        # Calculate void volume for electrolyte
        cathode_void_volume = cathode_volume * self.cathode.porosity
        anode_void_volume = anode_volume * self.anode.porosity
        separator_void_volume = separator_volume * self.separator.porosity
        total_void_volume = (
            cathode_void_volume + anode_void_volume + separator_void_volume
        )

        # Calculate electrolyte mass and volume
        self.electrolyte.volume = total_void_volume * (
            1 + self.electrolyte.volume_excess
        )
        electrolyte_mass = self.electrolyte.volume * self.electrolyte.density

        # Calculate total mass, volume and thickness
        self.total_mass = (
            cathode_mass
            + cathode_cc_mass
            + anode_mass
            + anode_cc_mass
            + separator_mass
            + pouch_mass
            + tabs_mass
            + electrolyte_mass
            + self.extra_mass
        )
        self.total_volume = (
            cathode_volume
            + anode_volume
            + separator_volume
            + pouch_volume
            + (self.electrolyte.volume - total_void_volume)
            + anode_cc_volume
            + cathode_cc_volume
        )
        self.total_thickness = 10 * (
            2 * self.cathode.thickness
            + self.cathode.cc_thickness
            + 2 * self.anode.thickness
            + self.anode.cc_thickness
            + 2 * self.separator.thickness
        ) * self.layers_number

        # Calculate capacity (based on the limiting electrode)
        cathode_capacity = (
            cathode_mass * self.cathode.mass_ratio['am'] * self.cathode.capacity / 1000
        )  # Convert to Ah
        anode_capacity = (
            anode_mass * self.anode.mass_ratio['am'] * self.anode.capacity / 1000
        )  # Convert to Ah
        self.capacity = min(cathode_capacity, anode_capacity) * self.ice


    def calculate_cylindrical_energy(self):
        # Calculate stack thickness
        stack_thickness = (
            2 * self.cathode.thickness
            + self.cathode.cc_thickness
            + 2 * self.anode.thickness
            + self.anode.cc_thickness
            + 2 * self.separator.thickness
        )

        # Calculate jelly roll length
        d_cell = self.format.diameter - 2 * self.format.can_thickness

        a = stack_thickness / (2 * np.pi)
        theta = (d_cell / 2) * (2 * np.pi) / stack_thickness
        total_length = (a / 2) * (
            theta * (1 + theta**2) ** 0.5 + np.log(theta + (1 + theta**2) ** 0.5)
        )

        theta_mandrel = (self.format.mandrel_diam / 2) * (2 * np.pi) / stack_thickness
        length_inner_void = (a / 2) * (
            theta_mandrel * (1 + theta_mandrel**2) ** 0.5
            + np.log(theta_mandrel + (1 + theta_mandrel**2) ** 0.5)
        )

        length_jellyroll = total_length - length_inner_void

        # Calculate length (width) of each component
        self.cathode.width = length_jellyroll - 2 * self.format.diameter * np.pi # 2 turns less than separator
        self.anode.width = length_jellyroll - self.format.diameter * np.pi  # 1 turn less than separator
        self.separator.width = length_jellyroll

        # Calculate height of components
        self.cathode.height = self.format.height - self.format.headspace - 2 * self.format.can_thickness
        self.anode.height = self.cathode.height + 0.2
        self.separator.height = self.anode.height + 0.2

        # Calculate volumes
        cathode_volume = self.cathode.width * self.cathode.height * self.cathode.thickness * 2
        anode_volume = self.anode.width * self.anode.height * self.anode.thickness * 2
        separator_volume = self.separator.width * self.separator.height * self.separator.thickness * 2
        cathode_cc_volume = self.cathode.width * self.cathode.height * self.cathode.cc_thickness
        anode_cc_volume = self.anode.width * self.anode.height * self.anode.cc_thickness
        can_volume = (
            np.pi
            * (
                (self.format.diameter / 2) ** 2
                - ((self.format.diameter / 2) - self.format.can_thickness) ** 2
            )
            * self.format.height
        )

        # Calculate masses
        cathode_mass = cathode_volume * self.cathode.density
        anode_mass = anode_volume * self.anode.density
        separator_mass = separator_volume * self.separator.density
        can_mass = can_volume * self.format.can_density
        cathode_cc_mass = (
            cathode_cc_volume
            * materials['current_collectors'][self.cathode.current_collector]['density']
        )
        anode_cc_mass = (
            anode_cc_volume
            * materials['current_collectors'][self.anode.current_collector]['density']
        )

        # Calculate void volume for electrolyte
        cathode_void_volume = cathode_volume * self.cathode.porosity
        anode_void_volume = anode_volume * self.anode.porosity
        separator_void_volume = separator_volume * self.separator.porosity
        total_void_volume = (
            cathode_void_volume + anode_void_volume + separator_void_volume
        )

        # Calculate electrolyte mass and volume
        self.electrolyte.volume = total_void_volume * (
            1 + self.electrolyte.volume_excess
        )
        electrolyte_mass = self.electrolyte.volume * self.electrolyte.density

        # Calculate total mass and volume
        self.total_mass = (
            cathode_mass
            + cathode_cc_mass
            + anode_mass
            + anode_cc_mass
            + separator_mass
            + can_mass
            + electrolyte_mass
            + self.extra_mass
        )
        self.total_volume = np.pi * (self.format.diameter / 2) ** 2 * self.format.height

        # Calculate capacity
        cathode_capacity = (
            cathode_mass * self.cathode.mass_ratio["am"] * self.cathode.capacity / 1000
        )
        anode_capacity = (
            anode_mass * self.anode.mass_ratio["am"] * self.anode.capacity / 1000
        )
        self.capacity = min(cathode_capacity, anode_capacity) * self.ice


    def calculate_prismatic_energy(self):
        # Calculate stack thickness
        stack_thickness = (
            2 * self.cathode.thickness
            + self.cathode.cc_thickness
            + 2 * self.anode.thickness
            + self.anode.cc_thickness
            + 2 * self.separator.thickness
        )

        # only matters for wound
        # Calculate jelly roll dimensions
        d = min(self.format.width, self.format.depth)
        d_jellyroll = d - 2 * self.format.can_thickness - 2 * self.separator.thickness 

        # Calculate number of turns
        a = stack_thickness / (2 * np.pi)
        theta = (d_jellyroll / 2) * (2 * np.pi) / stack_thickness
        length_jellyroll = (a / 2) * (
            theta * (1 + theta**2) ** 0.5 + np.log(theta + (1 + theta**2) ** 0.5)
        )

        # Calculate number of layers
        available_depth = self.format.depth - 2 * self.format.can_thickness - 4 * self.separator.thickness - self.anode.thickness - self.anode.cc_thickness
        self.layers_number = int(available_depth / stack_thickness)

        # Calculate electrode and separator dimensions
        if self.format.structure == 'Wound':
            flat_width = self.format.width - d_jellyroll - 2 * self.format.can_thickness
            self.separator.width = length_jellyroll + (self.layers_number + 1) * flat_width
            self.cathode.width = length_jellyroll + self.layers_number * flat_width - 2 * d_jellyroll * np.pi   # 2 turns less than separator
            self.anode.width = length_jellyroll + (self.layers_number + 1) * flat_width - d_jellyroll * np.pi  # 1 turn less than separator
            self.layers_number = 1  # reset layers nr
        else:
            self.cathode.width = self.format.width - 2 * self.format.can_thickness - 0.4
            self.anode.width = self.cathode.width + 0.2
            self.separator.width = self.cathode.width + 0.4

        self.cathode.height = self.format.height - 2 * self.format.can_thickness - self.format.headspace - 0.4
        self.anode.height = self.format.height - 2 * self.format.can_thickness - self.format.headspace - 0.2
        self.separator.height = self.format.height - 2 * self.format.can_thickness - self.format.headspace

        # Calculate volumes of individual items (cm3)
        cathode_volume = (
            self.cathode.width
            * self.cathode.height
            * self.cathode.thickness
            * 2
            * self.layers_number
        )
        if self.format.structure == 'Wound':
            anode_volume = (
                self.anode.width
                * self.anode.height
                * self.anode.thickness
                * 2
            )
        else:
            anode_volume = (
                self.anode.width
                * self.anode.height
                * self.anode.thickness
                * 2
                * (self.layers_number + 1)  # Extra anode layer
            )
        separator_volume = (
            self.separator.width
            * self.separator.height
            * self.separator.thickness
            * 2
            * self.layers_number
        )
        can_volume = (
            self.format.width * self.format.height * self.format.depth
            - ((self.format.width - 2 * self.format.can_thickness)
            * (self.format.height - 2 * self.format.can_thickness)
            * (self.format.depth - 2 * self.format.can_thickness))
        )
        if self.format.structure == 'Wound':
            anode_cc_volume = (
                self.anode.width
                * self.anode.height
                * self.anode.cc_thickness
            )
        else:
            anode_cc_volume = (
                (self.layers_number + 1)  # Extra anode current collector
                * (self.anode.width * self.anode.height)
                * self.anode.cc_thickness
            )
        cathode_cc_volume = (
            self.layers_number
            * (self.cathode.width * self.cathode.height)
            * self.cathode.cc_thickness
        )

        # Calculate masses (g)
        cathode_mass = cathode_volume * self.cathode.density
        anode_mass = anode_volume * self.anode.density
        separator_mass = separator_volume * self.separator.density
        can_mass = can_volume * self.format.can_density
        cathode_cc_mass = (
            cathode_cc_volume
            * materials['current_collectors'][self.cathode.current_collector]['density']
        )
        anode_cc_mass = (
            anode_cc_volume
            * materials['current_collectors'][self.anode.current_collector]['density']
        )
        tabs_mass = (
            self.tabs.height
            * self.tabs.width
            * self.tabs.thickness
            * (self.tabs.density_cathode + self.tabs.density_anode)
        )

        # Calculate void volume for electrolyte
        cathode_void_volume = cathode_volume * self.cathode.porosity
        anode_void_volume = anode_volume * self.anode.porosity
        separator_void_volume = separator_volume * self.separator.porosity
        total_void_volume = (
            cathode_void_volume + anode_void_volume + separator_void_volume
        )

        # Calculate electrolyte mass and volume
        self.electrolyte.volume = total_void_volume * (
            1 + self.electrolyte.volume_excess
        )
        electrolyte_mass = self.electrolyte.volume * self.electrolyte.density

        # Calculate total mass and volume
        self.total_mass = (
            cathode_mass
            + cathode_cc_mass
            + anode_mass
            + anode_cc_mass
            + separator_mass
            + can_mass
            + tabs_mass
            + electrolyte_mass
            + self.extra_mass
        )
        self.total_volume = self.format.width * self.format.height * self.format.depth

        # Calculate capacity (based on the limiting electrode)
        cathode_capacity = (
            cathode_mass * self.cathode.mass_ratio['am'] * self.cathode.capacity / 1000
        )  # Convert to Ah
        anode_capacity = (
            anode_mass * self.anode.mass_ratio['am'] * self.anode.capacity / 1000
        )  # Convert to Ah
        self.capacity = min(cathode_capacity, anode_capacity) * self.ice


    def anode_free_energy(self):
        if isinstance(self.format, Pouch):
            anode_volume = (
            self.anode.width
            * self.anode.height
            * self.anode.thickness
            * 2
            * (self.layers_number + 1)
            )
        elif isinstance(self.format, Cylindrical):
            anode_volume = (
            self.anode.width
            * self.anode.height
            * self.anode.thickness
            )
        elif isinstance(self.format, Prismatic):
            if self.format.structure == 'Wound':
                anode_volume = (
                self.anode.width
                * self.anode.height
                * self.anode.thickness
                * 2
                )
            else:
                anode_volume = (
                self.anode.width
                * self.anode.height
                * self.anode.thickness
                * 2
                * (self.layers_number + 1)
                )

        anode_mass = anode_volume * self.anode.density
        self.total_mass = self.total_mass - anode_mass
        self.gravimetric_energy_density = self.energy / self.total_mass * 1000  # Wh/kg
