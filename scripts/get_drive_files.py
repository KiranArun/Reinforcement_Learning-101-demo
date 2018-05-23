import os, sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import GoogleCredentials

print('Getting files from drive')

gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

local_download_path = os.path.expanduser('./')

if len(sys.argv) > 1:
  	drive_folder = sys.argv[1]
else:
  	drive_folder = 'Reinforcement_Learning-101-demo'

drive_folder = drive.ListFile({'q': "title = '"+str(drive_folder)+"'"}).GetList()

ignore = ['.ipynb_checkpoints','__pycache__','core']

to_download = drive_folder

to_download[0]['path'] = local_download_path
to_download[0]['title'] = ''

def retrieve_folder_files(path_to_folder, folder):

	files = drive.ListFile({'q': "'"+folder['id']+"' in parents"}).GetList()
    
  	try:
    	os.makedirs(os.path.join(path_to_folder,folder['title']))
  	except: pass
    
  	subdirs = []
  
  	for file in files:
      
    	if all(s not in file['title'] for s in ignore) and all(s not in path_to_folder for s in ignore):
      
      		if file['mimeType'][-6:] != 'folder':
                
        		fname = os.path.join(os.path.join(path_to_folder, folder['title']),file['title'])

		        if os.path.isfile(fname) != True:
		        	print('Getting', fname)
		        	f_ = drive.CreateFile({'id': file['id']})
		        	f_.GetContentFile(fname)
      
		    else:
			    file['path'] = os.path.join(path_to_folder, folder['title'])
		        subdirs.append(file)
             
  	return(subdirs)

while len(to_download) > 0:
  
  	subdirs = []

  	for folder in to_download:
    	subdirs += (retrieve_folder_files(folder['path'], folder))

  	to_download = subdirs