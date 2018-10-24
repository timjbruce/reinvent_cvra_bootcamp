# Overview
This part of the lab will build the additional components to store trip data and provide a Fleet Admin dashboard.

## Step 1 - Create DynamoDB Tables, Lambda Function and update an IoT Rule
The following steps will guide you through creating two new DynamoDB tables, a Lambda function with the required IAM Role and Policy. Then we will update an IoT rules created by the CVRA CloudFormation template to store trip telemetry and route data into the new tables.

### Create the DynamoDB tables.
From the Console create 2 new DynamoDB tables. You can either use your own schema or the suggested on below.

- Table Name **vehicleTelemetryTable** Primary Key **vin** type **string**
- Table Name **vehicleRouteTable** Primary Key **trip_id** type **string**

### Create a new Lamdba Function with the required permissions

The *Role* for the **Lambda** function will need access to the two new DynamoDB tables.

You can use the below policy if required.

```json
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "dynamodb:PutItem",
                  "dynamodb:UpdateItem"
              ],
              "Resource": [
                  "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/vehicleTelemetryTable",
                  "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/vehicleRouteTable"
              ]
          }
      ]
  }
  ```
> Make sure you replace REGION and ACCOUNT_ID with your relevant information.


Create a new Lambda Function and add it as an action to the IoT **VehicleTelemetryStorage** rule.

Copy and paste the below code into the Function.

```javascript
'use strict';
console.log('Loading function');
const aws = require('aws-sdk');
aws.config.update({region: 'us-east-1'});
const docClient = new aws.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});

exports.handler = (event, context, callback) => {
    console.log(JSON.stringify(event, null, 2));
    var vin_val = event['vin'];
    var last_update_val = event['timestamp'];
    var trip_id_val = event['trip_id'];
    var attr_name = event['name'];
    var attr_val = event['value'];

    // Set the table name
    var table = "vehicleTelemetryTable";

    var updexp = "set last_updated=:lu, trip_id=:ti, #attrName=:an";
    var params = {
        TableName:table,
        Key:{
            "vin": vin_val
        },
        UpdateExpression: updexp,
        ExpressionAttributeNames: {
            "#attrName" : attr_name
        },
        ExpressionAttributeValues: {
            ":lu":last_update_val,
            ":ti":trip_id_val,
            ":an":attr_val
        },
        ReturnValues:"UPDATED_NEW"
    };
    console.log(params)
    console.log("Updating the item...");
    docClient.update(params, function(err, data) {
        if (err) {
            console.error("Unable to update item. Error JSON:", JSON.stringify(err, null, 2));
        } else {
            console.log("UpdateItem succeeded:", JSON.stringify(data, null, 2));
        }
    });

    //Store Location
    if (attr_name == "location" ){
      // Set the table name
      var table = "vehicleRouteTable";
      var updexp = "set #rt = list_append(if_not_exists(#rt, :empty_list), :rt)";
      var params = {
        TableName:table,
        Key:{
          "trip_id": trip_id_val
        },
        UpdateExpression: updexp,
        ExpressionAttributeNames: {
            "#rt": "route"
        },
        ExpressionAttributeValues: {
          ":rt": [attr_val],
          ":empty_list": []
        },
        ReturnValues:"UPDATED_NEW"
      };
      console.log("Adding Route to Trip");
      docClient.update(params, function(err, data) {
          if (err) {
              console.error("Unable to update route. Error JSON:", JSON.stringify(err, null, 2));
          } else {
              console.log("Update Route Successfully:", JSON.stringify(data, null, 2));
          }
      });
    }
};
```

## Step 2 - Run some vehicle simulations

Log into the IoT Device Simulator using the credentials and instructions you got in your the Email.
1. Click on "Settings" in the left hand menu and input your Mapbox API token into the dialog box and click Save
2. Click on "Automotive" on the left hand menu.
3. Click on "+ Add Vehicle"
4. Choose 5 and click submit

The simulator will now run 5 route simulations.

## Step 3 - View the Routes

Once the Simulations have completed, via the console look at the Telemetry and Routes tables.

*Additional Instruction will be added to build and deploy the Fleet Management UI*
