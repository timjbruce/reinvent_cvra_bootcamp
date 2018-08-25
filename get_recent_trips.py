import boto3
import json
import argparse
import time
import sys
import requests


def sortFunc(e):
	return e['timestamp']['S']


# // sortFunc()

def getLocationInfo(strProx, strApp_id, strApp_code):
	# this method takes the following parameters:
	# strProx = '41.8842,-87.6388,250'
	# strApp_id = 'cF1SE2QqJkuUgBEQHEma'
	# strApp_code = 'rKLZInnnnJDvNE5ioQIMEg'

	strUrl = 'https://reverse.geocoder.api.here.com/6.2/reversegeocode.json'
	dictHeaders = {'Content-Type': '*'}
	dictPayload = {
		'prox': strProx,
		'mode': 'retrieveAddresses',
		'maxresults': '1',
		'gen': '9',
		'app_id': strApp_id,
		'app_code': strApp_code
	}

	response = requests.get(strUrl, headers=dictHeaders, params=dictPayload)

	jsonResponse = response.json()

	return (jsonResponse['Response']['View'][0]['Result'][0]['Location']['Address'])


# // getLocationInfo()

def main():
	parser = argparse.ArgumentParser(
		description='Example: python3 get_recent_trips.py -t "cvra-demo-VehicleTripTable-abcdef" -i "cF1SE2QqJkxyzabc" -c "xyzabcJDvNE5ioQIMEg"')

	requiredNamed = parser.add_argument_group('required named arguments')
	requiredNamed.add_argument('-t', '--VehicleTripTable',
							   help='VehicleTripTable, the DynamoDB table provisioned by the Connected Vehicle Reference Archietcture',
							   required=True)
	requiredNamed.add_argument('-i', '--HereAppId',
							   help='HERE Maps app_id for determining location (register at developer.here.com)',
							   required=True)
	requiredNamed.add_argument('-c', '--HereAppCode',
							   help='HERE Maps app_code for determining location (register at developer.here.com)',
							   required=True)

	args = parser.parse_args()

	print("Using args: " + str(args))

	strVehicleTripTable = args.VehicleTripTable

	# reverse geocoding with HERE maps
	# https://developer.here.com/documentation/geocoder/topics/example-reverse-geocoding.html

	strApp_code = args.HereAppCode
	strApp_id = args.HereAppId

	strRegion = 'us-east-1'

	dynamoDbClient = boto3.client('dynamodb', region_name=strRegion)

	sys.stdout.write('Scanning trip table ' + strVehicleTripTable + '... ')

	intStartTime = int(time.time())
	response = dynamoDbClient.scan(
		TableName=strVehicleTripTable,
		Select='ALL_ATTRIBUTES'
	)

	intEndTime = int(time.time())
	intTotalTime = intEndTime - intStartTime

	print('done (' + str(intTotalTime) + 'ms).')

	listTrips = response['Items']

	# if you want to convert the response to JSON, just  use json.dumps(response) as in the following
	# strJsonResponse=json.dumps(response)
	# print(strJsonResponse)

	# sort the list by timestamp
	listTrips.sort(key=sortFunc)

	intRecordCount = json.dumps(response['Count'])
	print("Found " + str(intRecordCount) + " items in the trip table.")
	print("listItems is a " + str(type(listTrips)))

	intTripNumber = 1
	for trip in listTrips:
		strVin = str(trip['vin']['S'])
		strTripId = str(trip['trip_id']['S'])
		strTimestamp = str(trip['timestamp']['S'])
		strLongitude = str(trip['longitude']['N'])
		strLatitude = str(trip['latitude']['N'])
		strProx = strLatitude + "," + strLongitude
		floatDistance = trip['odometer']['N']
		floatFuelConsumed = trip['fuel_consumed_since_restart']['N']

		# call a method to do reverse geocoding on given lat/long
		jsonLocationInfo = getLocationInfo(strProx, strApp_id, strApp_code)

		strAddressLabel = ""
		strCity = ""
		strState = ""
		strDistrict = ""

		try:
			strAddressLabel = jsonLocationInfo['Label']
			strCity = jsonLocationInfo['City']
			strState = jsonLocationInfo['State']
			strDistrict = jsonLocationInfo['District']
		except KeyError:
			pass

		print("**** Trip " + str(intTripNumber) + " (trip_id: " + strTripId + ", VIN: " + strVin + ")")
		print("Time: " + strTimestamp + ")")
		print("Location: near " + strAddressLabel)
		print("Neighborhood: " + strDistrict)
		print("Distance: " + str(floatDistance) + " miles")
		print("Fuel consumed: " + str(floatFuelConsumed) + " gallons")
		print("All trip data: " + str(trip))
		print()
		intTripNumber = intTripNumber + 1


main()
