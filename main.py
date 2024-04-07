import csv
from convertor.temperature import to_celsius, to_fahrenheit
from convertor.distance import meters_to_feet, feet_to_meters

def convert_file(input_file):
    output_file = input_file.replace('.csv', '_converted.csv')
    
    with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        
        if "Reading" in fieldnames and "Distance" not in fieldnames:
            fieldnames = ['Date', 'Reading']
            convert_temperature(reader, outfile, fieldnames)
        elif "Distance" in fieldnames:
            fieldnames = ['Date', 'Distance', 'Reading']
            convert_distance(reader, outfile, fieldnames)

def convert_temperature(reader, outfile, fieldnames):
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        reading = row['Reading'].replace('°C', '').replace('°F', '').replace('Â', '').strip()
        try:
            value = float(reading)
        except ValueError:
            print(f"Could not convert {reading} to float.")
            continue

        unit = 'C' if '°C' in row['Reading'] else 'F'
        if unit == 'F':
            row['Reading'] = f"{to_celsius(value)}°C"
        elif unit == 'C':
            row['Reading'] = f"{to_fahrenheit(value)}°F"
        writer.writerow(row)


def convert_distance(reader, outfile, fieldnames):
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        
        distance = row['Distance'].replace('m', '').replace('ft', '').strip()
        try:
            distance_value = float(distance)
        except ValueError:
            print(f"Could not convert distance {distance} to float.")
            continue

        if 'm' in row['Distance']:
            row['Distance'] = f"{meters_to_feet(distance_value)}ft"
        elif 'ft' in row['Distance']:
            row['Distance'] = f"{feet_to_meters(distance_value)}m"
        
        
        reading = row['Reading'].replace('°C', '').replace('°F', '').replace('Â', '').strip()
        try:
            temperature_value = float(reading)
        except ValueError:
            print(f"Could not convert temperature {reading} to float.")
            continue

        unit = 'C' if '°C' in row['Reading'] else 'F'
        if unit == 'F':
            row['Reading'] = f"{to_celsius(temperature_value)}°C"
        elif unit == 'C':
            row['Reading'] = f"{to_fahrenheit(temperature_value)}°F"

        writer.writerow(row)


convert_file('temperatures.csv')
convert_file('distances.csv')