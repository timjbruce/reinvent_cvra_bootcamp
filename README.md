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
of Python. You'll also need to prepare the following for
the workshop (can be done in Cloud9 or on your local machine): 
>* Laptop running Windows or MacOS and Google Chrome or Mozilla Firefox (Safari, Internet Explorer, or Microsoft Edge are not recommended)
>* An AWS account with Administrator Access
>* The AWS CLI, configured with a user that has Administrator Access ([directions here](https://docs.aws.amazon.com/cli/latest/userguide/installing.html))
>* Python, Virtualenv, git
>* a HERE Maps app_code and app_id (register for a free account at [developer.here.com](developer.here.com))

## Introduction
This Bootcamp has four main parts as shown below. The intent 
of this Bootcamp is to help attendees understand what's "under the 
hood" of the CVRA and the IoT Device Simulator so that they can 
modify and extended it to fir their scenarios. 
1. Deploy the CVRA (15 mins.)
2. Install the IoT Device Simulator and Generate Trip Data (30 mins.)
3. Deploy the ConnectedCar Alexa Skill (20 mins.)
4. Cleanup (10 mins.)
5. Review Ideas for Customization and Enhancement

> If you have established an AWS account within the last 12 months, then this lab will be in the free tier. Otherwise, costs are anticipated to be less than $5

---

## Cloud9 Preparation Steps
> We recommend using a Cloud9 instance (hosted IDE) for the next steps, as it is bandwidth-friendly and helpful during troubleshooting!
> Cloud9 is free-tier eligible

Next, clone the git repository for this bootcamp:
```bash
git clone https://github.com/dixonaws/reinvent_cvra_bootcamp
```

You should now have a new directory, *reinvent_cvra_bootcamp* in your work direcrtory. Third, complete the 
worksheet below *or*, if you are on macOS/Cloud9, you can use a utility in the reinvent_cvra_bootcamp to
check versions and create worksheet (called worksheet.txt) for you:
```bash
chmod +x create_worksheet.sh
./create_worksheet.sh
```

<b>*** Now, you're ready to move on to Step 2 and deploy the Connected Vehicle Reference Architecture *** </b>

---

## 1. Deploy the CVRA (15 mins.)
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

<b>*** Now, you can move on to Step 2, Deploy the IoT Device Simulator ***</b>

---
 
## 2. Deploy the IoT Device Simulator and Generate Trip Data (30 mins.)
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

<b>*** At this point, you can move on to Step 3 and integrate with the Connected Vehicle Reference Architecture with Alexa ***</b>

---

## 3. Deploy the ConnectedCar Alexa Skill (20 mins.)
In this section, we'll deploy an Alexa skill called ConnectedCar that will read back information about 
the three recent trips that you have taken and details about your car.

### 3.1 Obtain App_id and App_code from developer.here.com
Head over to developer.here.com, establish an account, and make note of your app_code and app_id in your worksheet for this bootcamp. 

### 3.2 Run a Python Program to Test Your Permissions and CVRA Installation
First, you can use a Python program included with the reinvent_cvra_bootcamp repo, getRecentTrips.py, to 
test your configuration sofar. The best way to run this program is within a Python Virtual Environment. Install a Python 
virtual environment, install the dependencies from requirements.txt, and run get_recent_trips.py.

<details>
<summary><strong>Step-by-step instructions (expand for details)</strong></summary>
<p>
Install and activate Python virtual environment in ./venv (macOS):

```bash
virtualenv venv
source venv/bin/activate
```

Install dependencies (macOS):
```bash
pip install -r requirements.txt
```

Run the program:
```bash
python getRecentTrips.py --VehicleTripTable <TripTable> --HereAppId <app id> --HereAppCode <app code>
```

Or, if you wanted to be very clever using your <i>ninja bash skills</i>, you could do something like this on the bash prompt: 

```bash
python3 getRecentTrips.py --VehicleTripTable `aws cloudformation describe-stacks --stack-name cvra-demo --output table --query 'Stacks[*].Outputs[*]' |grep 'Vehicle Trip table' |awk -F "|" '{print $4}'` --HereAppId <app id> --HereAppCode <app code>
```
> Quote trifecta: Note the tricky combination of backticks, single quotes, AND double quotes!
</p>
</details>
<br>

You should see output similar to the following after running the program:
```json(venv) f45c898a35bf:reinventCvraBootcamp dixonaws$ python3 getRecentTrips.py --VehicleTripTable cvra-demo-VehicleTripTable-U0C6DSG0JW11
Scanning trip table cvra-demo-VehicleTripTable-U0C6DSG0JW11... done (0).
Found 18 items in the trip table.
dictItems is a <class 'list'>
**** Trip 1 (VIN: 2Z61V6JISOE60EWI8)
{'ignition_status': {'S': 'off'}, 'transmission_gear_position': {'S': 'fourth'}, 'engine_speed_mean': {'N': '3525.2780709525855'}, 'name': {'S': 'aggregated_telemetrics'}, 'driver_safety_score': {'N': '74.82328344340092'}, 'brake_mean': {'N': '0'}, 'high_braking_event': {'N': '0'}, 'fuel_level': {'N': '99.95453355436261'}, 'latitude': {'N': '38.958911'}, 'idle_duration': {'N': '213'}, 'fuel_consumed_since_restart': {'N': '0.019374198537822133'}, 'torque_at_transmission_mean': {'N': '314.3124901722019'}, 'timestamp': {'S': '2018-08-21 23:13:01.589000000'}, 'vehicle_speed_mean': {'N': '79.9034721171209'}, 'start_time': {'S': '2018-08-21T23:12:31.456Z'}, 'end_time': {'S': '2018-08-21T23:13:01.589Z'}, 'trip_id': {'S': '84983a6b-0881-4600-ad20-9db40eb7f868'}, 'oil_temp_mean': {'N': '29.021054075000006'}, 'geojson': {'M': {'bucket': {'S': 'connected-vehicle-trip-us-east-1-477157386854'}, 'key': {'S': 'trip/2Z61V6JISOE60EWI8/84983a6b-0881-4600-ad20-9db40eb7f868.json'}}}, 'accelerator_pedal_position_mean': {'N': '38.609446258882855'}, 'longitude': {'N': '-77.401168'}, 'vin': {'S': '2Z61V6JISOE60EWI8'}, 'brake_pedal_status': {'BOOL': False}, 'high_speed_duration': {'N': '0'}, 'odometer': {'N': '0.6705392939350361'}, 'high_acceleration_event': {'N': '2'}}
...

```

The get_recent_trips.py program simply queries your DynamoDB trip table, which is similar to the ConnectedCar skill that 
we'll deploy in the next section.
<details>
<summary><strong>Code details for getRecentTrips.py (expand for details)</strong></summary>
Have a look at the code listing for getRecentTrips.py. The guts 
are similar to the ConnectedCar skill that we'll deploy in the next
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
> You may even elect to create an API layer in front of the 
> DynamoDB table so that other applications can use the 
> data.
</details>


### 3.3 Deploy the Alexa Skill
In ths step, you'll use the trip data recorded in your DynamoDB table with an Alexa skill called ConnectedCar. First, you'll
need to create an account on developer.amazon.com if you haven't already done so.

Once you have confirmed that your DynamoDB Trip table contains trip data with getRecentTrips.py, follow these instructions 
to create a new *custom* skill called "ConnectedCar" in your developer.amazon.com account: [Alexa Skills Kit Documentation](https://developer.amazon.com/docs/devconsole/create-a-skill-and-choose-the-interaction-model.html)

Create the Intent Schema for your skill:
1. From the developer console, open your ConnectedCar skill
2. Under Interaction Model, click "JSON Editor"
3. Paste the contents of the intent_schema.json file into the JSON Editor for the skill
4. Click "Save Model"
<br>

#### 3.3.1 Create a Deployment Package for Your Lambda Function
You will need to create a deployment package, instructions here: https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/
Install the following dependencies in your ConnectedCarLambda directory:
requests
boto3

From within your ConnectedCarLambda directory, create a deployment package for your skill code with the following command:
```bash
zip -r ../ConnectedCarLambdaPackage.zip .
```

This command will create a deployment package in your reinvent_cvra_bootcamp directory. Use it in the next step to upload to Lambda.

Next, create the Lambda endpoint and Lambda function for your skill:
1. From the Alexa Developer Console, open the ConnectedCar skill
2. Under Interaction Model, click on "Endpoint"
3. Open a new browser window and navigate to the AWS Console
4. Create a new Lambda function called "ConnectedCarLambda" choosing "Author from scratch" and an existing role 
5. For "Code entry type" choose to upload a .zip file and use the deployment package that you create in the previous step 
6. For "Execution role", choose to create a new role and attach the AmazonDynamoDBReadOnlyAccess and AWSLambdaBasicExecution policies 
7. Modify the handler for the function to be ```ConnectedCarLambda.lambda_handler```
8. Create four environment variables in your Lambda function: VehicleTripTable, AppCode, and AppId, Region

<br>

Navigate back to the Alexa Developer Console, save and build your Alexa skill:
1. Copy the ARN of the "ConnectedCarLambda" function into the developer console endpoint field
2. From the ConnectedCar build page, click "Save Model"
3. Once saved, click "Build Model"
<br>

### 3.4 Interact with ConnectedCar
Open developer.amazon.com, login, and browse to your ConnectedCar Alexa Skill. Click on "Developer Console," and then "Alexa Skills Kit." You 
should be able to see the ConnectedCar skill that you deployed in the previous section. Open ConnectedCar and click 
on "Test" near the top of the page. You can use this console to interact with an Alexa skill without using a 
physical Echo device -- via text or via voice. Try these interactions:

```
"Alexa, open <your skill name>"

"Alexa, ask <your skill> about my car"

"Alexa, ask <your skill> about my trips"
```

You can also test via the command line with this command:
```bash
ask simulate --text "alexa, open <your skill>" --locale "en-US"
```

> Testing from the command line is handy for use in automated build pipelines 

---

## 4. Cleanup (10 mins.)
The last thing to do in this bootcamp is to clean up any resources that were deployed in your account. 
From your worksheet, delete the following Cloudformation stacks:
* Your CVRA Cloudformation stack
* Your vehicle simulator Cloudformation stack

Delete your Cloud9 instance if you created one.

```bash
aws cloudformation delete-stack --stack-name <your CVRA stack>
aws cloudformation delete-stack --stack-name <your vehicle simulator stack>
```

From the AWS console, ensure that any associated S3 buckets, DynamoDB tables, and IoT service is clean.

Also be sure to delete the following:
* The Lambda function for ConnectedCar
* The ConnectedCar skill from developer.amazon.com

---

## 5. Ideas for Customization and Enhancement
Hopefully, you were able to learn how to make use
of the data collected by a simulated connected vehicle (and ultimately any connected 
device). Here are some ideas to make enhancements and improvements from here:
* Enhance the Alexa skill to read values from many different cars 
* Adjust the IAM roles for more granular permissions
* Develop account linking for the ConnectedCar skill to read back information only for linked VINs
* Create an authenticated API to access the VehicleTripTable (API Gateway, Lambda, Cognito)
* Enhance the ConnectedCar Alexa skill to get the latest fuel prices in a certain location
* Connect to other public APIs to enhance your Alexa skill
* Create a deployment pipeline for your Alexa skill and Lambda function
* Deploy the CVRA solution with a real vehicle, using Greengrass and an OBDII interface!