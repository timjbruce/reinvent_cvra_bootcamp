# AWS Connected Vehicle Reference Architecture Bootcamp
During this Bootcamp, we'll take a deep dive into the AWS 
Connected Vehicle Reference Architecture. Attendees will install it, 
generate trip data from a simulated vehicle, and learn how 
the data can be accessed with various other AWS services. In 
this bootcamp, we'll access trip data using an Alexa skill.

> #### Prerequisites
>We'll assume that you have some basic knowledge of AWS 
services like IAM, Cloudformation, DynamoDB, S3, IoT, etc., 
are comfortable using the AWS CLI, and have some knowledge 
of Python. You'll also need to prepare the following <b>prior</b> 
to the workshop: 
>* Laptop running Windows or MacOS
>* An AWS account with Administrator Access
>* The AWS CLI, configured with an Administrator Access ([directions here](https://docs.aws.amazon.com/cli/latest/userguide/installing.html))
>* The ASK CLI ([Alexa Skills Kit CLI](https://developer.amazon.com/docs/smapi/quick-start-alexa-skills-kit-command-line-interface.html#step-1-prerequisites-for-using-ask-cli))
>* Python, Node, and NPM, Virtualenv, git
>* a HERE Maps app_code and app_id (register for a free account at [developer.here.com](developer.here.com))

## Introduction
This Bootcamp has four main parts as shown below. The intent 
of this Bootcamp is to help attendees understand what's "under the 
hood" of the CVRA and the IoT Device Simulator so that they can 
modify and extended it to fir their scenarios. 
1. Deploy the CVRA (15 mins.)
2. Install the IoT Device Simulator and Generate Trip Data (30 mins.)
3. Deploy the CarGuru Alexa Skill (20 mins.)
4. Cleanup (10 mins.)
5. Ideas for Customization and Enhancement

> If you have established an AWS account within the last 12 months, then this lab will be in the free tier. Otherwise, costs are anticipated to be less than $5

## Local Prepation Steps
First, create a *work directory* where you can download the git repository for this bootcamp,
save the worksheet, make notes, etc. On my macOS system, I use ~/Developer/bootcamps (that is, /Users/dixonaws/Developer/bootcamps.) 
Second, clone the git repository for this bootcamp:
```bash
git clone https://github.com/dixonaws/reinvent_cvra_bootcamp
```

You should now have a new directory, *reinvent_cvra_bootcamp* in your work direcrtory. Make

Third, complete the worksheet below *or*, if you are on macOS, you can use a utility in the reinvent_cvra_bootcamp to
check versions and create worksheet (called worksheet.txt) for you:
```bash
chmod +x create_worksheet.sh
./create_worksheet.sh
```

## Deploy the CVRA
Let's deploy the Connected Vehicle Reference Architecture (CVRA).
 Following the [directions here](https://docs.aws.amazon.com/solutions/latest/connected-vehicle-solution/deployment.html), deploy 
 the CVRA in an AWS account where you have administrator access.
The CVRA comes with a Cloudformation template that deploys and configures
all of the AWS services necessary to ingest, store, process, and
analyze data at scale from IoT devices. Automotive use cases aside,
the CVRA provides a useful example of how to secure connect an 
IoT device, perform JITR (Just in Time Registration), use 
Kinesis Analytics to query streams of data, use an IoT rule to 
store data in S3, etc.

The CVRA Cloudformation 
template returns these outputs:

| Key | Value | Description | Associated AWS Service
|:---|:---|:---|:---
UserPool|arn:aws:cognito-idp:us-east-1:000000000:userpool/us-east-1_loAchZlyI|Connected Vehicle User Pool| Cognito
CognitoIdentityPoolId|us-east-1:de4766b0-519a-4030-b036-97a3a2291c98|	Identity Pool ID| Cognito
VehicleOwnerTable|	cvra-demo-VehicleOwnerTable-1TMCCT7LY76B0|	Vehicle Owner table|DynamoDB
CognitoUserPoolId|	us-east-1_loAchZlyI|	Connected Vehicle User Pool ID|Cognito
CognitoClientId|	6rjtru6aur0vni0htpvb49qeuf|	Connected Vehicle Client|Cognito
DtcTable|	cvra-demo-DtcTable-UPJUO460FVYT|	DTC reference table|DynamoDB
VehicleAnomalyTable|	cvra-demo-VehicleAnomalyTable-E3ZR7I8BN41D|	Vehicle Anomaly table|DynamoDB
VehicleTripTable|	cvra-demo-VehicleTripTable-U0C6DSG0JW11|	Vehicle Trip table|DynamoDB
TelemetricsApiEndpoint|	https://abcdef.execute-api.us-east-1.amazonaws.com/prod|RESTful API endpoint to interact with the CVRA (Cognito authZ required)|API Gateway
Telemetrics API ID|(not used)|(not used)|API Gateway
HealthReportTable|	cvra-demo-HealthReportTable-C4VRARO31UZ1|	Vehicle Health Report table|DynamoDB
VehicleDtcTable|	cvra-demo-VehicleDtcTable-76E1UB71GEH3|	Vehicle DTC table|DynamoDB

**Validation**: run the following command from a terminal window:
```bash
aws cloudformation describe-stacks --stack-name cvra-demo --query 'Stacks[*].StackStatus'
```

> We'll refer to the CVRA Cloudformation stack as **cvra-demo** throughout this bootcamp.

The output should resemble something like this:
```json
[
    "CREATE_COMPLETE"
]
```

We're interested in the *VehicleTripTable* -- a table in DynamoDB. You can view the outputs from your 
CVRA deployment through the AWS Console or by using the CLI with something like:
```bash
aws cloudformation describe-stacks --stack-name cvra-demo --output table --query 'Stacks[*].Outputs[*]'
```

 
## Generate Trip Data
In this section, you'll install and configure the AWS IoT Device Simulator to generate 
trip data. [Follow these directions](https://aws.amazon.com/answers/iot/iot-device-simulator/) 
to install the simulator in your own AWS account.

You can provision up to 25 vehicles to simulate trip data. Each simulated
vehicle will travel one of several paths that have been pre-defined by the IoT
device simulator. 

The CVRA expects data to be published to a topic called: `connectedcar/telemetry/<VIN>` The 
device simulator allows you to simulate a number of vehicles and generate trip data.
The payload is of the form:

```json
{
  "timestamp": "2018-08-25 22:38:40.791000000",
  "trip_id": "871be6ea-4ee6-49b8-8a9b-b6ebe5050c8a",
  "vin": "9JVVV63E5NVZWH5UH",
  "name": "odometer",
  "value": 2.267
}
```


## Deploy an Alexa Skill to Read Recent Trip Data
In this section, we'll deploy an Alexa skill called CarGuru that will read back information about 
the three recent trips that you have taken. You must have the ASK-CLI installed to complete this part of the lab.

#### Run a Python Program to Test Your Access
First, you can use a Python program included with the reinvent_cvra_bootcamp repo, getRecentTrips.py, to 
test your configuration sofar. The best way to run this program is within a Python Virtual Environment. For the 
impatient, install a virtual environment, install the dependencies from requirements.txt, and run getRecentTrips.py.

<details>
<summary><strong>Step-by-step instructions (expand for details)</strong></summary>
<p>
Install and activate Python virtual environment in `pwd`/venv (macOS):
```bash
virtualenv -p `which python3` venv
source venv/bin/activate
```

Install dependencies (macOS):
```bash
pip install -r requirements.txt
```

Run the program:
```bash
python getRecentTrips.py <TripTable>
```

Or, if you wanted to be very clever using your <i>ninja bash skills</i>, you could do something like this on the bash prompt: 

```bash
python getRecentTrips.py `aws cloudformation describe-stacks --stack-name cvra-demo --output table --query 'Stacks[*].Outputs[*]' |grep 'Vehicle Trip table' |awk -F "|" '{print $4}'`
```
> Quote trifecta: Note the tricky combination of backticks, single quotes, AND double quotes!
</p>
</details>
<br>

You should see output similar to the following after running the program:
```json(venv) f45c898a35bf:reinventCvraBootcamp dixonaws$ python3 getRecentTrips.py cvra-demo-VehicleTripTable-U0C6DSG0JW11
Scanning trip table cvra-demo-VehicleTripTable-U0C6DSG0JW11... done (0).
Found 18 items in the trip table.
dictItems is a <class 'list'>
**** Trip 1 (VIN: 2Z61V6JISOE60EWI8)
{'ignition_status': {'S': 'off'}, 'transmission_gear_position': {'S': 'fourth'}, 'engine_speed_mean': {'N': '3525.2780709525855'}, 'name': {'S': 'aggregated_telemetrics'}, 'driver_safety_score': {'N': '74.82328344340092'}, 'brake_mean': {'N': '0'}, 'high_braking_event': {'N': '0'}, 'fuel_level': {'N': '99.95453355436261'}, 'latitude': {'N': '38.958911'}, 'idle_duration': {'N': '213'}, 'fuel_consumed_since_restart': {'N': '0.019374198537822133'}, 'torque_at_transmission_mean': {'N': '314.3124901722019'}, 'timestamp': {'S': '2018-08-21 23:13:01.589000000'}, 'vehicle_speed_mean': {'N': '79.9034721171209'}, 'start_time': {'S': '2018-08-21T23:12:31.456Z'}, 'end_time': {'S': '2018-08-21T23:13:01.589Z'}, 'trip_id': {'S': '84983a6b-0881-4600-ad20-9db40eb7f868'}, 'oil_temp_mean': {'N': '29.021054075000006'}, 'geojson': {'M': {'bucket': {'S': 'connected-vehicle-trip-us-east-1-477157386854'}, 'key': {'S': 'trip/2Z61V6JISOE60EWI8/84983a6b-0881-4600-ad20-9db40eb7f868.json'}}}, 'accelerator_pedal_position_mean': {'N': '38.609446258882855'}, 'longitude': {'N': '-77.401168'}, 'vin': {'S': '2Z61V6JISOE60EWI8'}, 'brake_pedal_status': {'BOOL': False}, 'high_speed_duration': {'N': '0'}, 'odometer': {'N': '0.6705392939350361'}, 'high_acceleration_event': {'N': '2'}}
...

```


<details>
<summary><strong>Code details for getRecentTrips.py (expand for details)</strong></summary>
Have a look at the code listing for getRecentTrips.py. The guts 
are similar to the CarGuru skill that we'll deploy in the next
step, particularly the call to <i>scan</i> the DynamoDB trip table:

```python 
dynamoDbClient=boto3.client('dynamodb')

    response=dynamoDbClient.scan(
        TableName='cvra-demo-VehicleTripTable-U0C6DSG0JW11',
        Select='ALL_ATTRIBUTES'
    )

    dictItems=response['Items']

    intRecordCount=json.dumps(response['Count'])
    print("Found " + str(intRecordCount) + " items in the trip table.")

    intTripNumber=1
    for item in dictItems:
        strVin=str(item['vin']['S'])
        print("**** Trip " + str(intTripNumber) + " (VIN: " + strVin + ")")
        print(item)
        print()
        intTripNumber=intTripNumber+1

    print("dictItems is a " + str(type(dictItems)))

```
> An improvement here for production applications would be to 
> query the DynamoDB table instead of scanning it, per the 
> [best practices for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html). 
> You may even elect to create an API layer in front fo the 
> DynamoDB table so that other applications can use the 
> data.
</details>


#### Deploy the CarGuru Alexa Skill
In ths step, you'll use the trip data recorded in your DynamoDB table with an Alexa skill called CarGuru.
Once you have confirmed that your DynamoDB Trip table contains trip data, issue the following command to clone the CarGuru skill:

```bash
ask new --skill-name "CarGuru" --url https://github.com/dixonaws/CarGuru.git  
```

Modify CarGuru's Lambda function to use your DynamoDB table. Then simply deploy it with:
```bash
ask deploy
```

### Cleanup
The last thing to do in this bootcamp is to clean up any resources that were deployed in your account. 
From your worksheet, delete the following Cloudformation stacks:
* Your CVRA Cloudformation stack
* Your vehicle simulator Cloudformation stack

```bash
aws cloudformation delete-stack --stack-name <your CVRA stack>
aws cloudformation delete-stack --stack-name <your vehicle simulator stack>
```

From the AWS console, ensure that any associated S3 buckets, DynamoDB tables, and IoT service is clean.


#### Ideas for Customization and Enhancement
Hopefully, you were able to learn how to make use
of the data collected by a simulated connected vehicle (and ultimately any connected 
device). Here are some ideas to make enhancements and improvements from here:
* Adjust the IAM roles for more granular permissions
* Develop account linking for the CarGuru skill to read back information only for linked VINs
* Create an authenticated API to access the VehicleTripTable (API Gateway, Lambda, Cognito)
* Enhance CarGuru to get the latest fuel prices in a certain location
* Deploy the solution with a real vehicle, using Greengrass and an OBD II dongle!