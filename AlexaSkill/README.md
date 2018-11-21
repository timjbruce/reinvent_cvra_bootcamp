## 3. Deploy the ConnectedCar Alexa Skill (20 mins.)
In this section, we'll deploy an Alexa skill called ConnectedCar that will read back information about
the three recent trips that you have taken and details about your car.

### 3.1 Obtain App_id and App_code from the HERE dveeloper site
Head over to https://aws.amazon.com/marketplace/pp/B07JPLG9SR, establish a freemium account, and make note of your app_code and app_id in your worksheet for this bootcamp.

### 3.2 Run a Python Program to Test Your Permissions and CVRA Installation
First, you can use a Python program included with the reinvent_cvra_bootcamp repo, getRecentTrips.py, to
test your configuration sofar. The best way to run this program is within a Python Virtual Environment. Install a Python
virtual environment, install the dependencies from requirements.txt, and run get_recent_trips.py.

<details>
<summary><strong>Step-by-step instructions (expand for details)</strong></summary>
<p>
Install and activate Python virtual environment in ./venv:

```bash
virtualenv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the program:
```bash
python3 get_recent_trips.py --VehicleTripTable <TripTable> --HereAppId <app id> --HereAppCode <app code>
```

Or, if you wanted to be very clever using your <i>bash ninja warrior skills</i>, you could do something like this on the bash prompt:

```bash
python3 getRecentTrips.py --VehicleTripTable `aws cloudformation describe-stacks --stack-name cvra-demo --output table --query 'Stacks[*].Outputs[*]' |grep 'Vehicle Trip table' |awk -F "|" '{print $4}'` --HereAppId <app id> --HereAppCode <app code>
```
> Quote trifecta: bash ninjas will note the tricky combination of backticks, single quotes, AND double quotes!
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
You will need to create a deployment package, instructions here: [Build an AWS Lambda Deployment Package for Python](https://aws.amazon.com/premiumsupport/knowledge-center/build-python-lambda-deployment-package/).
Install the following dependencies in your ConnectedCarLambda directory:
* requests
* boto3

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
6. For "Execution role", choose to create a new role and attach the following policies
* AmazonDynamoDBReadOnlyAccess
* AWSLambdaBasicExecution
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
