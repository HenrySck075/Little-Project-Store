import os,pickle

#termux instance
import webbrowser
from shutil import which
import shlex
def wbopentermux(url,new=0,autoraise=True):
    os.system("termux-open-url "+shlex.quote(url))
def wbopennewtermux(url): wbopentermux(url)
if which("termux-open-url") is not None:
    webbrowser.open = wbopentermux
    webbrowser.open_new = wbopennewtermux
    
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

port = 8080
import socket
def port_in_use():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

while port_in_use():

    port+=1

def create_service(client_secret_file:str, api_name, api_version, scope, prefix=''):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [f'https://www.googleapis.com/auth/{s}' for s in scope]
	
    cred = None
    working_dir = os.getcwd()
    token_dir = 'token files'
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.pickle'

	### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
        with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
            cred:Credentials = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            try: cred.refresh(Request())
            except Exception as hi:
                os.remove(os.path.join(working_dir, token_dir, pickle_file))
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server(success_message="done",redirect_uri_trailing_slash=False, port=port)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server(success_message="done",redirect_uri_trailing_slash=False,port=port)

        with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
            pickle.dump(cred, token)
	
	#return cred.token
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service #fallback to return the snippetless Resource if the file doesnt exist
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, pickle_file))
        return None
