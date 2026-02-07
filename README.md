# Ajay-Singh
Machine Learning (ML)-Drived Optimization Platform for Multistep Synthesis of Anticancer Pyrazolopyrimidines

mp1.py represents the code for the synthesis of compound 3.

mp2.py represents the code for the synthesis of compound 5.

mp3.py represents the code for the synthesis of compound 7.

mp4.py represents the code for the synthesis of compound 9.

mp5.py represents the code for the synthesis of compound 11a.

mp6.py represents the code for the synthesis of compound 12.

mp7.py represents the code for the synthesis of compound 14.

Enviorment setup for python
To install all the required dependencies for running the Python program, first create and activate a virtual environment, then install the packages using the command below

python -m venv flowopt-env
flowopt-env\Scripts\activate
pip install -r requirements.txt
Hardware & System Connections
Device	Port	Baud Rate	Function
HPLC Pump1	COM5	9600	Flowrate control
HPLC Pump2	COM29	9600	Flowrate control
Syringe Pump1	COM16	9600	Flowrate control
Syringe Pump2	COM18	9600	Flowrate control
Temperature Controller	COM19	9600	Heating and monitoring
Arduino Pressure Controller	COM50	9600	Pressure regulation
3D Printer Collector	COM46	115200	Fraction collector
Ensure all COM ports are correctly assigned before running the code.

You can check available ports in device manager.

HPLC bought from KNAUER, Syringe pump, temperature and pressure controller has been bought from smart chem synthesis.

Data Acquisition
Export FTIR spectral data to CSV format from ReactIR 15.

Update the path in the Python script:

mypath = r"C:\\Users\\Admin\\Desktop\\Ibrutinib automation\\Exp 2024-07-15 12-16"

Ensure all instrument COM ports are correctly mapped.

Run the script (mp1.py, mp2.py, mp3.py, mp4.py, mp5.py, mp6.py or mp7.py) to start the closed-loop Bayesian optimization.

The script:
Runs the HPLC pump and sets the temperature and pressure.

Monitors FTIR signals continuously.

Integrates the area under the product-specific IR peak using:

scipy.integrate.trapz

Uses this value as the objective function for Bayesian optimization.

Saves each experiment’s conditions and corresponding IR area to CSV:

output round <i>.csv

Model and Optimization
Algorithm: Bayesian Optimization using Gaussian Process (GP) surrogate

Kernel: Squared Exponential (RBF) with Automatic Relevance Determination

Acquisition Function: Expected Improvement (EI)

Implementation: skopt.Optimizer

Search bounds:
Flowrate: 0.020–2.0 mL·min⁻¹

Temperature: 25–150 °C 

Pressure: 2–40 bar

n_initial_points = 3 (Latin hypercube sampling)

Maximum iterations = 22
