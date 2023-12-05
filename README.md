# avionics_fenix
Control and data processing system created by the Fênix UFMG 2023/24 trainee avionics team.

# Install avionics-dependencies
```
git clone git@github.com:felipefalconn/avionics_fenix.git
```
```
cd avionics_fenix
```
```
pip install -r requirements.txt
```



## Graph plotting
![Graphs of speed, acceleration and height, by time.](https://imgur.com/bGYhpJI)

```
cd avionics_fenix/2Dplot
```
```
python3 main-2d-plot.py
```

## Real-time attitude simulation
![Attitude simulation of an IMU, in real time.](https://i.imgur.com/IDNQEMN.png)

- Connect your Inertial Measurement Unit
```
cd avionics_fenix/Gait-Tracking-With-x-IMU-Python-master
```
```
python3 script.py
```
