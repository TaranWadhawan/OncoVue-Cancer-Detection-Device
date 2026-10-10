# import sys
# import os
# import datetime
# import socket
# import traceback
# import subprocess
# from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
#                              QHBoxLayout, QWidget, QPushButton, QListWidget, QProgressBar)
# from PyQt6.QtCore import QThread, pyqtSignal, Qt
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload

# SCOPES = ['https://www.googleapis.com/auth/drive']
# DRIVE_BACKUP_FOLDER_NAME = "oncovue"

# class SyncWorker(QThread):
#     status_updated = pyqtSignal(str)
#     lists_ready = pyqtSignal(list, list)
#     sync_finished = pyqtSignal(bool, str)

#     def __init__(self, action="check"):
#         super().__init__()
#         self.action = action

#     def has_internet(self):
#         try:
#             socket.setdefaulttimeout(3)
#             socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
#             return True
#         except socket.error:
#             return False

#     def get_credentials(self):
#         cred_path = None
#         possible_paths = [
#             'credentials.json',
#             os.path.join('credentials', 'credentials.json'),
#             os.path.join('data', 'credentials.json')
#         ]
#         for path in possible_paths:
#             if os.path.exists(path) and os.path.getsize(path) > 0:
#                 cred_path = path
#                 break
                
#         if not cred_path:
#             raise FileNotFoundError("credentials.json is missing. Please place your Service Account key file in the root directory.")
            
#         try:
#             creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES)
#             return creds
#         except Exception as e:
#             raise ValueError(f"Failed to read Service Account credentials.json: {str(e)}")

#     def get_or_create_root_folder(self, service, folder_name):
#         query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
#         response = service.files().list(q=query, spaces='drive', fields='files(id)').execute()
#         files = response.get('files', [])
#         if files:
#             return files[0]['id']
#         else:
#             raise FileNotFoundError(f"Backup folder '{folder_name}' not found. Please create it on your personal Google Drive and share it with the Service Account email.")

#     def create_drive_folder(self, service, folder_name, parent_id):
#         file_metadata = {
#             'name': folder_name,
#             'mimeType': 'application/vnd.google-apps.folder',
#             'parents': [parent_id]
#         }
#         file = service.files().create(body=file_metadata, fields='id').execute()
#         return file.get('id')

#     def list_drive_folder_contents(self, service, folder_id):
#         query = f"'{folder_id}' in parents and trashed = false"
#         results = []
#         page_token = None
#         while True:
#             response = service.files().list(
#                 q=query,
#                 spaces='drive',
#                 fields='nextPageToken, files(id, name, mimeType, modifiedTime)',
#                 pageToken=page_token
#             ).execute()
#             results.extend(response.get('files', []))
#             page_token = response.get('nextPageToken', None)
#             if not page_token:
#                 break
#         return results

#     def should_update(self, local_path, remote_mtime_str):
#         if not remote_mtime_str:
#             return True
#         try:
#             local_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(local_path), tz=datetime.timezone.utc)
#             remote_mtime = datetime.datetime.fromisoformat(remote_mtime_str.replace('Z', '+00:00'))
#             return (local_mtime - remote_mtime).total_seconds() > 2
#         except Exception:
#             return True

#     def upload_drive_file(self, service, file_name, local_path, parent_id):
#         file_metadata = {
#             'name': file_name,
#             'parents': [parent_id]
#         }
#         media = MediaFileUpload(local_path, resumable=True)
#         file = service.files().create(
#             body=file_metadata,
#             media_body=media,
#             fields='id'
#         ).execute()
#         return file.get('id')

#     def update_drive_file(self, service, file_id, local_path):
#         media = MediaFileUpload(local_path, resumable=True)
#         file = service.files().update(
#             fileId=file_id,
#             media_body=media,
#             fields='id'
#         ).execute()
#         return file.get('id')

