my_devices = {
  'rtr1': {
    'host': 'device1',
    'device_type': 'cisco',
  },
  'rtr2': {
    'host': 'device2',
    'device_type': 'junos',
  }
}
device_type_rtr1 = my_devices['rtr2']['device_type']
print(device_type_rtr1)
print(type(my_devices))
