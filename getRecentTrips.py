import boto3
import json
import argparse
import time
import sys

def main():
    parser = argparse.ArgumentParser(
        description='getRecentTrips scans the DynamoDB table that was setup as a part of the Connected Vehicle Reference Architecture, returning the total number of trips and informtion about the last three.')
    parser.add_argument('VehicleTripTable',
                        help='The DynamoDB trip table that was deployed as a part of the Connected Vehicle Reference Architeture')
    args = parser.parse_args()

    strVehicleTripTable = args.VehicleTripTable

    strRegion = 'us-east-1'

    dynamoDbClient = boto3.client('dynamodb', region_name=strRegion)

    sys.stdout.write('Scanning trip table ' + strVehicleTripTable + '... ')

    intStartTime = int(time.time())
    response = dynamoDbClient.scan(
        TableName=strVehicleTripTable,
        Select='ALL_ATTRIBUTES'
    )
    intEndTime = int(time.time())

    intTotalTime = intStartTime - intEndTime

    print('done (' + str(intTotalTime) + ').')

    dictItems = response['Items']

    intRecordCount = json.dumps(response['Count'])
    print("Found " + str(intRecordCount) + " items in the trip table.")
    print("dictItems is a " + str(type(dictItems)))

    intTripNumber = 1
    for item in dictItems:
        strVin = str(item['vin']['S'])
        print("**** Trip " + str(intTripNumber) + " (VIN: " + strVin + ")")
        print(item)
        print()
        intTripNumber = intTripNumber + 1


main()
