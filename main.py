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

        videosExtensions = ["mp4", "avi", "mov", "wmv", "avi", "avchd", "flv", "mkv"]

        audioExtensions = ["mp3", "m4a", "wav", "aac"]

        imageExtensions = ["jpg", "jpeg", "gif", "png"]

        documentsExtensions = ["pdf", "docx", "doc", "pptx", "ppt", "xls", "xlsx", "csv", "xml", "html", "txt"]

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
            if exists(join("/Users/kevin/Documents/videos", video)):
                remove(join("/Users/kevin/Documents/videos", video))
            shutil.move(join(folder_to_track,  video), "/Users/kevin/Documents/videos", video)

        for audio in self.audios:
            if exists(join("/Users/kevin/Documents/audios", audio)):
                remove(join("/Users/kevin/Documents/audios", audio))
            shutil.move(join(folder_to_track, audio), "/Users/kevin/Documents/audios", audio)

        for image in self.images:
            if exists(join("/Users/kevin/Documents/images", image)):
                remove(join("/Users/kevin/Documents/images", image))
            shutil.move(join(folder_to_track, image), "/Users/kevin/Documents/images", image)
        
        for document in self.documents:
            if exists(join("/Users/kevin/Documents/documents", document)):
                remove(join("/Users/kevin/Documents/documents", document))
            shutil.move(join(folder_to_track, document), "/Users/kevin/Documents/documents", document)
        
        for software in self.softwares:
            if exists(join("/Users/kevin/Documents/softwares", software)):
                remove(join("/Users/kevin/Documents/softwares", software))
            shutil.move(join(folder_to_track, software), "/Users/kevin/Documents/softwares", software)

        for compressedFile in self.compressedFiles:
            if exists(join("/Users/kevin/Documents/zip files", compressedFile)):
                remove(join("/Users/kevin/Documents/zip files", compressedFile))
            shutil.move(join(folder_to_track, compressedFile), "/Users/kevin/Documents/zip files", compressedFile)

        for packetTracerFile in self.packetTracerFiles:
            if exists(join("/Users/kevin/Desktop/packetTracerFiles", packetTracerFile)):
                remove(join("/Users/kevin/Desktop/packetTracerFiles", packetTracerFile))
            shutil.move(join(folder_to_track, packetTracerFile), "/Users/kevin/Desktop/packet tracer files", packetTracerFile)

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

#fileOrganizer.moveFiles()
