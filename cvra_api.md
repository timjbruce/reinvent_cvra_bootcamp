# Overview of Connected Vehicle Reference Architecture API #

There is an API that is included withe the Connected Vehicle Reference Archtitecture.  The API is setup to allow a vehicle owner to access their vehicle's data on the platform.  This is what we will focus on.

The API could be modified, fairly easily, to allow for a number of data access use cases.  If you are interested in exploring these options, you can [find the source code in github](https://github.com/awslabs/aws-connected-vehicle-solution).

## API Structure ##

The API uses the following structure:

* /vehicles
    * /{vin}
        * /anomalies
            * /{anomaly_id}
        * /dtc
            * /{dtc_id}
        * /healthreports
            * /{healthreportid}
        * /trip
            * /{tripid}

All support GET.  /vehicles/{vin}, /anomalies/{anomaly_id}, and /dtc/{dtc_id} support PUT in addition to GET.

More detials on the API can be found in the [Connected Vehicle Reference Architecture documentation](https://docs.aws.amazon.com/solutions/latest/connected-vehicle-solution/appendix.html).

This API, as it is built, is meant to secure the data in the CVRA tables.  As such, users will need to authenticate and have appropriate permissions to perform this task. These steps below will walk through the setup that is needed to setup the authentication and permissions first and then demonstrate the API.

## Setting Up Authentication and Permissions ##

:exclamation: It is important that you do this step *after* starting the IoT Device Simulator to put some vehicle data in the tables.  The tables use VIN as a part of the key and a valid VIN will help provide a better result.

1. Get a VIN from your Connected Car Trip Table

a) From the console, navigate to DynamoDB.
b) Click on "Tables" in the Navigation.
c) The Connected Car Trip Table's name begins with "cvra-VehicleTripTable-".  Find this table and click on it.
d) Click on the "Items" tab to display the records in it.
e) Copy any of the VINs from this table.

2. Add an Owner Record

a) Continuing from Step 1, click on the Vehicle Owner Table.  This table begins with "cvra-VehicleOwnerTable-".
b) Click the "Create Item" button.
c) Add in a record using your first name with all lower case letters as the "owner_id" and the VIN from step 1 as the vin
d) Click "Save"

Your record should now appear in the Items view for your Owners Table.

3. Modify the Cognito User Pool

a) From the console, navigate to "Cognito"
b) Click on "Manage User Pools"
c) Click on "connected_vehicle_user_pool"
d) Copy your "Pool ID" at the top of the page.  You will need this for a later step.
e) Click on "App Clients" on the left hand navigation.
f) Click the "Show Details" button.
g) Check the "Enable sign-in API for server-based authentication (ADMIN_NO_SRP_AUTH)" box.
h) Copy the "App Client Id" from the page.  You will need this for a later step.
i) Click the "Save app client changes" button.

4. Add Your User

a) Continuing from Step 3, click the "Users and Group" item on the left hand navigation.
b) Click the "Create User" button.
c) Enter your first name in lower case letters for the "Username".  This must match the owner_id from step 2.
d) Uncheck "Send an invitation to this new user?"
e) Enter your "Temporary Password," "Phone Number," and "Email"
f) Click "Create User"

At this point we are now ready to use the API that is provided by the Connected Vehicle Reference Architecture.

## Demonstrating API ##

We will be using the command line in your Cloud9 environment

1.  Authenticating

The first step to use the 