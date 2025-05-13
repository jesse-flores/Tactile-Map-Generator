# Tactile Map Generator

This project generates **3D tactile maps** from real-world geographic data using OpenStreetMap. It converts urban layouts into simplified 3D models (in STL format), including buildings and walkable paths - ready for **3D printing**. The output can be used for **assistive navigation**, **education**, **urban planning**, and more.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Applications](#applications)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Example](#example)  
- [License](#license)  

---

## Overview

The **Tactile Map Generator** is a Python script that retrieves geographic data for any location using OSM (OpenStreetMap), processes the building footprints and pedestrian paths, and generates a printable 3D model. The goal is to translate 2D geospatial information into a **tangible experience** — useful for **visually impaired users**, **educators**, **designers**, and **makers**.

Using libraries like `osmnx`, `shapely`, and `trimesh`, the script handles:
- Geometry cleanup and simplification  
- Automatic projection and scaling  
- 3D extrusion of buildings and paths  
- Export to a `.stl` file for printing

---

## Features

- Convert any city, town, or region into a tactile 3D model  
- Automatically includes buildings and walkable paths  
- Built-in geometry validation and simplification  
- Exports to STL format — ready for slicing/3D printing  
- Fallback geometry in case of missing data  
- Command-line interface with flexible output options

---

## Applications

This tool has a variety of real-world applications:

- **Accessibility**: Tactile city maps for visually impaired users  
- **Education**: Teaching geography, city planning, or 3D modeling  
- **Urban Design**: Physical mockups of neighborhood plans  
- **Architecture**: Presenting simplified site contexts  
- **Makerspaces**: Engaging STEM/STEAM projects for all ages  
- **Exhibits**: Museum and outreach tools to explain spatial data  

---

## Requirements

Install the necessary dependencies:

```bash
pip install osmnx shapely trimesh numpy geopandas
```
Recommended: Use a virtual environment


---

## Installation

1. Clone the repository
```bash
git clone https://github.com/jesse-flores/tactile-map-generator.git
```

2. Install the necessary dependencies:
```bash
cd tactile-map-generator
```

3. Install dependencies
```bash
pip install osmnx shapely trimesh numpy geopandas
```

---

## Usage
To generate a 3D tactile map for a specific place, run the script with a place name:
```bash
python tactile_map_generator.py "Chicago, IL"
```

You can also specify a custon output file:
```bash
python tactile_map_generator.py "New York City, NY" --output NYC.stl
```

### This script will:
- Fetch OSM data for the place
- Process building and walkway geometries
- Generate a 3D mesh (extruded buildings and paths)
- Save the result as an STL file


---

## Example

Here’s how to generate a 3D model of San Francisco:
```bash
python tactile_map_generator.py "Tufts University, MA" --output University_Map.stl
```
### Example output:

```console
PS C:\Tactile_Map_Generator> python tactile_map_generator.py "Tufts University, MA" --output University_Map.stl

==================================================
TACTILE MAP GENERATOR - Tufts University, MA
==================================================

FETCHING DATA FOR: Tufts University, MA

Fetching buildings...

Fetching walkways...

PROCESSING GEOMETRIES
Found 2700 valid paths

GENERATING 3D MODEL
Creating building mesh...

SAVED: University_Map.stl

SUCCESS: Map generated
PS C:\Tactile_Map_Generator> 
```

Generated STL File in 3d Viewer (Blender):
![image](https://github.com/user-attachments/assets/1e8aa674-b2f9-426a-9ef2-ca6aa7eab946)

|    Generated Map     | Google Maps Location |
| -------------------- | --------------------- |
| ![image](https://github.com/user-attachments/assets/83787c41-2754-4663-8a0c-eb17bacf2a1f) | ![image](https://github.com/user-attachments/assets/f939159f-11ea-4d9f-a8ea-00b081c15d9b) |



## License

This project is licensed under the MIT License.
