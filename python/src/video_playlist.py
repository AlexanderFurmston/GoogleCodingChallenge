"""A video playlist class."""

class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name):
        self.name = name
        self.videos = []
    
    def add(self, video_id):
        if video_id in self.videos:
            return False
        else:
            self.videos.append(video_id)
            return True
