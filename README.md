# python-VEDirect

## What is this lib ?
Small library to read Victron's VE.Direct frames.

This is useful in order to read Victron's MPPT charge controllers.

You need to use a VE.Direct to FTDI-USB cable

Tested with the [Smart Solar MPPT 100/20](https://www.victronenergy.com/solar-charge-controllers/smartsolar-mppt-75-10-75-15-100-15-100-20)

## How to use this lib ?
First of all, install this library using pip:
```bash
pip3 install vedirect
```

Then, you simply need to import the lib and start asking values:
```python

>>> import vedirect
>>> device = vedirect.VEDirect()
>>> print(device.battery_volts)
27.5
```


The list of available parameters is:

- `battery_volts`
- `battery_amps`
- `solar_volts`
- `solar_power`
- `device_serial`
- `device_MPPT_state`
- `firmware_version`
- `product_id`
- `charge_state`
- `error_code`
- `load_state`
- `load_current`
- `total_yield`
- `yield_today`
- `max_power_today`
- `yield_yesterday`
- `max_power_yesterday`
- `day_sequence`
