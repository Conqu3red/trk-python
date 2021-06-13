from lrtools.trkformat import *
from lrtools.track import *
from lrtools.utils import *
trk = "song.trk"
track = load_trk(trk, trk)
print(track.song, type(track.song))
print(track.song_offset)
track.song_offset = 1
save_trk(track, "song_")