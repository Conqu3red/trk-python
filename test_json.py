from json import load
from lrtools.jsonformat import *

save_json(load_json("test.track.json"), "test2.track.json")