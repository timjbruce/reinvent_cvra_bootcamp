# AWS Connected Vehicle Reference Architecture Bootcamp
During this Bootcamp, we'll take a deep dive into the AWS Connected Vehicle Reference Architecture. You'll install it, generate trip data from a simulated vehicle, and learn how the data can be accessed with various other AWS services. In this bootcamp, we'll access trip data using an Alexa skill.

#### Prerequisites
We'll assume that you have some basic knowledge of AWS services like IAM, DynamoDB, S3, IoT, etc., are comfortable using the AWS CLI, and have some knowledge of Python. You'll also need to prepare the following prior to the workshop: 
* Laptop running Windows or MacOS
* An AWS account with Administrator Access
* The AWS CLI, configured with an Administrator Access

## Deploy the CVRA
The CVRA returns the following outputs:
The CVRA Cloudformation template returns these outputs:

Key|Value|Description
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

We're interested in the VehicleTripTable -- a table in DynamoDB

## Generate Trip Data
//todo

## Deploy an Alexa Skill to Read Recent Trip Data
In this section, we'll deploy an Alexa skill called CarGuru that will read back information about the three recent trips that you have taken.

#### Run a Python Program to Test Your Access
//todo

#### Deploy the CarGuru Alexa Skill
//todo