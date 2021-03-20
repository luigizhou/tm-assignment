#!/usr/bin/env python3

import requests
import argparse
from tabulate import tabulate
import time

class Cli:
	"""
		CLI class
	"""

	def __init__(self, address):
		self.url = address
		self.all_services = []
		self.service_types = {}


	def get_service(self, service_ip):
		service =  requests.get(self.url + service_ip).json()
		service['ip'] = service_ip
		return service

	def get_all_services(self):
		r = requests.get(self.url + 'servers')
		all_services = []
		for service_ip in r.json():
			all_services.append(self.get_service(service_ip))
		self.all_services = all_services
		self.service_types = {service['service'] for service in all_services}

	def get_average_by_service(self, service_type):
		cpu = 0
		mem = 0
		service_count = 0
		for service in self.all_services:
			if service['service'] == service_type:
				service_count += 1
				cpu += int(service['cpu'].strip('%'))
				mem += int(service['memory'].strip('%'))
		return {'service': service_type, 'avg_cpu': "{0:.0%}".format(cpu / service_count / 100), 'avg_mem': "{0:.0%}".format(mem / service_count / 100), 'service_count': service_count}


	def running_services(self):
		self.get_all_services()
		return tabulate(self.all_services, headers="keys")


	def average_services(self):
		self.get_all_services()
		result = []
		for service_type in self.service_types:
			result.append(self.get_average_by_service(service_type))
		return tabulate(result, headers="keys")

	def flag_services(self):
		self.get_all_services()
		result = []
		for service_type in self.service_types:
			avg_service = self.get_average_by_service(service_type)
			if avg_service['service_count'] < 2:
				result.append(avg_service)
		if result:
			return tabulate(result)
		else:
			return '0 services with less than 2 instances'

	def track_service(self,service_type):
		loop_count = 10
		all_services_by_type = []
		while True:
			if loop_count >= 10:
				loop_count = 0
				self.get_all_services()
				for service in self.all_services:
					if service['service'] == service_type:
						all_services_by_type.append(service)
			for idx,service in enumerate(all_services_by_type):
				updated_service = self.get_service(service['ip'])
				all_services_by_type[idx] = updated_service
			print(tabulate(all_services_by_type, headers="keys"))
			time.sleep(1)
			loop_count += 1


def main(args):
	try:
		r = requests.get(args.address  + '/servers' )
		if r.status_code == 200:
			cli = Cli(args.address + '/')
		else:
			print('Unexpected error, please check the address and try again')
		if args.get_running_services:
			print(cli.running_services())
		elif args.flag_services:
			print("Flagged Services: \n" + cli.flag_services())
		elif args.get_averages:
			print(cli.average_services())
		elif args.track_service:
			print(cli.track_service(args.track_service))
	except requests.exceptions.ConnectionError as err:
		print('Invalid Address. Format of address must be http://ip:port')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("address", help="address of the cpx api (i.e. http://localhost:port )", type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--get-running-services', help="challenge1, print running services", action='store_true')
    group.add_argument('--get-averages', help="challenge2, print averages for running services", action='store_true')
    group.add_argument('--flag-services', help="challenge3, print services that have less than 2 instance running", action='store_true')
    group.add_argument('--track-service', help="challenge4, track cpu and mem of a specificed service", type=str)

    args = parser.parse_args()

    main(args)



