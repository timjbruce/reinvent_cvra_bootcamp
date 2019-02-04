## 3. Deploy the ConnectedCar Alexa Skill (20 mins.)
In this section, we'll deploy an Alexa skill called ConnectedCar that will read back information about
the three recent trips that you have taken.

> Perform the following steps from within the ```AlexaSkill``` folder in your downloaded copy of the ```reinvent_cvra_bootcamp```
repository. If you haven't already, run ```git clone https://github.com/dixonaws/reinvent_cvra_bootcamp``` in your Cloud9 environment

> We'll be using us-east-1 (N Virginia) for this section

1. The AWS CLI is already installed on Cloud9, but is configured to use the EC2 instance role. For compatibility with the ASK CLI,
we need to configure it with permanent credentials.

<details>
<summary><strong>Detailed instructions to configure Cloud9 to use permenent credentials (expand for details)</strong></summary>

1. Open Cloud9 Preferences by clicking AWS Cloud9 > Preference or by clicking on the "gear" icon in the upper right corner of the Cloud9 window
2. Click "AWS Settings"
3. Disable "AWS managed temporary credentials" 
4. Open a bash prompt and type ```aws configure```
5. Enter the Access Key and Secret Access Key of a user that has AdministratorAccess credentials
6. Be sure to enter ```us-east-1``` as the region

Verify that everything worked by examining the file ```~/.aws/credentials```. It should resemble the following:
```bash
[default]
aws_access_key_id = ABCDEF1234567890
aws_secret_access_key = 2bacnfjjui689fwjek100009909922h
region=us-east-1
aws_session_token=
```

*Remove the ```aws_session_token``` line from your credentials file.

You should now be able to run AWS CLI commands using the credentials on your Cloud9 instance. For example run the following
command from Cloud9's bash prompt:
```bash
aws s3 ls
```

...should return a list of the S3 buckets in your account.

</details>
<br>

4. Install and activate Node v8.1.4 in your Cloud9 environment
```bash
nvm install v8.1.4
```

>Note: Node v8.1.0 has a specific compatibility problem with the ASK CLI

------

### 3.1 Obtain an App_id and App_code from the HERE developer site
Head over to https://aws.amazon.com/marketplace/pp/B07JPLG9SR, establish a freemium account, and 
make note of your app_code and app_id in your worksheet for this session.

### 3.2 Run a Program to Test Your Permissions and CVRA Installation
First, you can use a Node program included with the reinvent_cvra_bootcamp repo to
test your configuration. GetRecentTrips.js is a Node v8 program that is similar to the 
Alexa Lambda function -- it scans your VehicleTripTable for recent trips, then queries HERE APIs for 
the neighborhood that matches the GPS location of the trip. Instead of speaking the results, this 
program prints them to the console.

Instructions:
1. Descend into the reinvent_cvra_bootcamp/AlexaSkill/GetRecentTrips directory
2. Install dependencies with ```npm install```
3. Run the program with the following command:
 
```bash
node GetRecentTrips.js --appId=<your_app_id> --appCode=<your_app_code> --tableName=<your_vehicle_trip_table>
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

> Note: if you get an error when running this program "The security token included in the request is 
invalid," then have a look at your ~/.aws/credentials file and ensure that ```aws_session_token``` is 
not present.


### 3.3 Deploy the Alexa Skill
In step 3.2, you confirmed that your DynamoDB Trip table contains trip data,
that you have HERE credentials setup properly, and that your AWS permissions are ok. In ths 
step, you'll use the trip data recorded in your DynamoDB table with an Alexa 
skill called ConnectedCar. Follow these instructions to create a new skill using the ASK CLI. 
1. Install the ASK CLI (from the base Cloud9 directory)
```bash
npm install ask-cli --global
```

2. Initialize the ASK CLI by issuing the following command:
```bash
ask init --no-browser
``` 

<details>
<summary><strong>Initialize the ASK CLI (expand for details)</strong></summary>

Issue the following command:
```bash
ask init --no-browser
```

You should now see this screen in the command prompt. This step is used to select your AWS profile. Choose the default profile.
```bash
dixonaws:/environment$ ask init
? Please create a new profile or overwrite the existing profile.
 (Use arrow keys)
  ──────────────
❯ Create new profile 
  ──────────────
  Profile              Associated AWS Profile
  [default]                 "default" 

```

Next, you'll see the following screen to select the AWS profile to use for Lambda function deployment. Choose default:
```bash
? Please create a new profile or overwrite the existing profile.
 [default]                 "default"
-------------------- Initialize CLI --------------------
Setting up ask profile: [default]
? Please choose one from the following AWS profiles for skill's Lambda function deployment.
 
❯ default  
  ──────────────
  Skip AWS credential for ask-cli. 
  Use the AWS environment variables. 
  ──────────────


