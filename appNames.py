import urllib2
import re
import json


def apn_application_id_to_name(application_id):
    
    #do a regex match for each of the ID's
    android_id_match = re.search('^com\..*?\..*$', application_id)
    windows_id_match = re.search('^[0-f]{8}-([0-f]{4}-){3}[0-f]{12}$', application_id)
    itunes_id_match = re.search('^[0-9]{9}$', application_id)
    
    #dCall the function to get the app name depending on the format of the ID
    if android_id_match:
        application_name = get_android_app_name(application_id)
    elif windows_id_match:
        application_name = get_windows_app_name(application_id)
    elif itunes_id_match:
        application_name = get_ios_app_name(application_id)
    elif application_id == "--":
        application_name == "--"
    else:
        application_name = "Not Found"

    print application_name

def get_android_app_name(application_id):
    
    #set the google play URL with the application_id
    google_play_url = "https://play.google.com/store/apps/details?id=" + application_id

    #get the HTML of the google play store URL
    response = urllib2.urlopen(google_play_url).read()

    #regEx the page to search for the App Name
    app_name = re.findall(r'<div class="document-title" itemprop="name"> <div>(.*?)</div> </div>', response)
    
    #Return the App Name
    return app_name[0]


def get_ios_app_name(application_id):

    #set the iTunes API URL with the application_id
    itunes_store_api_url = "https://itunes.apple.com/lookup?id=" + application_id

    #get the raw JSON from the iTunes API
    response = urllib2.urlopen(itunes_store_api_url)

    #Parse the JSON
    data = json.load(response)   

    #Return the App Name
    return data["results"][0]["trackName"]     


def get_windows_app_name(application_id):

    #set the windows store URL with the application_id
    windows_store_url = "https://www.microsoft.com/store/appid/" + application_id

    #make a request to the page
    request = urllib2.Request(windows_store_url)
    #add a header so the server let's you parse the page
    request.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5")
    response = urllib2.urlopen(request).read()
    
    #regEx the page to search for the App Name
    app_name = re.findall(r'<h1 id="page-title" class="header-small m-v-n" itemprop="name">(.*?)</h1>', response)

    return app_name[0]

    