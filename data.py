materials = {
    'current_collectors': {
        'Al': {'density': 2.7, 'thickness': 16},  # thickness in um
        'Cu': {'density': 8.94, 'thickness': 8},  # thickness in um
    },
    'cathodes':{
        'Prussian White (Na-ion)': {
            'density': 2.3,  # in g/cm3; our calculations from XRD refinement
            'capacity': 160,  # in Ah/kg
            'voltage': 3.2  # in V
        },
        'LCO': {
            'density': 5.1,
            'capacity': 165,
            'voltage': 3.86
        },  # Source: https://github.com/ndrewwang/BotB/blob/main/1.%20BotB%20Theoretical%20Capacities.ipynb
        'LFP': {
            'density': 3.6,
            'capacity': 160,
            'voltage': 3.375
        },  # Source: https://github.com/ndrewwang/BotB/blob/main/1.%20BotB%20Theoretical%20Capacities.ipynb
        'LMNO': {
            'density': 4.27,
            'capacity': 130,
            'voltage': 4.7
        },  # Source: https://www.targray.com/li-ion-battery/cathode-materials/lnmo
        'LMO': {
            'density': 4.58,
            'capacity': 105,
            'voltage': 4.0
        },  # Source: https://www.neicorporation.com/products/batteries/cathode-anode-tapes/lithium-manganese-oxide/
        'NCA': {
            'density': 4.85,
            'capacity': 210,
            'voltage': 3.86
        },  # Source: https://github.com/ndrewwang/BotB/blob/main/1.%20BotB%20Theoretical%20Capacities.ipynb
        'NMC532': {
            'density': 4.7,
            'capacity': 175,
            'voltage': 3.75
        },  # Source: Harlow et al, J. Electrochem. Soc. 166 (13) A3031-A3044 (2019)
        'NMC622': {
            'density': 4.7,
            'capacity': 181,
            'voltage': 3.86
        },  # Source: https://github.com/ndrewwang/BotB/blob/main/1.%20BotB%20Theoretical%20Capacities.ipynb
        'NMC811': {
            'density': 4.7,
            'capacity': 195,
            'voltage': 3.86
        },  # Source: https://github.com/ndrewwang/BotB/blob/main/1.%20BotB%20Theoretical%20Capacities.ipynb
        'Prussian White (K-ion)': {
            'density': 1.79,
            'capacity': 111,
            'voltage': 3.6
        },  # Source: https://doi.org/10.1016/j.elecom.2017.02.012
        'Layered oxide - Faradion (Na-ion)': {
            'density': 4.2,
            'capacity': 156,
            'voltage': 3.3
        },  # Source: https://doi.org/10.1039/D1TA00376C
        'Polyanionic NVPF - Tiamat (Na-ion)': {
            'density': 3.17,
            'capacity': 127,
            'voltage': 3.8
        },  # Source: https://doi.org/10.26434/chemrxiv-2022-716b5
        'FeS2 (Na-ion)': {
            'density': 5.0,
            'capacity': 460,
            'voltage': 1.55
        },  # Source: Own data
    },
    'anodes': {
        'Hard Carbon - Kuraray (Na-ion)': {  # from KURANODE
            'capacity': 332,
            'voltage': 0.1,
            'density': 1.48
        },
        'Sodium metal': {
            'capacity': 1166,
            'voltage': 0.0,
            'density': 0.971
        },
        'Graphite (Li-ion)': {
            'capacity': 344,
            'voltage': 0.17,
            'density': 2.24
        },  # Source: https://github.com/ndrewwang/BotB/blob/main/1.%20BotB%20Theoretical%20Capacities.ipynb
        'Hard Carbon - Faradion (Na-ion)': {
            'capacity': 360,
            'voltage': 0.1,
            'density': 1.6
        },  # Source: https://doi.org/10.1039/D1TA00376C
        'Lithium metal': {
            'capacity': 3861,
            'voltage': 0.0,
            'density': 0.534
        },  # Source: https://github.com/ndrewwang/BotB/blob/main/1.%20BotB%20Theoretical%20Capacities.ipynb
        'LTO': {
            'capacity': 167,
            'voltage': 1.55,
            'density': 3.43
        },  # Source: https://github.com/ndrewwang/BotB/blob/main/1.%20BotB%20Theoretical%20Capacities.ipynb
        'Si': {
            'capacity': 2300,
            'voltage': 0.4,
            'density': 2.32
        },  # Source: https://github.com/ndrewwang/BotB/blob/main/1.%20BotB%20Theoretical%20Capacities.ipynb
        'Antimony (Sb) (Na-ion)': {
            'capacity': 650,
            'voltage': 0.6,
            'density': 6.691
        },  # Source: https://iopscience.iop.org/article/10.1149/2.080403jes
        'Potassium metal': {
            'capacity': 685,
            'voltage': 0.05,
            'density': 0.862
        },  
    },
    'SuperP': {'density': 1.9},
    'binders':{
        'PVDF': {'density': 1.78},
        'CMC+SBR': {'density': (1.6+0.96)/2},
        'CMC': {'density': 1.6},
    },
    'separators':{
        'Celgard 2325': {
            'thickness': 25,  # in um
            'porosity': 0.39,
            'density': 0.74  # in g/cm³ from https://core.ac.uk/download/pdf/288499223.pdf
        },
        'Celgard 2318': {
            'thickness': 18,  # in um
            'porosity': 0.39,
            'density': 0.74  # in g/cm³ from https://core.ac.uk/download/pdf/288499223.pdf
        },
        'Celgard 2320': {
            'thickness': 20,  # in um
            'porosity': 0.39,
            'density': 0.74  # in g/cm³ from https://core.ac.uk/download/pdf/288499223.pdf
        },
        'Celgard 2340': {
            'thickness': 39,  # in um
            'porosity': 0.44,
            'density': 0.74  # in g/cm³ from https://core.ac.uk/download/pdf/288499223.pdf
        },
        'Celgard 2400': {
            'thickness': 25,  # in um
            'porosity': 0.41,
            'density': 0.69  # in g/cm³ from https://core.ac.uk/download/pdf/288499223.pdf
        },
        'Celgard H1409': {
            'thickness': 14,  # in um
            'porosity': 0.45,
            'density': 0.74  # in g/cm³ from https://core.ac.uk/download/pdf/288499223.pdf
        },
        'Solupor 10P05A': {
            'thickness': 60,  # in um
            'porosity': 0.83,
            'density': 0.68  # in g/cm³ from https://core.ac.uk/download/pdf/288499223.pdf
        },
        'Solupor 7P03A': {
            'thickness': 50,  # in um
            'porosity': 0.85,
            'density': 0.88  # in g/cm³ from https://core.ac.uk/download/pdf/288499223.pdf
        }
    },
    'formats':{
        'pouch': {
            'thickness': 113,  # in um
            'density': 1.62,  # in g/cm³
            'extra_width': 0.9,  # in cm
            'extra_height': 2  # in cm
        },
        'cylindrical': {
            '18650': {
                'diameter': 18,  # mm
                'height': 65,  # mm
                'can_thickness': 0.2,  # mm
                'mandrel_dia': 1.5,  # mm
                'headspace': 5.0  # mm
            },
            '21700': {
                'diameter': 21, 
                'height': 70,
                'can_thickness': 0.25,  
                'mandrel_dia': 2.0,
                'headspace': 5.0  
            },
            '4680': {  # https://iopscience.iop.org/article/10.1149/1945-7111/ad14d0
                'diameter': 46,
                'height': 80,
                'can_thickness': 0.5,
                'mandrel_dia': 5.0,
                'headspace': 8.0
            }
        }
    },
    'tabs': {
        'Al': {
            'density': 2.7
        },
        'Ni': {
            'density': 8.9
        },
        'Cu': {
            'density': 8.94
        },
        'None': {
            'density': 0.0
        }
    },
    'electrolytes': {
        '1M NaPF6 in diglyme': {
            'density': 1.15  # measured in lab
        },
        '1M NaPF6 in EC:DEC': {
        'density': 1.19  # calculated
        },
        '1.1M LiPF6 in EC:EMC': {
        'density': 1.2  # https://github.com/ndrewwang/BotB/blob/main/3.%20BotB%20The%20Cell%20Stack.ipynb
        },
    },
    'can_density':{
        'Stainless steel': 7.98,
        'Aluminium': 2.7
    }
}
