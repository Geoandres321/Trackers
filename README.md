# Solar Tracker Optimization 🖥

## Introduction 🚀

This repository contains a Python script that performs solar tracker optimization for a photovoltaic (PV) system. The main goal of this project is to find optimal tracker angles that minimize shadowing and maximize solar exposure, thus enhancing the overall efficiency of the PV system.

## Installation 🖥

To run the script, follow these steps:
1. Clone this repository to your local machine.
2. Activate the virtualenv 
3. Install the required dependencies using the following command:

```bash
pip install virtualenv
virtualenv env -p python 3.9
pip install -r requirements.txt
python app.py
```

## Architecture 📦
The script is designed to calculate solar angles, optimize tracker angles, and visualize the results. It leverages the pvlib library for solar position calculations and scipy for optimization.

<div align="center">
       <img src="images/arquitecture.png?raw=true" width="200px"</img> 
</div>

## Project Layout 🛠️
The repository is organized as follows:

```bash
.
├── app.py #The main Python script for solar tracker optimization.
├── requirements.txt #List of required Python packages.
├── README.md #List of required Python packages.
├── images # Images project
```

## Results 📖
The script generates optimized tracker angles over a specified time range and visualizes them alongside solar angles. This visualization provides insights into the performance of the optimized tracker angles.

<div align="center">
       <img src="images/Diagrama.png?raw=true" width="800px"</img> 
</div>

## Built With 📌
pvlib - A library for solar energy modeling.
scipy - A scientific library for optimization.
pandas
numpy

## Version📄
This is version 1.0 of the Solar Tracker Optimization script.

## Author🎁
* **Geovanni Vera** - [Geoandres321](https://github.com/Geoandres321)

## Acknowledgements 📢
* Thanks to the gamechangesolar team🤓.