#     def get_local_files_to_sync(self):
#         targets = ["data", r"data\image", r"data\report", r"data\data.xlsx", r"data\manager.xlsx", r"data\user.xlsx"]
#         local_files = []
#         for target in targets:
#             if os.path.exists(target):
#                 if os.path.isdir(target):
#                     for root, dirs, files in os.walk(target):
#                         for f in files:
#                             if not f.startswith('~$') and not f.startswith('.'):
#                                 path_under_target = os.path.join(root, f)
#                                 local_files.append(os.path.relpath(path_under_target, "."))
#                 else:
#                     local_files.append(target)
#         return list(set(local_files))

#     def run(self):
#         if not self.has_internet():
#             self.sync_finished.emit(False, "Error: No internet connection.")
#             return

#         try:
#             creds = self.get_credentials()
#             service = build('drive', 'v3', credentials=creds)
#         except Exception as e:
#             traceback.print_exc()
#             self.sync_finished.emit(False, f"Authentication Error: {str(e)}")
#             return

#         try:
#             self.status_updated.emit("Checking Google Drive directory structures...")
#             drive_root_id = self.get_or_create_root_folder(service, DRIVE_BACKUP_FOLDER_NAME)
            
#             local_files = self.get_local_files_to_sync()
#             remaining = []
#             pushed = []

#             remote_cache = {}
            
#             def map_remote_folders(folder_id, current_rel_path):
#                 items = self.list_drive_folder_contents(service, folder_id)
#                 for item in items:
#                     name = item['name']
#                     rel_name = os.path.join(current_rel_path, name) if current_rel_path else name
#                     rel_name = rel_name.replace("\\", "/")
#                     if item['mimeType'] == 'application/vnd.google-apps.folder':
#                         map_remote_folders(item['id'], rel_name)
#                     else:
#                         remote_cache[rel_name] = item

#             map_remote_folders(drive_root_id, "")

#             for local_f in local_files:
#                 normalized_f = local_f.replace("\\", "/")
#                 if normalized_f in remote_cache:
#                     remote_item = remote_cache[normalized_f]
#                     if self.should_update(local_f, remote_item.get('modifiedTime')):
#                         remaining.append(local_f)
#                     else:
#                         pushed.append(local_f)
#                 else:
#                     remaining.append(local_f)

#             if self.action == "check":
#                 self.lists_ready.emit(remaining, pushed)
#                 self.sync_finished.emit(True, "Check completed. Lists populated.")
#                 return

#             if self.action == "sync":
#                 self.status_updated.emit("Syncing remaining files...")
                
#                 local_to_drive_id = {os.path.abspath("."): drive_root_id}
                
#                 for local_f in remaining:
#                     dirpath = os.path.dirname(local_f) or "."
#                     filename = os.path.basename(local_f)
                    
#                     parts = []
#                     temp_dir = dirpath
#                     while temp_dir and temp_dir != ".":
#                         head, tail = os.path.split(temp_dir)
#                         parts.insert(0, tail)
#                         temp_dir = head
                        
#                     current_parent_id = drive_root_id
#                     accumulated_path = "."
                    
#                     for part in parts:
#                         accumulated_path = os.path.join(accumulated_path, part)
#                         abs_acc = os.path.abspath(accumulated_path)
#                         if abs_acc not in local_to_drive_id:
#                             items = self.list_drive_folder_contents(service, current_parent_id)
#                             folder_exists_id = None
#                             for item in items:
#                                 if item['name'] == part and item['mimeType'] == 'application/vnd.google-apps.folder':
#                                     folder_exists_id = item['id']
#                                     break
#                             if folder_exists_id:
#                                 local_to_drive_id[abs_acc] = folder_exists_id
#                             else:
#                                 local_to_drive_id[abs_acc] = self.create_drive_folder(service, part, current_parent_id)
#                         current_parent_id = local_to_drive_id[abs_acc]
                    
