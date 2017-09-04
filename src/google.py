from __future__ import print_function
import httplib2
import os
import json
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import base64
import operator
import datetime
from urllib.error import HTTPError as HttpError

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/drive']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def ListMessagesWithLabels(service, user_id, label_ids=[]):
  """List all Messages of the user's mailbox with label_ids applied.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    label_ids: Only return Messages with these labelIds applied.

  Returns:
    List of Messages that have all required Labels applied. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate id to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               labelIds=label_ids).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])
    c = 1
    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id,
                                                 labelIds=label_ids,
                                                 pageToken=page_token).execute()
      messages.extend(response['messages'])
      if (c <= 0):
          break
      else:
          c -= 1
    return messages
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    #print ('Message snippet: %s' % message['snippet'])

    return message
  except errors.HttpError as error:
    print ('An error occurred: %s' % error)

def GetAttachments(service, user_id, msg_id, store_dir):
  """Get and store attachment from Message with given id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    store_dir: The directory used to store attachments.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    try:
        tmp = message['payload']['parts']
    except:
        print('no attachements')
        return
    for part in message['payload']['parts']:
      if part['filename']:
        path = os.path.join(store_dir, part['filename'])
        if (os.path.isfile(path)):
            print('file ' + part['filename'] + ' already downloaded')
            return
        if 'data' in part['body']:
            data=part['body']['data']
        else:
            att_id=part['body']['attachmentId']
            att=service.users().messages().attachments().get(userId=user_id, messageId=msg_id,id=att_id).execute()
            data=att['data']
        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        if not os.path.exists(store_dir):
            os.makedirs(store_dir)
        f = open(path, 'wb')
        f.write(file_data)
        f.close()
        print('Downloaded '+ part['filename'])
            

  except HttpError as error:
    print ('An error occurred: %s' % error)

def decodeB64(content):
    return base64.b64decode(content)

def toDate(ms):
    return datetime.datetime.fromtimestamp(int(ms)/1000.0)

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    serviceDrive = discovery.build('drive', 'v3', http=http)
    service = discovery.build('gmail', 'v1', http=http)

    '''
    results = serviceDrive.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))


    file_metadata = {
                  'name' : 'MyStrangeFolder',
                  'mimeType' : 'application/vnd.google-apps.folder'
                }
    file = serviceDrive.files().create(body=file_metadata,
                                    fields='id').execute()
    print ('Folder ID: %s' % file.get('id'))
    '''

    '''
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      #for label in labels:
        print(label['name'])
    '''
    inbox = ['INBOX']

    l = []
    l = ListMessagesWithLabels(service, 'me', inbox)

    print('processing')
    grams = {}
    count = 20
    for mail in l:
        m = GetMessage(service, 'me', mail['id'])
        #print(toDate(m['internalDate']), end='\t')
        m = m['payload']
        m = m['headers']
        for rt in m:
            if (rt['name'] == 'From'):
                val = rt['value'][rt['value'].find("<")+1:rt['value'].find(">")]
                grams.setdefault(val, 0)
                grams[val] += 1
                print('added')
        count -= 1
        if (count < 0):
            break
    sorted_x = sorted(grams.items(), key=operator.itemgetter(1))
    sorted_x.reverse()
    lUser = []
    for x in sorted_x:
        if ('reply' not in x[0]):
            lUser.append(x[0])
    print(lUser)

    with open('GOOGLE/GoogleUser.config', "w+") as myfile:
        for email in lUser:
            myfile.write(email + '\n')

    
    '''
    count = 25
    for mail in l:
        a = GetAttachments(service, 'me', mail['id'], 'piecejointe')
        count -= 1
        if (count <= 0):
            break
    '''
        
    '''
    for mail in l:
        m = GetMessage(service, 'me', mail['id'])
        
        m = m['payload']
        m = m['parts']
        for elt in m:
            elt = elt['body']
            file_data = base64.urlsafe_b64decode(elt['data'].encode('UTF-8'))
            print(file_data)
            print('-----------------------------------------------------')
    '''
    
if __name__ == '__main__':
    main()
