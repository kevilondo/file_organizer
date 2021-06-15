from os import listdir, remove
from os.path import isfile, join, exists
import shutil

import time
import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileOrganizer(FileSystemEventHandler):

    filesInFolder = []

    videos = []

    audios = []

    images = []

    documents = []

    softwares = []

    compressedFiles = []

    packetTracerFiles = []

    #List the files inside the Download folder

    def getFilesinFolder(self):

        self.filesInFolder = listdir(folder_to_track)

    #group files according to their categories

    def groupFilesinFolders(self):

        self.getFilesinFolder()

        videosExtensions = ["mp4", "avi", "mov", "wmv", "avi", "avchd", "m4v", "flv", "mkv"]

        audioExtensions = ["mp3", "m4a", "wav", "aac"]

        imageExtensions = ["jpg", "jpeg", "gif", "png"]

        documentsExtensions = ["pdf", "docx", "doc", "pptx", "ppt", "ppsx", "xls", "xlsx", "csv", "xml", "html", "txt"]

        softwareExtensions = ["exe", "dmg", "pkg"]

        compressedFilesExt = ["zip", "rar", "tar", "gz", "iso"]

        packetTracerExtensions = ["pka"]

        #check extension of each file in order to group them

        for file in self.filesInFolder:
            
            #get the extension of the file and converts it to lowercase to make the array search easier
            extension = file.split(".")[-1].lower()

            if extension in videosExtensions:
                self.videos.append(file)
            elif extension in audioExtensions:
                self.audios.append(file)
            elif extension in imageExtensions:
                self.images.append(file)
            elif extension in documentsExtensions:
                self.documents.append(file)
            elif extension in softwareExtensions:
                self.softwares.append(file)
            elif extension in compressedFilesExt:
                self.compressedFiles.append(file)
            elif extension in packetTracerExtensions:
                self.packetTracerFiles.append(file)
            else:
                pass

    def moveFiles(self):

        self.groupFilesinFolders()
 
        #we add a timestamp when moving files to avoid errors and duplicates

        for video in self.videos:
            self.move_file_to_folder(video, "/Users/kevin/Documents/videos")

        for audio in self.audios:
            self.move_file_to_folder(audio, "/Users/kevin/Documents/audios")

        for image in self.images:
            self.move_file_to_folder(image, "/Users/kevin/Documents/images")
        
        for document in self.documents:
            self.move_file_to_folder(document, "/Users/kevin/Documents/documents")
        
        for software in self.softwares:
            self.move_file_to_folder(software, "/Users/kevin/Documents/softwares")

        for compressedFile in self.compressedFiles:
            self.move_file_to_folder(compressedFile, "/Users/kevin/Documents/zip files")

        for packetTracerFile in self.packetTracerFiles:
            self.move_file_to_folder(packetTracerFile, "/Users/kevin/Desktop/packet tracer files")

    #this function moves file to the appropriate folder and is called by the moveFile function
    def move_file_to_folder(self, file_name, destination_folder):
        if exists(join(destination_folder, file_name)):
            extension = file_name.split(".")[-1].lower()
            file = file_name.split(".")[-2]
            new_filename = file + "-" + datetime.datetime.now().strftime("%d%m%Y-%H%M%s") + "." + extension
            shutil.move(join(folder_to_track, file_name), join(destination_folder, new_filename))
        else:
            shutil.move(join(folder_to_track, file_name), join(destination_folder, file_name))

    def on_modified(self,event):
        self.moveFiles()

        #clear array of files after moving to avoid errors
        self.videos = []

        self.audios = []

        self.images = []

        self.documents = []

        self.softwares = []

        self.compressedFiles = []

        self.packetTracerFiles = []

folder_to_track = '/Users/kevin/Downloads'

fileOrganizer = FileOrganizer()

observer = Observer()
observer.schedule(fileOrganizer, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
