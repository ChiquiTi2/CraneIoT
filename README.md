# CraneIoT Simulator

The Crane IoT Simulator can be used to test IoT Gateway solutions that connect to Crane systems onboard ships (or similar systems). 
It represents a fairly minimal system for rapid testing.

It supports two main functionalities:
* send a NMEA Rate of Turn sentence with a simulated measurement value
* host & update a Modbus TCP server where simulated temperature measurements are written to holding register

## NMEA details

Different to the original NMEA 0183 standard, the sentences for the simulation are beign send via Websockets on the localhost. The default port is `8888`. 

## Modbus details

By default, 4 temperature measurements in a range of 1 - 100°C are being simulated and written to the first 4 holding registers (i.e. registers id 0 - 3). 
The standard Modbus port has been modified to `8889` to avoid potential incompatibilities on some systems. 

## Dependencies

To ensure compatiblity with the required dependencies, a requirements.txt has been added to the project. Use pip to install the dependencies:
```
  pip install -r requirements.txt
```

## Script usage

The simulation script can be executed from the terminal:
```
  python crane_simulation.py
```

The script will continue to run till it gets interrupted by a keyboard interrupt. 
