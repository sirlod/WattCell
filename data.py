materials = {
    'current_collectors': {
        'Al': {'density': 2.7, 'thickness': 16},  # thickness in um
        'Cu': {'density': 8.94, 'thickness': 8},  # thickness in um
    },
    'cathodes':{
        'Prussian Blue (Na)': {
            'density': 1.8,  # in g/cm3
            'capacity': 150,  # in Ah/kg
            'voltage': 3.2  # in V
        }
    },
    'anodes':{
        'Hard Carbon': {  # from KURANODE
            'capacity': 332,
            'voltage': 0.1,
            'density': 1.48
        },
        'Sodium metal':{
            'capacity': 1166,
            'voltage': 0.0,
            'density': 0.971
        }
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
    'pouch': {
        'thickness': 113,  # in um
        'density': 1.62,  # in g/cm³
        'extra_width': 0.9,  # in cm
        'extra_height': 2  # in cm
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
        }
    },
    'electrolytes': {
        'NaPF6 in diglyme': {
            'density': 1.15
        }
    }
}
