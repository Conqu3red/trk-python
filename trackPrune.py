# Conqu3red's Line ID Pruner
from lrtools.trkformat import *
from vector_2d import Vector
from lrtools.utils import *
from lrtools.track import *
from typing import *
import os
track_name = input("Please enter track location: ")


track = load_trk(track_name, "track")
print(f"[-] Loaded {track_name}!")
# for id in l
# 	find all ids below id

def fix(l: List[int]):
	fixed = []
	for c, itm in enumerate(l):
		# find ids below itm
		num_under = [a for a in l if a < itm]
		fixed.append(len(num_under)+1)
	return fixed

blue_and_red = [line for line in track.lines if vars(line).get("ID")]
green = [line for line in track.lines if not vars(line).get("ID")]

track_ids = [line.ID for line in blue_and_red]
#print(track_ids)
prev_max = max(track_ids)
print(f"[!] Highest Line ID is {prev_max}")
print(f"[#] Fixing Line IDs...")
track_ids = fix(track_ids)
#print(track_ids)
print(f"[#] Fixed Line IDs!")
new_max = max(track_ids)
print(f"[!] New Highest Line ID is {new_max}")
print(f"[!] Highest Line ID decreased by {round(((prev_max/new_max)-1)*100)}%")
for c in range(len(blue_and_red)):
	blue_and_red[c].ID = track_ids[c]

track.lines = blue_and_red + green
#print(track.lines)
save_trk(track, track_name)
print(f"[-] Saved {track_name}!")
input("Press Enter to close the program...")