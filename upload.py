# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START drive_quickstart]
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import time
import math
import asyncio
from pyrogram import Client

api_id = 1346694
api_hash = 'f05a88ec0d880cb9fd97073f99468041'
SRING_SESSION="1BVtsOJcBu4MeK2lhsvoZ6fqqORsNN95BNQRgq9mCxrj0cjyPzMC9_7vJFhHpbO6WilpSZ62F9AMxQ-2EeMIX2fI9yGNrZH_4oIWXlVaArNx4ZvBVnp6MT4zrnFSUNRU4siaQbhRneI7Y3uEU_gjGT4x6LglRteuSF9nGdJkGNs5JNOyygiU93gqLtLFhO2tA8S6vfKhJnCkwcu2wyl4HWy_4tABI4uYI3hNADH7lz4lGKcP1ctwm_wX4bIKU5nBsQng8cV_GSJ-UE5NN4nORbOkVRoCYh3SvbOTsW7MXJ608g4hQrot10s5FMdsFFQ96uShkaRyz2CDjVrY6H7BBpcvKiVibhzQ="
client = Client(
    SRING_SESSION,
    api_id=api_id,
    api_hash=api_hash
)
chat_id = os.environ.get("chat_id", int(-1001286726171))

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.metadata"
]

REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
curr = os.environ.get("curr",None)

def humanbytes(size: int) -> str:
    if size is None or isinstance(size, str):
        return ""

    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

def time_formatter(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "") +
        ((str(hours) + " hour(s), ") if hours else "") +
        ((str(minutes) + " minute(s), ") if minutes else "") +
        ((str(seconds) + " second(s), ") if seconds else "")
    )
    return tmp[:-2]

async def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(curr+'/token.pickle'):
        with open(curr+'/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                curr+'/credentials.json', SCOPES, redirect_uri=REDIRECT_URI)
            #creds = flow.run_local_server(port=0)
            auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")
            print("Open this url on your browser : "+auth_url)
            print("Then paste your code here : ", end =" ")
            code = input()
            flow.fetch_token(code=code)
            creds = flow.credentials
        # Save the credentials for the next run
        with open(curr+'/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    file_path = os.environ.get("file_name",None)
    file_name = file_path.split("/")[-1]

    media_body = MediaFileUpload(
        file_path,
        resumable=True
    )

    body = {
        "name": file_name,
    }

    file = service.files().create(body=body, media_body=media_body,
                                  fields="id").execute()

    file_id = file.get("id")
    permission = {
        "role": "reader",
        "type": "anyone"
    }

    service.permissions().create(fileId=file_id, body=permission).execute()

    print ("File Name: "+file_name+"\nYour sharable link: "+ "https://drive.google.com/file/d/" + file.get('id')+'/view')
    text = "File Name: {}\nLink: https://drive.google.com/file/d/{}".format(file_name,file.get('id')+'/view')
    await client.send_message(chat_id, text, disable_web_page_preview=True)

with client:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

# The first parameter is the .session file name (absolute paths allowed)
