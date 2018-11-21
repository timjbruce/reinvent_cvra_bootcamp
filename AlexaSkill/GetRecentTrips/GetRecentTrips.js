'use strict';

const AWS = require('aws-sdk');
const fetch = require('node-fetch');
const args = require('yargs').argv;

function GetTripDetails(appId, appCode, tableName) {
    AWS.config.update({
        region: "us-east-1"
    });

    var docClient = new AWS.DynamoDB.DocumentClient();

    console.log("Scanning DynamoDB VehicleTripTable for trips...");

    var params = {
        TableName: tableName
    };

    docClient.scan(params, onScan);

    async function onScan(err, data) {
        if (err) {
            console.error("Unable to scan the table. Error:", JSON.stringify(err, null, 2));
            return;
        }

        // print trip info
        console.log("Scan succeeded, " + data.Count + " trips found.");

        // sort the trip by start_time, most recent first
        var trips = data.Items;
        trips.sort(function(a, b) {
            return (b.start_time > a.start_time);
        });

        // print the 3 most recent trips
        console.log("Your 3 most recent trips were: ");
        var url; // url to call HERE Maps reverse geocoder API
        var i = 0; // index of the trip
        var response; // response from HERE Maps API
        var data; // encoded response
        var locationData; // JSON response
        var latitude;
        var longitude;
        var neighborhood; // neighborhood string extracted from response

        for (i = 0; i < 3; i++) {
            latitude = trips[i].latitude;
            longitude = trips[i].longitude;

            url = "https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?app_id=" + appId + "&app_code=" + appCode + "&mode=retrieveAreas&prox=" + latitude + "," + longitude;
            response = await fetch(url);
            locationData = await (response.json());
            neighborhood = locationData.Response.View[0].Result[0].Location.Address.Label;

            console.log("vin: " + trips[i].vin + ", start time: " + trips[i].start_time + ", distance: " + (trips[i].odometer).toFixed(1) + ", neighborhood: " + neighborhood);

        } // for(i)
    } // async onScan()
} // GetTripDetails()

function main() {
    console.log('GetRecentTrips v1.0');
    console.log("-----------------------------------------");

    const appId = args.appId;
    const appCode = args.appCode;
    const tableName = args.tableName;

    console.log('HERE app_id: ' + appId);
    console.log('HERE app_code: ' + appCode);
    console.log('VehicleTripTable: ' + tableName);

    GetTripDetails(appId, appCode, tableName);

} // main

main();
