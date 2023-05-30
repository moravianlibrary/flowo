# -----------------------------------------------------------
#   Book Digitization Management System - bachelor's thesis
#
#   Lukas Vaclavek
#   xvacla32
#   
#   proarc.py
# -----------------------------------------------------------

import os
import time
import requests
from requests.adapters import HTTPAdapter
import json

from urllib3 import Retry

from api.models import Record, State

PAimportRunning = False
listOfPAtasks = {}
base_url = os.getenv("PA_URL")

def geturnnbn(pid, cookies, resolverId="test"):
    """
    :param pid: uuid od the document
    :param cookies: login cookies
    :return: True if export was successfull, False otherwise
    """
    # Define the base URL for the API
    global base_url
    print(pid)
    # Define the API endpoint path
    endpoint = "rest/v1/object/urnnbn"

    # Set the headers for the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?pid={pid}&resolverId={resolverId}"

    # Make the API call
    response = requests.post(url, cookies=cookies, headers=headers)
    print(response)
    # Check the status code of the response
    if response.status_code == 200:
        print("Getting urnnbn was successfull")
        return True
    else:
        print("Getting urnnbn failed. Code:", response.status_code, response.text)
        return False


def exportArchive(pid, package, cookies, ignoreMissingUrnNbn=False, isBagit=True):
    """
    :param pid: uuid od the document
    :param package: example "STT" for old prints
    :param cookies: login cookies
    :param ignoreMissingUrnNbn: ignore error of missing urn:nbn
    :param isBagit: if it's a bagit archive
    :return: True if export was successfull, False otherwise
    """
    # first, generate urnnbn for object if it is not ignored
    if not ignoreMissingUrnNbn:
        geturnnbn(pid, cookies)

    global base_url


    # Define the API endpoint path
    endpoint = "rest/v1/export/archive"

    if package == "STT":
        isBagit = False

    # Set the headers for the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?pid={pid}&package={package}&ignoreMissingUrnNbn={ignoreMissingUrnNbn}&isBagit={isBagit}"

    # Make the API call
    response = requests.post(url, cookies=cookies, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        print("Archive export successfull")
        return True
    else:
        print("Archive export failed. Code:", response.status_code, response.text)
        return False


def exportKwis(pid, policy, cookies):
    """
    :param pid: uuid od the document
    :param policy: example "policy:private" for private document
    :param cookies: login cookies
    :return: True if export was successfull, False otherwise
    """
    # Define the base URL for the API
    global base_url

    # Define the API endpoint path
    endpoint = "rest/v1/export/kwis"

    # Set the headers for the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?pid={pid}&policy={policy}"

    # Make the API call
    response = requests.post(url, cookies=cookies, headers=headers)
    print(response)
    # Check the status code of the response
    if response.status_code == 200:
        print("Kwis export successfull")
        return True

    else:
        print("Kwis export failed. Code:", response.status_code, response.text)
        return False


def exportKwisConvolute(parentPid, policy, cookies):
    # exports all convolute children - kwis export
    # TO TEST on another instance (one instance was successful

    children = getConvoluteChildren(parentPid, cookies)
    print("Exporting convolute", parentPid)

    # WAITING FUNCIONALITY TO BE IMPLEMETED HERE
    for i in range(len((children))):
        if i > 0:
            while not isInSolr(parentPid):
                print(".")
        print("Exporting child", children[i])
        if exportKwis(children[i], policy, cookies):
            print("child with PID", children[i], "exported")


def isInSolr(pid):
    # checks kramerius solr, if there is a record of PID in it.

    # Define the base URL for the API
    global base_url

    # Define the API endpoint path
    endpoint = "solr/kramerius/select"

    pid_content = pid.removeprefix("uuid:")

    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?fl=PID&q=PID%3A%22uuid%3A{pid_content}%22&wt=json"

    # Make the API call
    response = requests.get(url)

    # Check the status code of the response
    if response.status_code == 200:
        json_response = json.loads(response.text)
        if json_response['response']['numFound'] >= 0:
            return True
    else:
        return False


def exportArchiveConvolute(parentPid, package, cookies, ignoreMissingUrnNbn=False, isBagit=True):
    # TO TEST
    children = getConvoluteChildren(parentPid, cookies)
    print("Exporting convolute", parentPid)

    for child in children:
        print("Exporting child", child)
        if exportArchive(child, package, cookies, ignoreMissingUrnNbn, isBagit):
            print("child with PID", child, "archived")


def setImportObject(parentPid, id, cookies):
    # Define the base URL for the API
    global base_url
    # Define the API endpoint path
    endpoint = "rest/v1/import/batch"

    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?id={id}&parentPid={parentPid}"

    # Set the headers for the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    # Make the API call
    response = requests.put(url, cookies=cookies, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        print("Object with PID", parentPid, "successfully connected to batch", id)
        return id
    else:
        print("Failed to connect batch to the object. Code:", response.status_code, response.text)
        return False


def newBatch(parentPid, folderPath, profile, device, cookies, priority="medium", indices=True):
    # example: newBatch(parentPid=pid, folderPath="disk_proarc_import/test/", profile="profile.oldprint_full_import, device="device:eebd3a46-66ce-4bfa-af3e-6afe188df8b4", cookies=cookies)

    # Define the base URL for the API
    global base_url

    # Define the API endpoint path
    endpoint = "rest/v1/import/batch"

    # Set the headers for the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json"
    }

    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?folderPath={folderPath}&device={device}&indices={indices}&profile={profile}&priority={priority}"

    # Make the API call
    response = requests.post(url, cookies=cookies, headers=headers)

    # Check the status code of the response
    if response.status_code != 200:
        print("Failed to get make new import batch. Code:", response.status_code, response.text)
        return False

    json_response = json.loads(response.text)
    batch_id = json_response['response']['data'][0]['id']

    state = "LOADING"
    while state != "LOADED":
        state = batchState(batch_id, cookies)
        if state == "LOADING_FAILED":
            return("Import batch", batch_id, "failed. See ProArc logs.")
        print("Import loading batch")
        time.sleep(5)

    print("New batch imported with id:", batch_id)

    record = Record.objects.get(uuid=parentPid)
    stateDone = State.objects.get(pk=1)
    record.batchId = int(batch_id)
    record.state = stateDone
    record.process = record.process + 1
    record.save()
    if not record.batchId:
        record.batchId = batch_id
        record.save()
    uuid = "uuid:" + parentPid
    response = setImportObject(uuid, batch_id, cookies)
    return response


def batchState(batch_id, cookies):
    # Define the base URL for the API
    global base_url

    # Define the API endpoint path
    endpoint = "rest/v1/import/batch"

    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?id={batch_id}"

    # Make the API call
    response = requests.get(url, cookies=cookies)

    # Check the status code of the response
    if response.status_code == 200:
        json_response = json.loads(response.text)
        return json_response['response']['data'][0]['state']

    else:
        return ("Failed to get batch state. Code:", response.status_code, response.text)


def newObject(mods, cookies):
    # Define the base URL for the API
    global base_url

    # Define the API endpoint path
    endpoint = "rest/v1/object"

    model = "model:oldprintsheetmusic"

    # Set the headers for the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?model={model}&xml={mods}"

    # Make the API call
    response = requests.post(url, cookies=cookies, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        return (response.content)
    else:
        return ("Failed to create object. Code:", response.status_code, response.text)


def getConvoluteChildren(parentPid, cookies):
    # Define the base URL for the API
    global base_url

    # Define the API endpoint path
    endpoint = "rest/v1/object/member"

    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?parent={parentPid}"

    # Make the API call
    response = requests.get(url, cookies=cookies)

    # Check the status code of the response
    if response.status_code == 200:
        json_response = json.loads(response.text)
        children = []
        for i in range(int(json_response['response']['totalRows'])):
            children.append(json_response['response']['data'][i]['pid'])

        return children

    else:
        print("Failed to get convolute children. Code:", response.status_code, response.text)
        return None


def setDonator(donator, pid, cookies):
    # Define the base URL for the API
    global base_url

    # Define the API endpoint path
    endpoint = "rest/v1/object/atm"

    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?pid={pid}&donator={donator}"

    # Set the headers for the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    # Make the API call
    response = requests.put(url, cookies=cookies, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        print("Donator has been set successfully")
        return True
    else:
        print("Failed to set donator. Code:", response.status_code, response.text)
        return False


def deleteObject(pid, cookies, hierarchy=True, purge=False, restore=False):
    # Define the base URL for the API
    global base_url

    # Define the API endpoint path
    endpoint = "rest/v1/object"

    pid = "uuid:" + pid

    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?pid={pid}"

    # Set the headers for the request
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    # Make the API call
    response = requests.delete(url, cookies=cookies, headers=headers)

    # Check the status code of the response
    if response.status_code == 200:
        return True
    else:
        print("Failed to delete object. Code:", response.status_code, response.text)
        return False


def catalogueSearch(cookies, barcode, catalog):
    # Define the base URL for the API
    global base_url

    # Define the API endpoint path
    endpoint = "rest/v1/bibliographies/query"

    # Define the query parameters
    field_name = "bar"

    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?catalog={catalog}&fieldName={field_name}&value={barcode}"

    # Make the API call
    response = requests.get(url, cookies=cookies)

    # Check the status code of the response
    if response.status_code == 200:
        # If the response is successful, print the metadata list
        try:
            y = json.loads(response.content)
            metadataCatalogEntries = y["metadataCatalogEntries"]
            entry = metadataCatalogEntries["entry"][0]
            mods = entry["mods"]
            return mods
        except:
            return ""


    else:
        # If the response is not successful, print an error message
        return("Failed to get metadata list.")


def login():
    # Define the base URL for the API
    global base_url

    # Define the API endpoint path
    endpoint = "proarclogin"
    headers = {'Accept': 'application/json'}

    # Define the query parameters
    j_username = os.getenv("PA_USERNAME")
    j_password = os.getenv("PA_PASSWORD")

    # Define the full URL with query parameters
    url = f"{base_url}{endpoint}?j_username={j_username}&j_password={j_password}"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.post(url)


    # Make the API call
    # response = requests.post(url)

    # Check the status code of the response
    if response.status_code == 200:
        # If the response is successful, print the metadata list
        return response.cookies
    else:
        # If the response is not successful, print an error message
        return ("Failed to login.", response.status_code, response.text)


def extract_pid(response):
    json_response = json.loads(response)
    return json_response['response']['data'][0]['pid']