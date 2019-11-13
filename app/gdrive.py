import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import time

class GDrive:
    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self.drive = self.auth()
        self.path = os.path.dirname(os.path.abspath(__file__))

    def auth(self):
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
        drive = GoogleDrive(gauth)
        return drive

    def find_file(self, file_name):
        # View all folders and file in your Google Drive
        fileList = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in fileList:
            print('Title: %s, ID: %s' % (file['title'], file['id']))
            # Get the folder ID that you want
            if(file['title'] == file_name):
                fileID = file['id']
            
        return fileID

    def upload_data(self):
        fileID = self.find_file("cinetimes")
        file = self.drive.CreateFile({'title': 'cinetimes-dataset.csv', "mimeType": "text/csv", "parents": [{"kind": "drive#fileLink", "id": fileID}]})
        file.SetContentFile(f"{self.path}/data/cinetimes-dataset.csv")
        print('Uploading the file. It while take a moment...')
        file.Upload() # Upload the file.
        print(f"Created file {file['title']} with mimeType {file['mimeType']}")

    def download_predictions(self):
        start = time.time()

        fileID = self.find_file("predictions.csv")
        # Initialize GoogleDriveFile instance with file id.
        file = self.drive.CreateFile({'id': fileID})
        file.GetContentFile(f"{self.path}/data/predictions.csv")

        print(f"Predictions downloaded in {time.time() - start}s")

def main():
    google_drive = GDrive()
    google_drive.download_predictions()
    globals()[sys.argv[1]]()

if __name__ == "__main__":
		globals()[sys.argv[1]]()    
		#main()
