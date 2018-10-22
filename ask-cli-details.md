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
