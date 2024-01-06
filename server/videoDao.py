import uuid
import os

class VideoDAO:
    
    storage_folder = 'storage'
    index_file = 'index.txt'
    storage_path = os.path.dirname(os.path.abspath(__file__)) + f'/{storage_folder}/'
    index_path = storage_path + index_file
    chunk = 1024

    def __init__(self):
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        if not os.path.exists(self.index_path):
            with open(self.index_path, 'wb') as file:
                size = 0
                header = f'{size}'
                file.write(f"{header: <self.chunk}\n".encode())

    def getNameById(self, id_file):
        with open(self.index_path, 'wb') as file:
            _header = file.read(self.chunk)
            while True:
                line = file.read(self.chunk)
                if not line:
                    break
                id, name_file = line.split()
                if(id == id_file): 
                    return name_file.decode('utf-8')
    def getSize(self):
        with open(self.index_path, 'w+b') as file:
            _header = file.read(self.chunk)
            return _header
                
    def updateSize(self, new_size):
        with open(self.index_path, 'w+b') as file:
            _header = file.read(self.chunk)
            new_header = f'{new_size}'
            while True:
                line = file.read(self.chunk)
                if not line:
                    break
                id, name_file = line.split()
                if(id == new_size):
                    return name_file
    
    def get(self, id_file) -> bytes:
        filename = self.getNameById(id_file)
        with open(self.storage_path + filename, 'rb') as file:
            return file
    
    def listAll(self):
        video_list = []
        with open(self.index_path, 'rb') as file:
            _header = file.read(self.chunk)
            while True:
                line = file.read(self.chunk)
                if not line:
                    break
                id, name_file = line.split()
                if id: video_list.append({ id, name_file })
        return video_list

    def add(self, buffer, filename):
        idFile = uuid.uuid4()
        with open(self.storage_path + filename, 'wb') as file:
            file.write(buffer)
        with open(self.index_path, 'w+b') as file:
            line = file.read(self.chunk)
            if not line:
                newline = f"{idFile} {filename}"
                newline_formatted = f"{newline: < self.chunk}"
                file.write(newline_formatted.encode())

if __name__ == '__main__':
    videoDao = VideoDAO()
    with open(videoDao.storage_path + 'video.mp4', 'rb') as file:
        videoDao.add(file, 'newvideo.mp4')
    
