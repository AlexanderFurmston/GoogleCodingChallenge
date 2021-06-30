"""A video player class."""

from src.video_playlist import Playlist
from .video_library import VideoLibrary
import random
from requests.structures import CaseInsensitiveDict


def get_tags_formatted(video):
    tags = ""
    for t in video.tags: tags += " " + t
    return tags[1:]

class VideoPlayer:
    """A class used to represent a Video Player."""
    currently_playing = None
    paused = False
    playlists = {}
    playlists = CaseInsensitiveDict(playlists)
    flags = {}

    def __init__(self):
        self._video_library = VideoLibrary()
        self.currently_playing = None
        self.paused = False
        self.playlists = {}
        self.playlists = CaseInsensitiveDict(self.playlists)
        self.flags = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        videos = self._video_library.get_all_videos()
        videos.sort(key = lambda x: x.title)
        for video in videos: 
            flag = self.flags.get(video.video_id)
            if flag == None:
                print(f"  {video.title} ({video.video_id}) [{get_tags_formatted(video)}]")
            else:
                print(f"  {video.title} ({video.video_id}) [{get_tags_formatted(video)}] - FLAGGED (reason: {flag})")
        #print("show_all_videos needs implementation")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        flag = self.flags.get(video_id, None)
        if flag != None:
            print(f"Cannot play video: Video is currently flagged (reason: {flag})")
            return
        video = self._video_library.get_video(video_id)
        if video == None: # if the video ID is invalid
            print("Cannot play video: Video does not exist")
        elif self.currently_playing == None: # if nothing is currently playing
            print(f"Playing video: {video.title}")
            self.currently_playing = video.video_id
        else: # if something is currently playing
            self.stop_video()
            print(f"Playing video: {video.title}")
            self.currently_playing = video.video_id
        #print("play_video needs implementation")

    def stop_video(self):
        """Stops the current video."""
        if self.currently_playing == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self._video_library.get_video(self.currently_playing).title}")
            self.currently_playing = None
            self.paused = False
        #print("stop_video needs implementation")

    def play_random_video(self):
        """Plays a random video from the video library."""
        all_vids = self._video_library.get_all_videos() 
        all_vids = list(map(lambda x: x.video_id, all_vids))
        good_vids = list(filter(lambda x: self.flags.get(x, None) == None, all_vids))
        if len(good_vids) == 0:
            print("No videos available")
            return
        self.play_video(random.choice(good_vids))
        #print("play_random_video needs implementation")

    def pause_video(self):
        """Pauses the current video."""
        if self.paused:
            print(f"Video already paused: {self._video_library.get_video(self.currently_playing).title}")
        elif self.currently_playing == None:
            print("Cannot pause video: No video is currently playing")
        else:
            self.paused = True
            print(f"Pausing video: {self._video_library.get_video(self.currently_playing).title}")
        #print("pause_video needs implementation")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.currently_playing == None:
            print("Cannot continue video: No video is currently playing")
        elif not self.paused:
            print("Cannot continue video: Video is not paused")
        else:
            self.paused = False
            print(f"Continuing video: {self._video_library.get_video(self.currently_playing).title}")

        #print("continue_video needs implementation")

    def show_playing(self):
        """Displays video currently playing."""
        if self.currently_playing == None:
            print("No video is currently playing")
        else:
            video = self._video_library.get_video(self.currently_playing)
            if self.paused:
                print(f"Currently playing: {video.title} ({video.video_id}) [{get_tags_formatted(video)}] - PAUSED")
            else:
                print(f"Currently playing: {video.title} ({video.video_id}) [{get_tags_formatted(video)}]")
        #print("show_playing needs implementation")

    ########
    #PART 2#
    ########
    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self.playlists.get(playlist_name, None) == None:
            new_playlist = Playlist(playlist_name)
            self.playlists[playlist_name] = new_playlist
            print(f"Successfully created new playlist: {playlist_name}")
        else:
            print(f"Cannot create playlist: A playlist with the same name already exists {self.playlists.get(playlist_name, None).name} {playlist_name}")
        #print("create_playlist needs implementation")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        flag = self.flags.get(video_id, None)
        if flag != None:
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {flag})")
            return

        playlist = self.playlists.get(playlist_name, None)
        if playlist == None:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        elif not playlist.add(video_id):
            print(f"Cannot add video to {playlist_name}: Video already added")
        else:
            print(f"Added video to {playlist_name}: {self._video_library.get_video(video_id).title}") # video is added in the elif on line 137

        #print("add_to_playlist needs implementation")

    def show_all_playlists(self):
        """Display all playlists."""
        playlist_names = sorted(list(self.playlists.keys()), key = lambda x: x.upper())
        if len(playlist_names) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            for name in playlist_names: print(f"  {name}")
        #print("show_all_playlists needs implementation")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.playlists.get(playlist_name, None)
        if playlist == None:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            print(f"Showing playlist: {playlist_name}")
            if len(playlist.videos) == 0:
                print("  No videos here yet")
            else:
                for video_id in playlist.videos:
                    video = self._video_library.get_video(video_id)
                    flag = self.flags.get(video_id)
                    if flag == None:
                        print(f"  {video.title} ({video_id}) [{get_tags_formatted(video)}]")
                    else:
                        print(f"  {video.title} ({video.video_id}) [{get_tags_formatted(video)}] - FLAGGED (reason: {flag})")
        #print("show_playlist needs implementation")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self.playlists.get(playlist_name, None)
        if playlist == None:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        elif self._video_library.get_video(video_id) == None:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
        elif video_id not in playlist.videos:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
        else:
            print(f"Removed video from {playlist_name}: {self._video_library.get_video(video_id).title}")
            playlist.videos.remove(video_id)
            self.playlists[playlist.name] = playlist
        
        #print("remove_from_playlist needs implementation")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.playlists.get(playlist_name, None)
        if playlist == None:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            print(f"Successfully removed all videos from {playlist_name}")
            playlist.videos = []
            self.playlists[playlist.name] = playlist
        #print("clears_playlist needs implementation")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self.playlists.get(playlist_name, None)
        if playlist == None:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            print(f"Deleted playlist: {self.playlists.pop(playlist_name).name}")
        #print("deletes_playlist needs implementation")

    ########
    #PART 3#
    ########
    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = self._video_library.get_all_videos()
        correct_videos = list(filter(lambda x: search_term.upper() in x.title.upper() and self.flags.get(x.video_id, None) == None, videos))
        correct_videos.sort(key = lambda x: x.title.upper())
        if len(correct_videos) == 0:
            print(f"No search results for {search_term}")
            return

        print(f"Here are the results for {search_term}:")
        for i in range(len(correct_videos)):
            print(f"  {i+1}) {correct_videos[i].title} ({correct_videos[i].video_id}) [{get_tags_formatted(correct_videos[i])}]")
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        
        user_input = input()
        try:
            video_id = correct_videos[int(user_input)-1].video_id
            self.play_video(video_id)
        except:
            pass
        #print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = self._video_library.get_all_videos()
        correct_videos = list(filter(lambda x: video_tag.lower() in x.tags and self.flags.get(x.video_id, None) == None, videos))
        correct_videos.sort(key = lambda x: x.title.upper())
        if len(correct_videos) == 0:
            print(f"No search results for {video_tag}")
            return
        
        print(f"Here are the results for {video_tag}:")
        for i in range(len(correct_videos)):
            print(f"  {i+1}) {correct_videos[i].title} ({correct_videos[i].video_id}) [{get_tags_formatted(correct_videos[i])}]")
        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        
        user_input = input()
        try:
            video_id = correct_videos[int(user_input)-1].video_id
            self.play_video(video_id)
        except:
            pass
        #print("search_videos_tag needs implementation")

    ########
    #PART 4#
    ########
    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if self.flags.get(video_id, None) != None:
            print("Cannot flag video: Video is already flagged")
        elif self._video_library.get_video(video_id) == None:
            print("Cannot flag video: Video does not exist")
        else:
            if self.currently_playing == video_id:
                self.stop_video()
            print(f"Successfully flagged video: {self._video_library.get_video(video_id).title} (reason: {flag_reason})")
            self.flags[video_id] = flag_reason
        #print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        if self._video_library.get_video(video_id) == None:
            print("Cannot remove flag from video: Video does not exist")
        elif self.flags.get(video_id, None) == None:
            print("Cannot remove flag from video: Video is not flagged")
        else:
            print(f"Successfully removed flag from video: {self._video_library.get_video(video_id).title} (reason: {self.flags.pop(video_id)})")
        #print("allow_video needs implementation")
