# TRK-Loader-Python
 Line Rider .trk format implemented in Python 3


# Loading Tracks
```python
from load import * # track loader
from track import * # track and line objects
from lr_utils import * # utilities
```
To load a track `name.trk`:
```python
track = loadTrack("track", "name.trk")
```
# Saving Tracks
```python
from write import * # track writer
from track import * # track and line objects
from lr_utils import * # utilities
```
To save a track as `name.trk`:
```python
track = Track()
saveTrack(track, "name")
```

# Track Structure
```python
# assuming track is a Track object:
track.YGravity : int # Y gravity
track.XGravity : int # X gravity
track.GravityWellSize : int # Gravity well size
track.BGColorR : int
track.BGColorG : int
track.BGColorB : int
track.LineColorR : int
track.LineColorG : int
track.LineColorB : int
track.lines : List[Line]
track.Filename : str
track.Name : str
track.Remount : bool
track.ZeroStart : bool
track.frictionless : bool
track.ver : int (61 or 62)
track.StartOffset : Vector
track.Triggers : list
track.StartZoom : int
track.current_id : int
track.Triggers : list
```
# Todo
- Add `prune()` method to `Track.Track` to prune line IDs
- write the rest of the docs on other parts line line triggers and the `Line` object
- Add JSON support