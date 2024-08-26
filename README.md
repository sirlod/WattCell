
### WattCell is an application designed to quickly estimate critical parameters of battery cell performance based on user inputs. The app provides a user-friendly interface for designing and analyzing battery cells, with a focus on energy density calculations.

## Features

- Interactive input selection for cathode, anode, separator, electrolyte, and cell configuration
- Real-time calculation of cell performance metrics
- Energy density graph generation for various parameters
- Support for anode-free cell configurations
- Downloadable data in CSV format

## Disclaimer

The calculations provided by this app are reasonable estimates but do not take into account all details and factors, especially those related to power, cycle life, or manufacturing. There are limited constraints on some values, and users should always consider whether the inputs are realistic for their specific use case.

## App Structure

- `app.py` : Main application file containing the Streamlit interface and logic
- `cell_components.py`: Contains classes for various cell components (Electrode, Separator, Electrolyte, etc.)
- `graphs.py`: Functions for generating and plotting energy density data
- `materials.py`: Dictionary of material properties 


## Contributors

- Marcin Orzech
- Ashley Willow

