# For library dashboard 
import json 
import secrets 
import requests

# Destination, replace with CHFS
patroninfo = open("patroninfo.json", "w")

def get_token():
    url = "https://catalog.chapelhillpubliclibrary.org/iii/sierra-api/v4/token"
    # Get the API key from secrets.py
    header = {"Authorization": "Basic " + str(secrets.sierra_api), "Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=header)
    json_response = json.loads(response.text)
    print(json_response)
    # Create var to hold the response data
    active_patrons_token = json_response["access_token"]
    return active_patrons_token

# Function that creates json file of patron IDs
def get_activepatrons():
    
    savefile = open("patronids.json","w")
    
    header_text = {"Authorization": "Bearer " + get_token()}
    patron_id_url = "https://catalog.chapelhillpubliclibrary.org:443/iii/sierra-api/v4/patrons/?fields=id&deleted=false"
    
    i = 0
    loop = True
    while loop == True:
        
        #Test
        print(i)
    
        request = requests.get(patron_id_url, header_text)
    
        # Stop looping when the requests sends an error code/doesn't connect
        if request.status_code != 200:
            break
        elif i != 0:
            # adds a comma and newline for better organization and format
            savefile.write(',\n')
        
        # Counter to find slice start point 
        counter = 1
        for letter in request.text:
            if letter == '[':
                break
            counter += 1
            
        # Slice off the beginning and ends of json to allow for combining all data
        sliced_json = request.text[counter:-2]
    
        # Write data to patron json file 
        savefile.write(sliced_json)
        # Increment i 
        i = i + 2000
    savefile.close()
    return savefile
    
def get_checkout_info():
    patron_ids = get_activepatrons()
    print(patron_ids.keys())
    header_text = {"Authorization": "Bearer " + get_token()}
    checkout_url = "https://catalog.chapelhillpubliclibrary.org:443/iii/sierra-api/v4/patrons/" + i + "/checkouts?fields=dueDate%2CnumberOfRenewals"
    checkouts = requests.get(checkout_url, headers=header_text)
    print(checkouts)
    
def get_patron_info(): 
    patron_info_url = "https://catalog.chapelhillpubliclibrary.org:443/iii/sierra-api/v4/patrons/?fields=blockInfo,patronType,birthDate&deleted=false"
    header_text = {"Authorization": "Bearer " + get_token()}
    patron_info = requests.get(patron_info_url, headers=header_text)
    
def main():
    # Create final file to combine all info into 
    final_file = open("patroninformation.json", "w")
    # Call functions to get info
    checkout_info = get_checkout_info()
    patron_info = get_patron_info()
    final_file.write(checkout_info)
    final_file.write(patron_info)
