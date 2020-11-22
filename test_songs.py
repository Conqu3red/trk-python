from load import *
from write import *
from track import *
from lr_utils import *
trk = "song.trk"
track = LoadTrack(trk, trk)
print(track.song, type(track.song))
print(track.song_offset)
track.song_offset = 1
SaveTrack(track, "song_")