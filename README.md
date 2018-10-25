# AMT303 Deep Dive into the AWS Connected Vehicle Reference Solution Workshop
During this Workshop, we'll take a deep dive into the AWS
Connected Vehicle Reference Architecture. Attendees will install it, build functions on top of the CVRA including an Alexa Skill, generate trip data from a simulated vehicles, and learn how the data can be accessed with various other AWS services.

#### Prerequisites
We'll assume that you have some basic knowledge of AWS
services like IAM, Cloudformation, DynamoDB, S3, IoT, etc.,
are comfortable using the AWS CLI, and have some knowledge
of Python. You'll also need to prepare the following for
the workshop (can be done in Cloud9 or on your local machine):
* Laptop running Windows or MacOS and Google Chrome or Mozilla Firefox (Safari, Internet Explorer, or Microsoft Edge are not recommended)
* An AWS account with Administrator Access
* The AWS CLI, configured with a user that has Administrator Access ([directions here](https://docs.aws.amazon.com/cli/latest/userguide/installing.html))
* Python, Virtualenv, git
* a HERE Maps app_code and app_id (register for a free account at [developer.here.com](developer.here.com))
* Mapbox Account (you will need a Token for the IoT Simulator)

Due to AWS Service availability in certain Regions we suggest you use **US-EAST-1** for this workshop.

## Introduction
This Workshop has five main sections as shown below. The intent
of this Workshop is to help attendees understand what's "under the
hood" of the CVRA and the IoT Device Simulator so that they can
modify and extended it to for their scenarios.

1. Deploy the [CVRA](#Deploy-the-CVRA) and [IoT Device Simulator](#Deploy-the-IoT-Device-Simulator) (15 mins)
3. Build a Fleet Management Function (10 mins)
4. Generate Trip Data (5 mins)
5. Deploy the ConnectedCar Alexa Skill (30 mins)
6. Build the Remote Command function (30 mins)
7. Cleanup

> If you have established an AWS account within the last 12 months, then this lab will be in the free tier. Otherwise, costs are anticipated to be less than $5.
For the AMT303 workshop we will be providing Credits to covers costs at the end of the workshop.

This workshop has been written as modular and therefore after deploying the CVRA and the IoT Device Simulator each exercise is independent.
---

## Cloud9 Preparation Steps (Optional)
> We recommend using a Cloud9 instance (hosted IDE) for the next steps, as it is bandwidth-friendly and helpful during troubleshooting!
> Cloud9 is free-tier eligible

Next, clone the git repository for this bootcamp:
```bash
git clone https://github.com/dixonaws/reinvent_cvra_bootcamp
```

You should now have a new directory, *reinvent_cvra_bootcamp* in your work directory. Third, complete the
worksheet below *or*, if you are on macOS/Cloud9, you can use a utility in the reinvent_cvra_bootcamp to
check versions and create worksheet (called worksheet.txt) for you:
```bash
chmod +x create_worksheet.sh
./create_worksheet.sh
```

<b>*** Now, you're ready to move on to the next step and deploy the Connected Vehicle Reference Architecture *** </b>

---

## Step 1. Deploy the CVRA and IoT Device Simulator
### Deploying the CVRA
Let's deploy the Connected Vehicle Reference Architecture (CVRA).
 Following the [directions here](https://docs.aws.amazon.com/solutions/latest/connected-vehicle-solution/deployment.html), deploy
 the CVRA in an AWS account where you have administrator access.
We'll use "cvra-demo" for the stack name in this lab. The CVRA comes with a Cloudformation template that deploys and configures
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

*** Now, you can move on to Step 2, Deploy the IoT Device Simulator ***

---

### Deploying the IoT Device Simulator
In this section, you'll install and configure the AWS IoT Device Simulator and use the Automotive module to generate trip data.
[Follow these directions](https://aws.amazon.com/answers/iot/iot-device-simulator/)
to install the simulator in your own AWS account.

If the IoT Device Simulator CloudFormation Template fails to deploy due to a Permissions issue on ECS, just delete the Stack and re-deploy it again.

**Please note that you will need to enter an Email address you have access to in the workshop while deploying the Stack. Once the stack has deployed you will receive an Email with login instructions.**

You will need to setup the Mapbox Token within the IoT Device Simulator Web Portal. For detailed instructions of how to do this [follow these instructions](/MapBox/README.md).

At this point, you can move on to the next steps where you will build a Fleet Management Function and build an Alexa Skill.

---

## Building the Fleet Management Function
Click on the link for the [Fleet Management](fleetManagement/README.md) workshop module instructions.

---

## Generate Trip Data
If you have generated trips as part of the Fleet Management module you can skip this step.

Log into the IoT Device Simulator Web Console.

*The URL and credentials would have been sent to you via an Email, the Email address is the one your defined in the Stack deployment.*

From the left hand menu select *Automotive* and select **+ Add Vehicles** at the top of the page, choose the number of vehicles you want to create and click **Sumbit**.

We suggest you provision 5 vehicles to simulate trip data. Each simulated
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

---

## Deploy the ConnectedCar Alexa Skill
Click on the link for the [Alexa Skill](AlexSkill/README.md) workshop module instructions.

If you have skipped the Fleet Management module please make sure you follow the [instructions](#Generate-Trip-Data) to generate some trip data before you start this Alexa Skill module.

---

## Build the Remote Command Function
Click on the link for the [Remote Command](remoteCommands/README.md) workshop module instructions.

*For this module you will need to write your own Lambda functions and the instructions only provide you with code snippets*

---

## Cleanup (10 mins)
The last thing to do in this workshop is to clean up any resources that were deployed in your account.

From the AWS console, ensure that any associated S3 buckets, DynamoDB tables, and IoT service are clean.

Also be sure to delete the following:
* The Lambda function for ConnectedCar
* Delete the Fleet Management & Remote Command Function Code
* The ConnectedCar skill from developer.amazon.com


From your worksheet, delete the following Cloudformation stacks:
* Your CVRA Cloudformation stack
* Your vehicle simulator Cloudformation stack

Delete your Cloud9 instance if you created one.

```bash
aws cloudformation delete-stack --stack-name <your CVRA stack>
aws cloudformation delete-stack --stack-name <your vehicle simulator stack>
```

---

## Ideas for Customization and Enhancement
Hopefully, you were able to learn how to make use
of the data collected by a simulated connected vehicle (and ultimately any connected device). Here are some ideas to make enhancements and improvements from here:
* Enhance the Alexa skill to read values from many different cars
* Adjust the IAM roles for more granular permissions
* Develop account linking for the ConnectedCar skill to read back information only for linked VINs
* Create an authenticated API to access the VehicleTripTable (API Gateway, Lambda, Cognito)
* Enhance the ConnectedCar Alexa skill to get the latest fuel prices in a certain location
* Connect to other public APIs to enhance your Alexa skill
* Create a deployment pipeline for your Alexa skill and Lambda function
* Deploy the CVRA solution with a real vehicle, using Greengrass and an OBDII interface!
