import json
import os
import requests
import sys

# This called the ipstack API with the given data and returns the reponse
def get_location_api(ip_address, api_key):
    api_response=None
    try:
        endpoint = "http://api.ipstack.com/" + ip_address + "?access_key=" + api_key
        api_response = requests.get(endpoint)
    except Exception as e:
        print(f"API call failed with an exception: {str(e)}")

    return api_response

# Check the response from the API and handle appropriately
# Success should show the longitude and latitude
# Help should show usage info
# Failures should show an error
def evaluate_api_response(response_data):
    # Check if the "success" key is present and its value.
    # Note only a failure has the success data in the response
    # A successful call does not contain this.
    # Both scenarios respond with a 200 status code
    if "success" in response_data:
        if response_data["success"] == False:
            error_data = response_data.get("error", {})
            error_message = error_data.get("info", "Unknown error")
            print(f"API call was unsuccessful. Error: {error_message}")
    else:
        print("The location of the IP address given is: " + str(response_data['latitude']) + ", " + str(
            response_data['longitude']))

#This reads in the API key from a config file.  This is also not entirely secure
# because it is being checked into a public repository but it is better than hardcoding
# or putting onto command line where it will be read in history
# This should be placed somewhere more secure for continued usage like Docker secrets or a file vault
def read_api_key_from_config(file_path):
    try:
        with open(file_path, 'r') as config_file:
            config_data = json.load(config_file)
            api_key = config_data.get("api_key")
            if api_key:
                return api_key
            else:
                print("API key not found in the config file.")
                return None
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON in the config file.")
        return None

# Specify the path to your config file
config_file_path = "config.json"

# Read the API key from the config file
api_key = read_api_key_from_config(config_file_path)

if api_key:
    print("API Key found")
else:
    print("API key retrieval failed.")


# This Python script allows you to retrieve the location information for a given IP
# address using the IPStack API. It provides latitude and longitude
# coordinates for valid IP addresses.
def main():

    # File path can be changed.  Assuming all files in one location
    config_file_name = "config.json"
    config_file_path = os.path.join(os.getcwd(), config_file_name)
    api_key= read_api_key_from_config(config_file_path)

    #Check for arguments and handle appropriately
    if len(sys.argv) != 2:
        print("Usage: python3 ipstack.py <Valid IP Address>")
    elif sys.argv[1]== "--help":
        print("Usage: python3 ipstack.py <Valid IP Address>")
    else:
        ip_address = sys.argv[1]
        response = get_location_api(ip_address, api_key)
        if response != None:
            evaluate_api_response(response.json())


if __name__ == "__main__":

    main()