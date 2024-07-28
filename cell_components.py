# -*- coding: utf-8 -*-
'''
Created on 27/07/2024

@author: Marcin Orzech
'''

from dataclasses import dataclass, field
from typing import Dict, Any

materials = {
    'Cu': {'density': 8.94, 'thickness': 6},  # thickness in um
    'Al': {'density': 2.7, 'thickness': 16},  # thickness in um
    'Prussian Blue': {
        'density': 1.8,  # in g/cm3
        'capacity': 150,  # in Ah/kg
        'voltage': 3.2  # in V
    },
    'Hard Carbon': {
        'capacity': 300,
        'voltage': 0.1,
        'density': 1.6
    },
    'SuperP': {'density': 1.9},
    'PVDF': {'density': 1.78},
    'CMC+SBR': {'density': (1.6+0.96)/2},
    'Celgard 2325': {
        'thickness': 25,  # in um
        'porosity': 0.41,
        'density': 0.74  # in g/cm³ from https://core.ac.uk/download/pdf/288499223.pdf
    },
    'pouch': {
        'thickness': 113,  # in um
        'density': 1.62,  # in g/cm³
        'extra_width': 9,  # in mm
        'extra_height': 20  # in mm
    },
    'tabs': {
        'Al': {
            'thickness': 0.2,  # in mm
            'density': 2.7
        }
    },
    'electrolytes': {
        'NaPF6 in diglyme': {
            'density': 1.15
        }
    }
}

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
    height: float  # cm
    thickness: float  # cm
    cc_thickness: float  # cm
    current_collector: str
    tab_height: float = 1  # cm
    tab_width: float = 1  # cm
    density: float = field(init=False)

    def __post_init__(self):
        self.calculate_composite_density()

    def calculate_composite_density(self):
        volumes = {
            'am': self.mass_ratio['am'] / self.density_am,
            'carbon': self.mass_ratio['carbon'] / materials['SuperP']['density'],
            'binder': self.mass_ratio['binder'] / materials[self.binder]['density']
        }
        volume_ratios = {k: v / sum(volumes.values()) for k, v in volumes.items()}
        self.density = (1 - self.porosity) * (
            volume_ratios['am'] * self.density_am +
            volume_ratios['carbon'] * materials['SuperP']['density'] +
            volume_ratios['binder'] * materials[self.binder]['density']
        )

@dataclass
class Separator:
    material: str
    width: float
    height: float
    thickness: float
    porosity: float
    density: float

@dataclass
class Electrolyte:
    material: str
    density: float
@dataclass
class Pouch:
    width: float
    height: float
    thickness: float # cm
    density: float

@dataclass
class Tab:
    material: str
    height: float
    width: float
    thickness: float # cm
    density: float = field(init=False)

    def __post_init__(self):
        self.density = materials.get(self.material)['density']

@dataclass
class Cell:
    cathode: Electrode
    anode: Electrode
    separator: Separator
    electrolyte: Electrolyte
    format: Pouch
    tabs: Tab

    def calculate_energy_density(self):
        # Implement energy density calculation here
        pass

