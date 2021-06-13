from lrtools import jsonformat, trkformat, track
import os

location = input("enter json file location: ")
t = jsonformat.load_json(location)
save_name = os.path.splitext(os.path.basename(location))[0]
trkformat.save_trk(t, save_name)
print(f"Saved to {save_name}.trk")