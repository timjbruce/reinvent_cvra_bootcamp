Install the ASK CLI on your Cloud9 instance with the following command:
```bash
npm install ask-cli -g
```

Now, initialize the ASK CLI by issuing ```ask init --no-browser``` at the bash prompt.

<details>
<summary><strong>Initialize the ASK CLI (expand for details)</strong></summary>

Issue the following command:
```bash
ask init --no-browser
```

You should now see this screen in the command prompt. This step isused to select your AWS profile. Choose the default profile.
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


------

he AWS CLI is already installed on Cloud9, so we just need to configure it with permanent credentials. This is needed for compatibility
with the ASK CLI that we'll install later.

<details>
<summary><strong>Detailed instructions to configure Cloud9 to use permenent credentials (expand for details)</strong></summary>

1. Launch Cloud9
2. Open Cloud9 Preferences by clicking AWS Cloud9 > Preference or by clicking on the "gear" icon in the upper right corner of the Cloud9 window
3. Click "AWS Settings"
4. Disable "AWS managed temporary credentials" 
5. Open a bash prompt and type ```aws configure```
6. Enter the Access Key and Secret Access Key of a user that has AdministratorAccess credentials

Verify that everything worked by examining the file ```~/.aws/credentials```. It should resemble the following:
```bash
[default]
aws_access_key_id = ABCDEF1234567890
aws_secret_access_key = 2bacnfjjui689fwjek100009909922h
region=us-east-1
aws_session_token=
```

You should now be able to run AWS CLI commands using the credentials on your Cloud9 instance. For example run the following
command from Cloud9's bash prompt:
```bash
aws s3 ls
```

...should return a list of the S3 buckets in your account.

</details>