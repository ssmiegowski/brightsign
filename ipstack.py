import json
import os
import requests
import sys
import keyring


# This called the ipstack API with the given data and returns the reponse
def get_location_api(ip_address, api_key):
    api_response = None
    try:
        endpoint = "http://api.ipstack.com/" + ip_address + "?access_key=" + api_key
        api_response = requests.get(endpoint)
    except Exception as e:
        print(f"API URL assembly failed with an exception: {str(e)}")

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

# Set the API key securely using keyring
def set_api_key(api_key):
    keyring.set_password("ipstack-api", "bestuserever", api_key)
    pass

# Retrieve the API key securely using keyring
def get_api_key():
    api_key_temp = keyring.get_password("ipstack-api", "bestuserever")
    return api_key_temp

# This reads in the API key from a config file.  This is also not entirely secure
# because it is being checked into a public repository but in practice the config file should be
# empty and filled in by the user.
# It is prepopulated for the sake of this test so that it runs upon pulling.
# you could also have the user log in and scrape https://ipstack.com/dashboard using beautiful soup
# This should then be placed somewhere more secure for continued usage like Docker secrets, keyring
# or a file vault
# You could also turn it into a system variable and read that in
def read_api_key_from_config(file_path):

    try:
        with open(file_path, 'r') as config_file:
            config_data = json.load(config_file)
            api_data = config_data.get("api_key")
            if api_data:
                # Set the API key securely using keyring
                set_api_key(api_data)
            else:
                print("API key not found in the config file.")
                return None
    except FileNotFoundError:
        print("Config file not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON in the config file.")
        return None

# This Python script allows you to retrieve the location information for a given IP
# address using the IPStack API. It provides latitude and longitude
# coordinates for valid IP addresses.
def main():
    # File path can be changed.  Assuming all files in one location
    config_file_name = "config.json"
    config_file_path = os.path.join(os.getcwd(), config_file_name)
    read_api_key_from_config(config_file_path)

    # Config file should have a dummy value for API key and be filled in by user in normal situations
    api_key_real = get_api_key()
    if not api_key_real:
         print("API key retrieval failed.")

    # Check for arguments and handle appropriately
    if len(sys.argv) != 2:
        print("Usage: python3 ipstack.py <Valid IP Address>")
    elif sys.argv[1] == "--help":
        print("Usage: python3 ipstack.py <Valid IP Address>")
    else:
        ip_address = sys.argv[1]
        response = get_location_api(ip_address, api_key_real)
        if response != None:
            evaluate_api_response(response.json())

    #Try to delete password if it exists
    try:
        keyring.delete_password("ipstack-api", "bestuserever")
    except Exception as e:
        print("Password deletion failed")

#Token main
if __name__ == "__main__":
    main()
