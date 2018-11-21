## 3. Deploy the ConnectedCar Alexa Skill (20 mins.)
In this section, we'll deploy an Alexa skill called ConnectedCar that will read back information about
the three recent trips that you have taken and details about your car.

> Perform the following steps from within the AlexaSkill folder in your downloaded copy of the reinvent_cvra_bootcamp
repository.

> You'll need to install the ASK CLI (Alexa Skills Kit CLI) in this section

> You'll need Node v8.1.0 for this section

### 3.1 Obtain App_id and App_code from the HERE dveeloper site
Head over to https://aws.amazon.com/marketplace/pp/B07JPLG9SR, establish a freemium account, and 
make note of your app_code and app_id in your worksheet for this bootcamp.

### 3.2 Run a Program to Test Your Permissions and CVRA Installation
First, you can use a Node program included with the reinvent_cvra_bootcamp repo to
test your configuration. GetRecentTrips.js is a Node v8.1.0 program that is similar to the 
Alexa Lambda function -- it scans your VehicleTripTable for recent trips, then queries HERE APIs for 
the neighborhood that matches the GPS location of the trip. Instead of speaking the results, this 
program prints them to the console.

Instructions:
1. Descend into the AlexaSkill/GetRecentTrips directory
2. Install dependencies with ```npm install```
3. Run the program with the following command:
 
```bash
node GetRecentTrips.js --app_id=x --app_code=y --vehicle_trip_table=z
```

Or, if you wanted to be clever using your <i>bash ninja skills</i>, you could do something like this on the bash prompt:

```bash
node GetRecentTrips.js --tableName=`echo $(aws cloudformation describe-stacks --stack-name cvra-demo --output table --query 'Stacks[*].Outputs[*]' |grep 'Vehicle Trip table' |awk -F '|' '{print $4}')` --appCode=<your_app_code> --appId=<your_app_id>
```
> bash ninjas will note the tricky combination of backticks and single quotes!

You should see output similar to the following:

```
GetRecentTrips v1.0
-----------------------------------------
Scanning DynamoDB VehicleTripTable for trips...
Scan succeeded, 8 trips found.
Your 3 most recent trips were: 
vin: 9JVVV63E5NVZWH5UH, start time: 2018-11-20T17:46:43.608Z, distance: 10.2, neighborhood: Reston, VA, United States
vin: 2Z61V6JISOE60EWI8, start time: 2018-10-28T18:34:41.432Z, distance: 0.0, neighborhood: Herndon, VA, United States
vin: 9JVVV63E5NVZWH5UH, start time: 2018-10-17T01:00:09.695Z, distance: 228.0, neighborhood: Eisenhower East, Alexandria, VA, United States
```



### 3.3 Deploy the Alexa Skill
In ths step, you'll use the trip data recorded in your DynamoDB table with an Alexa skill called ConnectedCar. 
First, you'll need to create an account on developer.amazon.com if you haven't already done so.

Once you have confirmed that your DynamoDB Trip table contains trip data with the GetRecentTrips.js program,
follow these instructions to create a new skill using the ASK CLI. 

// todo: add ASK CLI instructions

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
