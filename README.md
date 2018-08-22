# AWS Connected Vehicle Reference Architecture Bootcamp
During this Bootcamp, we'll take a deep dive into the AWS 
Connected Vehicle Reference Architecture. You'll install it, 
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
>* Python, Node, and NPM

## Introduction
This Bootcamp has four main parts as shown below. The intent 
of this Bootcamp is to help attendees understand what's "under the 
hood" of the CVRA so that it can be modified and extended as desired. 
1. Deploy the CVRA (15 mins.)
2. Generate Trip Data (10 mins.)
3. Deploy the CarGuru Alexa Skill (20 mins.)
4. Cleanup (10 mins.)

> If you have established an AWS account within the last 12 months, then this lab will be in the free tier. Otherwise, costs are anticipated to be less than $5

## Deploy the CVRA
Let's deploy the Connected Vehicle Reference Architecture (CVRA).
 Following the [directions here](https://docs.aws.amazon.com/solutions/latest/connected-vehicle-solution/deployment.html).
The CVRA is a Cloudformation template that deploys and configures
all of the AWS services necessary to ingest, store, process, and
analyze data at scale from IoT devices. Automotive use cases aside,
the CVRA provides a useful example of how to secure connect an 
IoT device, perform JITR (Just in Time Registration), use 
Kinesis Analytics to query streams of data, use an IoT rule to 
store data in S3, etc.

The CVRA Cloudformation 
template returns these outputs:

| Key | Value | Description |
|:---|:---|:---
UserPool|arn:aws:cognito-idp:us-east-1:000000000:userpool/us-east-1_loAchZlyI|Connected Vehicle User Pool|
CognitoIdentityPoolId|us-east-1:de4766b0-519a-4030-b036-97a3a2291c98|	Identity Pool ID
VehicleOwnerTable|	cvra-demo-VehicleOwnerTable-1TMCCT7LY76B0|	Vehicle Owner table
CognitoUserPoolId|	us-east-1_loAchZlyI|	Connected Vehicle User Pool ID
CognitoClientId|	6rjtru6aur0vni0htpvb49qeuf|	Connected Vehicle Client
DtcTable|	cvra-demo-DtcTable-UPJUO460FVYT|	DTC reference table
VehicleAnomalyTable|	cvra-demo-VehicleAnomalyTable-E3ZR7I8BN41D|	Vehicle Anomaly table
VehicleTripTable|	cvra-demo-VehicleTripTable-U0C6DSG0JW11|	Vehicle Trip table
TelemetricsApiEndpoint|	https://2kkv2uwa45.execute-api.us-east-1.amazonaws.com/prod
Telemetrics API ID|
HealthReportTable|	cvra-demo-HealthReportTable-C4VRARO31UZ1|	Vehicle Health Report table
VehicleDtcTable|	cvra-demo-VehicleDtcTable-76E1UB71GEH3|	Vehicle DTC table

We're interested in the VehicleTripTable -- a table in DynamoDB. You can view the outputs from your CVRA deployment through the AWS Console or by using the CLI with something like:
```bash
aws cloudformation describe-stacks --stack-name cvra-demo --output table --query 'Stacks[*].Outputs[*]'
```
...where <i>cvra-demo</i> is the name of my Cloudformation stack.
 
## Generate Trip Data
//todo

## Deploy an Alexa Skill to Read Recent Trip Data
In this section, we'll deploy an Alexa skill called CarGuru that will read back information about the three recent trips that you have taken. You must have the ASK-CLI installed to complete this part of the lab.

#### Run a Python Program to Test Your Access
Run the getRecentTrips.py program from your laptop to ensure 
that your user has access to the correct DynamoDB table and that 
it is populated with some trip information.

Have a look at the code listing for getRecentTrips.py:
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

```{.line-numbers}

```bash
python3 getRecentTrips.py [TripTable]
```

Or, if you wanted to be very clever using your <i>ninja bash skills</i>, you could do something like this on the bash prompt 

```bash
python3 getRecentTrips.py `aws cloudformation describe-stacks --stack-name cvra-demo --output table --query 'Stacks[*].Outputs[*]' |grep 'Vehicle Trip table' |awk -F "|" '{print $4}'`
```
> Note the tricky combination of backticks and single quotes


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