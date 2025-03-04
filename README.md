# Kirdy

Low Noise Precision Laser Diode Driver with Built-in TEC Temperature Controller  

## Power Input
| Parameter | Min | Typical | Max | Unit | Condition |
| --- | --- | --- | --- | --- | ---|
| Input Voltage | | 12 | | V | |
| Input Current | | | 2 | A|
| PoE Standard | |  PoE+ (802.11at) | | |

Note: TEC Output Current should be limited to ±2A when it is being powered via PoE(802.11af). Otherwise, Kirdy may malfunction.

## Laser Diode Driver
### Current Source Controller  
| Parameter | Min | Typical | Max | Unit | Condition |
| --- | --- | --- | --- | --- | ---| 
| Resolution | | 0.292 | | uA |
| Control Range| | | 307.2 | mA | |
| Current Limit | | 319. | | mA| |
| Compliance voltage | | > 4.928 | | V | |   
| Current Noise (@ 1 kHz) | | < 300 || pA / rt(Hz) | @ DC Bias: 300 mA, Load: 10 Ω Load|
| RMS Noise(10 Hz - 1 MHz) || < 300 | | nA | @ DC Bias: 300 mA, Load: 10 Ω Load| 
| Temperature Coefficient | | ±1 | | ppm/°C | @ DC Bias: 50 mA. Tested Temperature Range: 43-56 °C |


### Photodiode Input
| Parameter | Min | Typical | Max | Unit | Condition |
| --- | --- | --- | --- | --- | ---|
| Photocurrent Range | 0 | | 3.0 | mA | |
| Photocurrent Resolution | | 0.8 | | uA | |
| Bandwidth (-3 dB) | | 500 | | Hz | |

Note1: Circuit may be damaged if photodiode input current exceeds 3.0 mA. User can modify the circuit and reprogram the photodiode current monitor range via the given driver.

Note2: Photodiode operates in photovoaic mode.

### Low Frequency Modulation Input
| Parameter | Min | Typical | Max | Unit | Condition |
| --- | --- | --- | --- | --- | ---|
| Input Voltage | -1.0 | | 1.0 | V | |
| Input Impedance | | 50 or 43.4k | | ohm | Depends on Termination Switch Position |
| Bandwidth (-3 dB) | | 18 | | MHz | @Modulation Depth: 25 mA/V, Input : 1 Vp-p, DC Bias: 150 mA |

Note: Low Frequency Modulation Input can accept DC input to impose a DC offset to the output current.

## TEC Temperature Controller
### TEC Current Output
| Parameter | Min | Typical | Max | Unit | Condition |
| --- | --- | --- | --- | --- | ---|
| Resolution | | 22.9 | | uA | |
| Control Range (Powered via 12 V Barrel Jack) | -3.0 | | 3.0 | A | With Active Cooling |
| Control Range (Powered via PoE(802.11af)) | -2.0 | | 2.0 | A | |
| Compliance Voltage | | 4.3 |  | V | |
| Voltage Reading Resolution | | 3.22 | | mV | |
| Current Reading Resolution | |  2.0 | | mA | |


### TEC Voltage and Current Limit
| Parameter | Min | Typical | Max | Unit | Condition |
| --- | --- | --- | --- | --- | ---|
| Voltage Limit Settable Range| 0 | | 4.3 | V | |
| Voltage Limit Resolution | | 3.14 | | mV | |
| Current Limit Settable Range | -3.0 | | 3.0 | A | |
| Current Limit Resolution | |  1.57 | | mA | |

### NTC Thermistor Sensor
| Parameter | Min | Typical | Max | Unit | Condition |
| --- | --- | --- | --- | --- | ---|
| Resolution | | 0.01 | | mK | With 10 kohm NTC with 3950 B-Constant, 25°C T0 |
| Sampling Rate | | 16.67 | > 1k | Hz | |

Note: Actual Sampling Rate subjects to device operating conditions.

### Digital PID Temperature Controller
| Parameter | Min | Typical | Max | Unit | Condition |
| --- | --- | --- | --- | --- | ---|
| Temperature Stability | | < 1| | mk | Using supplied Kirdy Adapter with its copper plate installed. PID Parameters are obtained from Kirdy Autotune Algorithm. |

Note: Actual Temperature Stability subjects to the ambient environment conditions.
