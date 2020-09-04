# Conqu3red's Line ID Pruner
from load import *
from write import *
from vector_2d import Vector
from lr_utils import *
from track import *
track_name = input("Please enter track name (without .trk extension): ")


track = LoadTrack(track_name+".trk","track")
print(f"[-] Loaded {track_name}.trk!")
# for id in l
# 	find all ids below id

def fix(l):
	fixed = []
	for c, itm in enumerate(l):
		# find ids below itm
		num_under = [a for a in l if a < itm]
		fixed.append(len(num_under))
	return fixed

blue_and_red = [line for line in track.lines if vars(line).get("ID")]
green = [line for line in track.lines if not vars(line).get("ID")]

track_ids = [line.ID for line in blue_and_red]
#print(track_ids)
print(f"[!] Highest Line ID is {max(track_ids)}")
print(f"[#] Fixing Line IDs...")
track_ids = fix(track_ids)
#print(track_ids)
print(f"[#] Fixed Line IDs!")
print(f"[!] Highest Line ID is {max(track_ids)}")
for c in range(len(blue_and_red)):
	blue_and_red[c].ID = track_ids[c]

track.lines = blue_and_red + green
#print(track.lines)
SaveTrack(track, track_name)
print(f"[-] Saved {track_name}.trk!")
input("Press Enter to close the program...")