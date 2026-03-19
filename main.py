import json
from datetime import datetime


# convert json data from format 1 to the expected format
def convertFromFormat1(jsonObject):

    # split location string into parts
    locationParts = jsonObject['location'].split('/')

    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],
        "location": {
            "country": locationParts[0],
            "city": locationParts[1],
            "area": locationParts[2],
            "factory": locationParts[3],
            "section": locationParts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }

    return result


# convert json data from format 2 to the expected format
def convertFromFormat2(jsonObject):

    # convert ISO timestamp to milliseconds since epoch
    dt = datetime.strptime(jsonObject["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch = datetime(1970, 1, 1)
    timestamp_ms = int((dt - epoch).total_seconds() * 1000)

    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp_ms,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"]
        }
    }

    return result


# main function to detect format
def main(jsonObject):

    if "device" in jsonObject:
        return convertFromFormat2(jsonObject)
    else:
        return convertFromFormat1(jsonObject)


# ------------------ TESTING ------------------

if __name__ == "__main__":

    # sample test (optional)
    sample1 = {
        "deviceID": "dh28dslkja",
        "deviceType": "LaserCutter",
        "timestamp": 1624445837783,
        "location": "japan/tokyo/keiyo-industrial-zone/daikibo-factory-meiyo/section-1",
        "operationStatus": "healthy",
        "temp": 22
    }

    print(json.dumps(main(sample1), indent=2))
