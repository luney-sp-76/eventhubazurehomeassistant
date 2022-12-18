import dbconn

#  call to the database
cnx = dbconn.connected()
cursor = cnx.cursor(dictionary=True)


#  returns all the device specifications associated with a given user id
def list_smart_device_specs(user):
    """ :param user:int
    """
    statement = f"""select device_name, current_level_percentual_offset,wattage_percentual_offset,energy_kwh, 
    temperature_degrees_centigrade, voltage_level_percentual_offset, device_voltage.date_of_read from device
    LEFT JOIN device_current
    ON device_current.device_id = device.device_id
    LEFT JOIN device_energy
    ON device_energy.device_id = device.device_id
    LEFT JOIN device_power
    ON device_power.device_id = device.device_id
    LEFT JOIN device_temperature
    ON device_temperature.device_id = device.device_id
    LEFT JOIN device_voltage
    ON device_voltage.device_id = device.device_id
    WHERE device.is_smart_device = true and device.device_id IN(select device_id from user_device WHERE user_id = {user} )"""

    cursor.execute(statement)

    return cursor.fetchall()


results = list_smart_device_specs(1)

for row in results:
    device = row['device_name']
    current_percentage = row['current_level_percentual_offset']
    wattage = row['wattage_percentual_offset']
    energy = row['energy_kwh']
    temperature = row['temperature_degrees_centigrade']
    voltage = row['voltage_level_percentual_offset']
    date_of_read = row['date_of_read']

    print('Name: %s | Percentage: %s | Wattage:  %s | Energy %s | Temperature %s | Voltage %s | Date %s' % (
        device, current_percentage, wattage, energy, temperature, voltage, date_of_read))