```

Next, you'll see a URL listed. You must use this URL to login to the developer console and obtain an Authorization Code. 
 
```bash
Paste the following url to your browser:
         https://www.amazon.com/ap/oa?redirect_uri=https%3A%2F%2Fs3.amazonaws.com%2Fask-cli%2Fresponse_parser.html&scope=alexa%3A%3Aask%3Askills%3Areadwrite%20alexa%3A%3Aask%3Amodels%3Areadwrite%20alexa%3A%3Aask%3Askills%3Atest&state=Ask-SkillModel-ReadWrite&response_type=code&client_id=amzn1.application-oa2-client.aadxxxxxxxxb44bac56

? Please enter the Authorization Code:  
```

If all goes well, you should see this on the command prompt:
```bash
? Please create a new profile or overwrite the existing profile.
 [default]                 "default"
-------------------- Initialize CLI --------------------
Setting up ask profile: [default]
? Please choose one from the following AWS profiles for skill's Lambda function deployment.
 default
Switch to 'Login with Amazon' page...
Tokens fetched and recorded in ask-cli config.
Vendor ID set as XXXXXXXXXX

Profile [default] initialized successfully.
 
```

</details>
<br>


3. Run the following command from the AlexaSkill directory to create a new "hello world" skill with the ASK CLI<br>
```ask new --skill-name "amt303"```

> Note: the skill name will be "amt303," but we will modify the *invocation name* in a later step 

Choose the following:
- Runtime: Node.js V8
- Template: "Hello World" (naturally)

This command will create a new directory called ```amt303```. The default invocation 
name for this skill is "hello world," which we'll change later.

4. Deploy the amt303 skill<br>
Run the following command from the amt303 directory:
```
ask deploy
```
If all goes well, this command will do two things: a) create a new skill in developer.amazon.com called ```amt303```, and 
b) creates a new Lambda function called ```ask-custom-amt303```.

5. Test invocation of the amt303 skill<br>
Open developer.amazon.com, navigate to the ```amt303 skill```, navigate to the test tab, and test 
with "alexa, open hello world." Alternatively, you can test from the command line 
with ```ask dialog --locale "en-US"```

6. Change the invocation name of the skill to "connected car"<br>
From your Cloud9 interface, open ```AlexaSkill/amt303/models/en-US.json``` and change the ```interactionModel.languageModel.invocationName```. Redeploy and test
the skill with ```ask deploy``` and test again from the console or command line.

7. Update the Lambda function code and deploy again<br>
Our Lambda function requires the ```node-fetch library```, so enter 
the ```AlexaSkill/amt303/lambda/custom``` directory and install it with ```npm install node-fetch --save```
You'll also need to update the Lambda function code. Replace the contents of ```AlexaSkill/amt303/lambda/custom/index.js```
with the program from ```AlexaSkill/ConnectedCarLambda.js```. Execute another deployment.

8. Update the IAM role for the Alexa Lambda<br>
If you have named your Alexa skill "amt303," then you should have a Lambda function named 
```ask-custom-amt303```, and an
IAM role called ask-lambda-amt303. Add the ```AmazonDynamoDBReadOnlyAccess``` policy to the 
```ask-lambda-amt303``` role.

9. Update the Lambda function with environment variables<br>
Browse to your AWS Console and open the Lambda service. Open your ```ask-custom-amt303```
Lambda function. Create three environment variables with values corresponding to the values in your 
worksheet:<br>
a. appId<br>
b. appCode<br>
c. tableName<br>
<br>

Next, from Cloud9, do another deployment with ASK CLI:

```bash
ask deploy --target lambda --force
```

> By default, the The ASK CLI updates both the intent schema for the Alexa skill as well as the supporting Lambda function. You can
> choose to update them independently by specifying the --target parameter. 

At this point, the Alexa skill should be functional. If you launch it with "Alexa, Open Connected Car," then you should be able to 
hear information about your most recent trips. 

### 3.4 Interact with ConnectedCar
Open developer.amazon.com, login, and browse to your amt303 Alexa Skill. Click on "Developer Console," and then "Alexa Skills Kit." You
should be able to see the amt303 skill that you deployed in the previous section. Open amt303 and click
on "Test" near the top of the page. You can use this console to interact with an Alexa skill without using a
physical Echo device -- via text or via voice. Try these interactions:

> Note: due to the nature of the Alexa Voice Service, you may need to disable/re-enable testing for the skill
> using the slider at the top left of the testing console. Try this step if you recieve errors or unexpected 
> results when testing the skill.

```
"Alexa, open Connected Car"
```

You can also test via the command line with this command:
```bash
ask dialog --locale "en-US"
```

> Testing from the command line is useful for use in automated build pipelines, particularly the 'replay'
> parameter; see this link for documentation
> https://developer.amazon.com/docs/smapi/ask-cli-command-reference.html#dialog-command

This section is intended to demonstrate the integration of connected vehicle data with other services. We chose to integrate with
Alexa and HERE Maps because they are familiar and convenient with the ASK CLI. Of course, once your connected vehicle data is in AWS (DynamoDB in this case),
then you could similarly integrate with a variety of other services.