#                     normalized_f = local_f.replace("\\", "/")
#                     if normalized_f in remote_cache:
#                         remote_item = remote_cache[normalized_f]
#                         self.update_drive_file(service, remote_item['id'], local_f)
#                     else:
#                         self.upload_drive_file(service, filename, local_f, current_parent_id)
                
#                 self.sync_finished.emit(True, "Synchronization completed successfully.")

#         except Exception as e:
#             traceback.print_exc()
#             self.sync_finished.emit(False, f"Execution Error: {str(e)}")

# class SyncWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Cloud Synchronization")
#         self.setFixedSize(1020, 720)
        
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.setStyleSheet("background-color: #2c3e50;")
        
#         self.main_layout = QVBoxLayout(self.central_widget)
#         self.main_layout.setContentsMargins(15, 15, 15, 15)
#         self.main_layout.setSpacing(12)
        
#         self.top_bar = QHBoxLayout()
#         self.btn_back = QPushButton("← Back")
#         self.btn_back.setFixedSize(100, 35)
#         self.btn_back.setStyleSheet("""
#             QPushButton {
#                 background-color: #34495e;
#                 color: white;
#                 font-weight: bold;
#                 border: none;
#                 border-radius: 5px;
#                 font-size: 13px;
#             }
#             QPushButton:hover {
#                 background-color: #1a252f;
#             }
#         """)
#         self.btn_back.clicked.connect(self.back_to_dashboard)
#         self.top_bar.addWidget(self.btn_back)
#         self.top_bar.addStretch()
#         self.main_layout.addLayout(self.top_bar)
        
#         self.lists_layout = QHBoxLayout()
#         self.lists_layout.setSpacing(15)
#         self.main_layout.addLayout(self.lists_layout)
        
#         self.left_panel = QVBoxLayout()
#         self.lbl_rem = QLabel("<b>Data Remaining to Push</b>")
#         self.lbl_rem.setStyleSheet("color: #e67e22; font-size: 14px;")
#         self.list_remaining = QListWidget()
#         self.list_remaining.setStyleSheet("background-color: #34495e; border: 1px solid #e67e22; color: #ffffff; border-radius: 5px; padding: 5px;")
#         self.left_panel.addWidget(self.lbl_rem)
#         self.list_remaining.addItem("Click 'Check Status' to start...")
#         self.left_panel.addWidget(self.list_remaining)
#         self.lists_layout.addLayout(self.left_panel)
        
#         self.right_panel = QVBoxLayout()
#         self.lbl_pushed = QLabel("<b>Pushed Already / Synced</b>")
#         self.lbl_pushed.setStyleSheet("color: #2ecc71; font-size: 14px;")
#         self.list_pushed = QListWidget()
#         self.list_pushed.setStyleSheet("background-color: #34495e; border: 1px solid #2ecc71; color: #ffffff; border-radius: 5px; padding: 5px;")
#         self.right_panel.addWidget(self.lbl_pushed)
#         self.right_panel.addWidget(self.list_pushed)
#         self.lists_layout.addLayout(self.right_panel)
        
#         self.status_label = QLabel("Click 'Check Status' to discover remote files.")
#         self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.status_label.setStyleSheet("color: #ecf0f1; font-size: 13px; font-weight: bold;")
#         self.main_layout.addWidget(self.status_label)
        
#         self.progress_bar = QProgressBar()
#         self.progress_bar.setFixedHeight(15)
#         self.progress_bar.setRange(0, 0)
#         self.progress_bar.setTextVisible(False)
#         self.progress_bar.setStyleSheet("""
#             QProgressBar {
#                 border: none;
#                 background-color: #34495e;
#                 border-radius: 5px;
#             }
#             QProgressBar::chunk {
#                 background-color: #3498db;
#                 border-radius: 5px;
#             }
#         """)
#         self.progress_bar.hide()
#         self.main_layout.addWidget(self.progress_bar)
        
#         self.buttons_layout = QHBoxLayout()
#         self.buttons_layout.setSpacing(15)
#         self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.main_layout.addLayout(self.buttons_layout)
        
