# -*- coding: utf-8 -*-
'''
Created on 27/07/2024

@author: Marcin Orzech
'''

from dataclasses import dataclass, field
from typing import Dict, Any

materials = {
    'Cu':{'density': 8.94},
    'Al':{'density': 2.7},
    'Prussian Blue': {
        'density': 1.8, # in g/cm3
        'capacity': 150, # in Ah/kg
        'voltage': 3.2 # in V
    },
    'Hard Carbon': {
        'capacity': 300,
    },
    'SuperP':{'density': 1.9},
    'PVDF':{'density': 1.78},
    'CMC+SBR':{'density': (1.6+0.96)/2}
}

@dataclass
class Electrode:
    active_material: str
    mass_ratio: Dict[str, float]
    binder: str
    porosity: float
    voltage: float
    capacity: float
    density_am: float
    width: float
    height: float
    thickness: float
    current_collector: str = 'Al'
    tab_height: float = 10
    tab_width: float = 10
    density_total: float = field(init=False)

    def __post_init__(self):
        self.calculate_density_total()

    def calculate_density_total(self):
        volumes = {
            'am': self.mass_ratio['am'] / self.density_am,
            'carbon': self.mass_ratio['carbon'] / materials['SuperP']['density'],
            'binder': self.mass_ratio['binder'] / materials[self.binder]['density']
        }
        volume_ratios = {k: v / sum(volumes.values()) for k, v in volumes.items()}
        self.density_total = (1 - self.porosity) * (
            volume_ratios['am'] * self.density_am +
            volume_ratios['carbon'] * materials['SuperP']['density'] +
            volume_ratios['binder'] * materials[self.binder]['density']
        )

@dataclass
class CurrentCollector:
    anode: str
    cathode: str
    anode_thickness: float
    cathode_thickness: float

@dataclass
class Separator:
    name: str
    width: float
    height: float
    thickness: float
    porosity: float
    density: float

@dataclass
class Pouch:
    width: float
    height: float
    thickness: float
    density: float

@dataclass
class Tab:
    material: str
    height: float
    width: float
    thickness: float
    density: float = field(init=False)

    def __post_init__(self):
        self.density = materials.get(self.material)['density']

@dataclass
class BatteryCell:
    cathode: Cathode
    anode: Anode
    current_collector: CurrentCollector
    separator: Separator
    pouch: Pouch
    tabs: Tab

    def calculate_energy_density(self):
        # Implement energy density calculation here
        pass

# Usage:
cathode = Cathode(
    active_material=cathode_am,
    mass_ratio={
        'active_material': active_material,
        'carbon': carbon,
        'binder': binder,
    },
    porosity=porosity,
    voltage=voltage,
    capacity=capacity,
    density_am=density_am,
    density_total=1.35,
    width=43,
    height=56,
    thickness=0.025,
    current_collector='Al',
    tab_height=10,
    tab_width=10
)

anode = Anode(
    active_material='none',
    current_collector='Al',
    width=cathode.width + 2,
    height=cathode.height + 2,
    thickness=0.01,
    tab_height=10,
    tab_width=10
)

# Initialize other components similarly...

battery = BatteryCell(cathode, anode, current_collector, separator, pouch, tabs)

