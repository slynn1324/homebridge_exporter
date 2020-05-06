from hapclient.client import HapClient
from hapclient.model.characteristics import CharacteristicTypes
import os
import json
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=False, help="Output File")
parser.add_argument('--address', required=True, help="Homebridge Address")
parser.add_argument('--port', required=True, help="Homebridge Port (usually 51826)")
parser.add_argument('--pin', required=True, help="The pairing pin for Homebridge")
args = parser.parse_args()

output_file = args.output



PAIRING_DATA_FILE = "pairingdata.json"

pairing_data = None

if os.path.exists(PAIRING_DATA_FILE):
	with open(PAIRING_DATA_FILE, 'r') as f:
		pairing_data = json.loads(f.read())


client = HapClient('python_hapclient', address=args.address, port=args.port, pairing_data=pairing_data)

#pin = "031-45-154"

client.pair(args.pin)

#print(json.dumps(client.pairing_data, indent=2))
# if the original pairing_data was null, let's save it for next time
if pairing_data == None:
	with open(PAIRING_DATA_FILE, 'w') as f:
		f.write(json.dumps(client.pairing_data))


data = client.get_accessories()

metrics = []

def clean_name(name):
	if name == None:
		name = ""
	name = name.lower()
	return re.sub("[^a-z0-9]", "_", name)


def add_metric(metric_name, accessory_name, service_name, value):
	metrics.append('homebridge_{}{{accessory="{}",service="{}"}} {}'.format(clean_name(metric_name), clean_name(accessory_name), clean_name(service_name), value))

def get_accessory_name(a):

	accessory_name = None

	for service in a['services']:
		if service['type'] == 'public.hap.service.accessory-information':
			for characteristic in service['characteristics']:
				if characteristic['type'] == 'public.hap.characteristic.name':
					accessory_name = characteristic['value']

	return accessory_name

def get_service_name(svc):

	service_name = None

	for characteristic in service['characteristics']:
		if characteristic['type'] == 'public.hap.characteristic.name':
			service_name = characteristic['value']

	return service_name

def get_metric_name_for_characteristic(characteristic):
	metric_name = characteristic['type']
	metric_name = metric_name.replace("public.hap.characteristic.", "")
	metric_name = metric_name.replace(".", "_")
	metric_name = metric_name.replace("-", "_")
	metric_name = clean_name(metric_name)

	if metric_name.startswith("unknown_characteristic_"):
		char_desc = characteristic.get('description')
		if char_desc != None:
			metric_name = clean_name(char_desc)

	return metric_name

def get_value_for_characteristic(characteristic):
	value = None

	char_format = characteristic.get('format')

	if char_format == 'uint8':
		value = characteristic.get('value')
	elif char_format == 'float':
		value = characteristic.get('value')
	elif char_format == 'bool':
		if characteristic.get('value'):
			value = 1
		else:
			value = 0

	return value

def add_thermostat(accessory_name, service):

	service_name = get_service_name(service)
	if service_name == None:
		service_name = accessory_name

	for characteristic in service['characteristics']:
		
		metric_name = get_metric_name_for_characteristic(characteristic)
		metric_value = get_value_for_characteristic(characteristic)

		if metric_value != None:
			add_metric(metric_name, accessory_name, service_name, metric_value)


for accessory in data['accessories']:

	accessory_name = get_accessory_name(accessory)

	for service in accessory['services']:

		#if service['type'] == 'public.hap.service.thermostat':

		add_thermostat(accessory_name, service)


if output_file != None:
	# use a temprary file to get an atomic write of the target file
	tmp_file = output_file + ".tmp"

	with open(tmp_file, 'w') as f:
		for m in metrics:
			f.write(m)
			f.write("\n")

	os.rename(tmp_file, output_file)

else:
	for metric in metrics:
		print(metric)