#         btn_style = """
#             QPushButton {
#                 font-weight: bold;
#                 font-size: 14px;
#                 border: none;
#                 border-radius: 5px;
#                 padding: 12px 25px;
#                 color: white;
#                 min-width: 180px;
#             }
#         """
#         self.btn_check = QPushButton("Check Status")
#         self.btn_check.setStyleSheet(btn_style + "QPushButton{background-color: #3498db;} QPushButton:hover{background-color: #2980b9;}")
#         self.btn_check.clicked.connect(self.run_check)
#         self.buttons_layout.addWidget(self.btn_check)
        
#         self.btn_sync = QPushButton("Sync Now")
#         self.btn_sync.setEnabled(False)
#         self.btn_sync.setStyleSheet(btn_style + "QPushButton{background-color: #2ecc71;} QPushButton:hover{background-color: #27ae60;} QPushButton:disabled{background-color: #7f8c8d;}")
#         self.btn_sync.clicked.connect(self.run_sync)
#         self.buttons_layout.addWidget(self.btn_sync)

#     def back_to_dashboard(self):
#         subprocess.Popen([sys.executable, "page3.py"])
#         self.close()

#     def run_check(self):
#         self.btn_check.setEnabled(False)
#         self.btn_sync.setEnabled(False)
#         self.status_label.setStyleSheet("color: #3498db; font-size: 13px; font-weight: bold;")
#         self.status_label.setText("Scanning directory and connecting to Cloud...")
#         self.progress_bar.show()
        
#         self.worker = SyncWorker(action="check")
#         self.worker.status_updated.connect(self.update_status_text)
#         self.worker.lists_ready.connect(self.populate_lists)
#         self.worker.sync_finished.connect(self.check_finished)
#         self.worker.start()

#     def run_sync(self):
#         self.btn_check.setEnabled(False)
#         self.btn_sync.setEnabled(False)
#         self.status_label.setStyleSheet("color: #3498db; font-size: 13px; font-weight: bold;")
#         self.status_label.setText("Uploading sync modifications to Drive...")
#         self.progress_bar.show()
        
#         self.worker = SyncWorker(action="sync")
#         self.worker.status_updated.connect(self.update_status_text)
#         self.worker.sync_finished.connect(self.sync_finished_event)
#         self.worker.start()

#     def update_status_text(self, text):
#         self.status_label.setText(text)

#     def populate_lists(self, remaining, pushed):
#         self.list_remaining.clear()
#         self.list_pushed.clear()
        
#         for item in remaining:
#             self.list_remaining.addItem(item)
#         for item in pushed:
#             self.list_pushed.addItem(item)
            
#         if remaining:
#             self.btn_sync.setEnabled(True)

#     def check_finished(self, success, message):
#         self.progress_bar.hide()
#         self.btn_check.setEnabled(True)
#         if success:
#             self.status_label.setStyleSheet("color: #2ecc71; font-size: 13px; font-weight: bold;")
#             self.status_label.setText("Status check complete.")
#         else:
#             self.status_label.setStyleSheet("color: #e74c3c; font-size: 13px; font-weight: bold;")
#             self.status_label.setText(message)

#     def sync_finished_event(self, success, message):
#         self.progress_bar.hide()
#         self.btn_check.setEnabled(True)
#         if success:
#             self.status_label.setStyleSheet("color: #2ecc71; font-size: 13px; font-weight: bold;")
#             self.status_label.setText(message)
#             self.run_check()
#         else:
#             self.status_label.setStyleSheet("color: #e74c3c; font-size: 13px; font-weight: bold;")
#             self.status_label.setText(message)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = SyncWindow()
#     window.show()
#     sys.exit(app.exec())

