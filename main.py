from os import listdir
from os.path import join, exists
import shutil
import time
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileOrganizer(FileSystemEventHandler):

    folder_to_track = '/Users/kevin/Downloads'
    filesInFolder = []
    allFiles = []

    #List the files inside the Download folder
    def getFilesinFolder(self):
        self.filesInFolder = listdir(self.folder_to_track)
    
    #group files according to their categories
    def groupFilesinFolders(self):
        self.getFilesinFolder()
        videosExtensions = ["mp4", "avi", "mov", "wmv", "avi", "avchd", "m4v", "flv", "mkv"]
        audioExtensions = ["mp3", "m4a", "wav", "aac"]
        imageExtensions = ["jpg", "jpeg", "gif", "png"]
        documentsExtensions = ["pdf", "docx", "doc", "pptx", "ppt", "ppsx", "xls", "xlsm", "xlsx", "csv", "xml", "html", "txt"]
        softwareExtensions = ["exe", "dmg", "pkg"]
        compressedFilesExt = ["zip", "rar", "tar", "gz", "iso"]
        packetTracerExtensions = ["pka"]
        #check extension of each file in order to group them
        for file in self.filesInFolder:
            #get the extension of the file and converts it to lowercase to make the array search easier
            extension = file.split(".")[-1].lower()
            destinationFolder = self.folder_to_track
            if extension in videosExtensions:
                destinationFolder = "/Users/kevin/Documents/videos"
            elif extension in audioExtensions:
                destinationFolder = "/Users/kevin/Documents/audios"
            elif extension in imageExtensions:
                destinationFolder = "/Users/kevin/Documents/images"
            elif extension in documentsExtensions:
                destinationFolder = "/Users/kevin/Documents/documents"
            elif extension in softwareExtensions:
                destinationFolder = "/Users/kevin/Documents/softwares"
            elif extension in compressedFilesExt:
                destinationFolder = "/Users/kevin/Documents/zip files"
            elif extension in packetTracerExtensions:
                destinationFolder = "/Users/kevin/Desktop/packet tracer files"
            else:
                continue
            self.allFiles.append({
                "name": file,
                "destinationFolder": destinationFolder
            })

    def moveFiles(self):
        self.groupFilesinFolders()
        #we add a timestamp when moving files to avoid errors and duplicates
        for file in self.allFiles:
            self.move_file_to_folder(file["name"], file["destinationFolder"])
        self.clear()

    def clear(self):
        #clear array of files after moving to avoid errors
        self.allFiles = []

    #this function moves file to the appropriate folder and is called by the moveFile function
    def move_file_to_folder(self, file_name, destination_folder):
        if exists(join(destination_folder, file_name)):
            extension = file_name.split(".")[-1].lower()
            file = file_name.split(".")[-2]
            new_filename = file + "-" + datetime.datetime.now().strftime("%d%m%Y-%H%M%s") + "." + extension
            shutil.move(join(self.folder_to_track, file_name), join(destination_folder, new_filename))
        else:
            shutil.move(join(self.folder_to_track, file_name), join(destination_folder, file_name))

    def on_modified(self,event):
        self.moveFiles()

fileOrganizer = FileOrganizer()
#move files when app is started
fileOrganizer.moveFiles()
observer = Observer()
observer.schedule(fileOrganizer, fileOrganizer.folder_to_track, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