import sys
import os
import datetime
import socket
import json
import traceback
import subprocess
from urllib.parse import urlparse, parse_qs
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QListWidget, QProgressBar)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
SCOPES = ['https://www.googleapis.com/auth/drive']
DRIVE_BACKUP_FOLDER_NAME = "oncovue"

class SyncWorker(QThread):
    status_updated = pyqtSignal(str)
    lists_ready = pyqtSignal(list, list)
    sync_finished = pyqtSignal(bool, str)

    def __init__(self, action="check"):
        super().__init__()
        self.action = action

    def has_internet(self):
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            return True
        except socket.error:
            return False

    def get_credentials(self):
        creds = None
        
        if os.path.exists('token.json'):
            try:
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            except Exception:
                try:
                    os.remove('token.json')
                except Exception:
                    pass
                creds = None
                
        is_valid = False
        if creds:
            try:
                is_valid = creds.valid
            except Exception:
                try:
                    os.remove('token.json')
                except Exception:
                    pass
                creds = None
                is_valid = False
                
        if not creds or not is_valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception:
                    try:
                        os.remove('token.json')
                    except Exception:
                        pass
                    creds = None
            if not creds:
                cred_path = None
                possible_paths = [
                    'credentials.json',
                    r'credentials/credentials.json',
                    os.path.join('credentials', 'credentials.json'),
                    os.path.join('data', 'credentials.json')
                ]
                for path in possible_paths:
                    if os.path.exists(path) and os.path.getsize(path) > 0:
                        cred_path = path
                        break
                        
                if not cred_path:
                    raise FileNotFoundError("credentials.json is missing. Please place it in the root or 'credentials/' folder.")
                
                try:
                    with open(cred_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                except json.JSONDecodeError:
                    raise ValueError("credentials.json is corrupted or not valid JSON format.")
                
                if 'installed' not in config and 'web' not in config:
                    raise ValueError("credentials.json is invalid. It is likely a Service Account key. Please delete it and generate an 'OAuth client ID' with Application Type set to 'Desktop app'.")
                
                payload = config.get('installed', config.get('web', {}))
                if not payload.get('token_uri') or not payload.get('client_id'):
                    raise ValueError("credentials.json is missing critical OAuth parameters. Ensure you downloaded the client configuration for a Desktop Application.")
                    
                flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
                
                print("\n" + "="*80)
                print("MANUAL BROWSER AUTHENTICATION REQUIRED")
                print("1. Please COPY the authorization URL printed below.")
                print("2. Open your web browser manually (Chrome, Edge, or Firefox) and PASTE the URL.")
                print("3. Complete the login, click 'Advanced' -> 'Go to OncoVue (unsafe)' -> 'Continue'.")
                print("="*80 + "\n")
                
                try:
                    creds = flow.run_local_server(host='127.0.0.1', port=0, open_browser=False)
                except Exception:
                    self.status_updated.emit("Local server blocked. Check your console terminal to complete manual authentication.")
                    print("\n" + "="*80)
                    print("LOCAL REDIRECT SERVER BLOCKED / FAILED")
                    print("FALLBACK MANUAL AUTHENTICATION METHOD:")
                    print("1. Complete the authorization in your browser tab.")
                    print("2. Your browser will attempt to redirect to an address starting with 'http://127.0.0.1'.")
                    print("3. Even if your browser says 'This site can’t be reached', COPY the entire URL from your address bar.")
                    print("4. Paste that copied URL here and press Enter:")
                    print("="*80 + "\n")
                    
                    redirect_url = input("Paste Redirect URL here: ").strip()
                    code = None
                    if "code=" in redirect_url:
                        try:
                            parsed = urlparse(redirect_url)
                            code = parse_qs(parsed.query).get('code', [None])[0]
                        except Exception:
                            pass
                        if not code:
                            try:
                                code = redirect_url.split("code=")[1].split("&")[0]
                            except Exception:
                                pass
                    else:
                        code = redirect_url
                        
                    if not code:
                        raise PermissionError("Authorization cancelled or invalid redirect URL pasted.")
                        
                    flow.fetch_token(code=code)
                    creds = flow.credentials
                    
                if not creds:
                    raise PermissionError("Authorization flow failed to complete.")
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_or_create_root_folder(self, service, folder_name):
        query = f"name = '{folder_name}' and 'root' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        response = service.files().list(q=query, spaces='drive', fields='files(id)').execute()
        files = response.get('files', [])
        if files:
            return files[0]['id']
        else:
            return self.create_drive_folder(service, folder_name, 'root')

    def create_drive_folder(self, service, folder_name, parent_id):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        file = service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

    def list_drive_folder_contents(self, service, folder_id):
        query = f"'{folder_id}' in parents and trashed = false"
        results = []
        page_token = None
        while True:
            response = service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name, mimeType, modifiedTime)',
                pageToken=page_token
            ).execute()
            results.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break
        return results

    def should_update(self, local_path, remote_mtime_str):
        if not remote_mtime_str:
            return True
        try:
            local_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(local_path), tz=datetime.timezone.utc)
            remote_mtime = datetime.datetime.fromisoformat(remote_mtime_str.replace('Z', '+00:00'))
            return (local_mtime - remote_mtime).total_seconds() > 2
        except Exception:
            return True

    def upload_drive_file(self, service, file_name, local_path, parent_id):
        file_metadata = {
            'name': file_name,
            'parents': [parent_id]
        }
        media = MediaFileUpload(local_path, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        return file.get('id')

    def update_drive_file(self, service, file_id, local_path):
        media = MediaFileUpload(local_path, resumable=True)
        file = service.files().update(
            fileId=file_id,
            media_body=media,
            fields='id'
        ).execute()
        return file.get('id')

    def get_local_files_to_sync(self):
        targets = ["data", "image", "report", "data.xlsx", "manager.xlsx", "user.xlsx"]
        local_files = []
        for target in targets:
            if os.path.exists(target):
                if os.path.isdir(target):
                    for root, dirs, files in os.walk(target):
                        for f in files:
                            if not f.startswith('~$') and not f.startswith('.'):
                                path_under_target = os.path.join(root, f)
                                local_files.append(os.path.relpath(path_under_target, "."))
                else:
                    local_files.append(target)
        return list(set(local_files))

    def run(self):
        if not self.has_internet():
            self.sync_finished.emit(False, "Error: No internet connection.")
            return

        try:
            creds = self.get_credentials()
            if not creds:
                self.sync_finished.emit(False, "Authentication Error: Credentials not found.")
                return
            service = build('drive', 'v3', credentials=creds)
        except Exception as e:
            traceback.print_exc()
            self.sync_finished.emit(False, f"Authentication Error: {str(e)}")
            return

        try:
            self.status_updated.emit("Checking Google Drive directory structures...")
            drive_root_id = self.get_or_create_root_folder(service, DRIVE_BACKUP_FOLDER_NAME)
            
            local_files = self.get_local_files_to_sync()
            remaining = []
            pushed = []

            remote_cache = {}
            
            def map_remote_folders(folder_id, current_rel_path):
                items = self.list_drive_folder_contents(service, folder_id)
                for item in items:
                    name = item['name']
                    rel_name = os.path.join(current_rel_path, name) if current_rel_path else name
                    rel_name = rel_name.replace("\\", "/")
                    if item['mimeType'] == 'application/vnd.google-apps.folder':
                        map_remote_folders(item['id'], rel_name)
                    else:
                        remote_cache[rel_name] = item

            map_remote_folders(drive_root_id, "")

            for local_f in local_files:
                normalized_f = local_f.replace("\\", "/")
                if normalized_f in remote_cache:
                    remote_item = remote_cache[normalized_f]
                    if self.should_update(local_f, remote_item.get('modifiedTime')):
                        remaining.append(local_f)
                    else:
                        pushed.append(local_f)
                else:
                    remaining.append(local_f)

            if self.action == "check":
                self.lists_ready.emit(remaining, pushed)
                self.sync_finished.emit(True, "Check completed. Lists populated.")
                return

            if self.action == "sync":
                self.status_updated.emit("Syncing remaining files...")
                
                local_to_drive_id = {os.path.abspath("."): drive_root_id}
                
                for local_f in remaining:
                    dirpath = os.path.dirname(local_f) or "."
                    filename = os.path.basename(local_f)
                    
                    parts = []
                    temp_dir = dirpath
                    while temp_dir and temp_dir != ".":
                        head, tail = os.path.split(temp_dir)
                        parts.insert(0, tail)
                        temp_dir = head
                        
                    current_parent_id = drive_root_id
                    accumulated_path = "."
                    
                    for part in parts:
                        accumulated_path = os.path.join(accumulated_path, part)
                        abs_acc = os.path.abspath(accumulated_path)
                        if abs_acc not in local_to_drive_id:
                            items = self.list_drive_folder_contents(service, current_parent_id)
                            folder_exists_id = None
                            for item in items:
                                if item['name'] == part and item['mimeType'] == 'application/vnd.google-apps.folder':
                                    folder_exists_id = item['id']
                                    break
                            if folder_exists_id:
                                local_to_drive_id[abs_acc] = folder_exists_id
                            else:
                                local_to_drive_id[abs_acc] = self.create_drive_folder(service, part, current_parent_id)
                        current_parent_id = local_to_drive_id[abs_acc]
                    
                    normalized_f = local_f.replace("\\", "/")
                    if normalized_f in remote_cache:
                        remote_item = remote_cache[normalized_f]
                        self.update_drive_file(service, remote_item['id'], local_f)
                    else:
                        self.upload_drive_file(service, filename, local_f, current_parent_id)
                
                self.sync_finished.emit(True, "Synchronization completed successfully.")

        except Exception as e:
            traceback.print_exc()
            self.sync_finished.emit(False, f"Execution Error: {str(e)}")

class SyncWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cloud Synchronization")
        self.setFixedSize(1280, 720)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.setStyleSheet("background-color: #2c3e50;")
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(12)
        
        self.top_bar = QHBoxLayout()
        self.btn_back = QPushButton("← Back")
        self.btn_back.setFixedSize(100, 35)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1a252f;
            }
        """)
        self.btn_back.clicked.connect(self.back_to_dashboard)
        self.top_bar.addWidget(self.btn_back)
        self.top_bar.addStretch()
        self.main_layout.addLayout(self.top_bar)
        
        self.lists_layout = QHBoxLayout()
        self.lists_layout.setSpacing(15)
        self.main_layout.addLayout(self.lists_layout)
        
        self.left_panel = QVBoxLayout()
        self.lbl_rem = QLabel("<b>Data Remaining to Push</b>")
        self.lbl_rem.setStyleSheet("color: #e67e22; font-size: 14px;")
        self.list_remaining = QListWidget()
        self.list_remaining.setStyleSheet("background-color: #34495e; border: 1px solid #e67e22; color: #ffffff; border-radius: 5px; padding: 5px;")
        self.left_panel.addWidget(self.lbl_rem)
        self.list_remaining.addItem("Click 'Check Status' to start...")
        self.left_panel.addWidget(self.list_remaining)
        self.lists_layout.addLayout(self.left_panel)
        
        self.right_panel = QVBoxLayout()
        self.lbl_pushed = QLabel("<b>Pushed Already / Synced</b>")
        self.lbl_pushed.setStyleSheet("color: #2ecc71; font-size: 14px;")
        self.list_pushed = QListWidget()
        self.list_pushed.setStyleSheet("background-color: #34495e; border: 1px solid #2ecc71; color: #ffffff; border-radius: 5px; padding: 5px;")
        self.right_panel.addWidget(self.lbl_pushed)
        self.right_panel.addWidget(self.list_pushed)
        self.lists_layout.addLayout(self.right_panel)
        
        self.status_label = QLabel("Click 'Check Status' to discover remote files.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #ecf0f1; font-size: 13px; font-weight: bold;")
        self.main_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #34495e;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 5px;
            }
        """)
        self.progress_bar.hide()
        self.main_layout.addWidget(self.progress_bar)
        
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setSpacing(15)
        self.buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(self.buttons_layout)
        
        btn_style = """
            QPushButton {
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-radius: 5px;
                padding: 12px 25px;
                color: white;
                min-width: 180px;
            }
        """
        self.btn_check = QPushButton("Check Status")
        self.btn_check.setStyleSheet(btn_style + "QPushButton{background-color: #3498db;} QPushButton:hover{background-color: #2980b9;}")
        self.btn_check.clicked.connect(self.run_check)
        self.buttons_layout.addWidget(self.btn_check)
        
        self.btn_sync = QPushButton("Sync Now")
        self.btn_sync.setEnabled(False)
        self.btn_sync.setStyleSheet(btn_style + "QPushButton{background-color: #2ecc71;} QPushButton:hover{background-color: #27ae60;} QPushButton:disabled{background-color: #7f8c8d;}")
        self.btn_sync.clicked.connect(self.run_sync)
        self.buttons_layout.addWidget(self.btn_sync)

    def back_to_dashboard(self):
                # self.timer.stop()
        subprocess.Popen([sys.executable, "loader_large.py"])
        subprocess.Popen([sys.executable, "page3.py"])
        self.close()

    def run_check(self):
        self.btn_check.setEnabled(False)
        self.btn_sync.setEnabled(False)
        self.status_label.setStyleSheet("color: #3498db; font-size: 13px; font-weight: bold;")
        self.status_label.setText("Scanning directory and connecting to Cloud...")
        self.progress_bar.show()
        
        self.worker = SyncWorker(action="check")
        self.worker.status_updated.connect(self.update_status_text)
        self.worker.lists_ready.connect(self.populate_lists)
        self.worker.sync_finished.connect(self.check_finished)
        self.worker.start()

    def run_sync(self):
        self.btn_check.setEnabled(False)
        self.btn_sync.setEnabled(False)
        self.status_label.setStyleSheet("color: #3498db; font-size: 13px; font-weight: bold;")
        self.status_label.setText("Uploading sync modifications to Drive...")
        self.progress_bar.show()
        
        self.worker = SyncWorker(action="sync")
        self.worker.status_updated.connect(self.update_status_text)
        self.worker.sync_finished.connect(self.sync_finished_event)
        self.worker.start()

    def update_status_text(self, text):
        self.status_label.setText(text)

    def populate_lists(self, remaining, pushed):
        self.list_remaining.clear()
        self.list_pushed.clear()
        
        for item in remaining:
            self.list_remaining.addItem(item)
        for item in pushed:
            self.list_pushed.addItem(item)
            
        if remaining:
            self.btn_sync.setEnabled(True)

    def check_finished(self, success, message):
        self.progress_bar.hide()
        self.btn_check.setEnabled(True)
        if success:
            self.status_label.setStyleSheet("color: #2ecc71; font-size: 13px; font-weight: bold;")
            self.status_label.setText("Status check complete.")
        else:
            self.status_label.setStyleSheet("color: #e74c3c; font-size: 13px; font-weight: bold;")
            self.status_label.setText(message)

    def sync_finished_event(self, success, message):
        self.progress_bar.hide()
        self.btn_check.setEnabled(True)
        if success:
            self.status_label.setStyleSheet("color: #2ecc71; font-size: 13px; font-weight: bold;")
            self.status_label.setText(message)
            self.run_check()
        else:
            self.status_label.setStyleSheet("color: #e74c3c; font-size: 13px; font-weight: bold;")
            self.status_label.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SyncWindow()
    window.showFullScreen()
    window.show()
    sys.exit(app.exec())