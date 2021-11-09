from lrtools.trkformat import *
from vector_2d import Vector
from lrtools.utils import *
from lrtools.track import *
import random



track = Track()
start = 5
end = 5
# add random triggers
# Flickering light warning if you load the track!
for i in range(1000):
	type_ = random.randint(0,2)
	start = random.randint(start-5,start+5)
	end = start = random.randint(start+1,start+7)
	if type_ == TriggerType.Zoom:
		newtrigger = {
					"Start" : start,
					"End" : end,
					"TriggerType" : TriggerType.Zoom,
					"ZoomTarget" : random.randint(1,240)/10,
		}
	if type_ == TriggerType.BGChange:
		newtrigger = {
					"Start" : start,
					"End" : end,
					"TriggerType" : TriggerType.BGChange,
					"backgroundRed" : random.randint(0,255),
					"backgroundGreen" : random.randint(0,255),
					"backgroundBlue" : random.randint(0,255),
		}
	if type_ == TriggerType.LineColor:
		newtrigger = {
					"Start" : start,
					"End" : end,
					"TriggerType" : TriggerType.LineColor,
					"lineRed" : random.randint(0,255),
					"lineGreen" : random.randint(0,255),
					"lineBlue" : random.randint(0,255),
		}
	start = end
	track.Triggers.append(newtrigger)
save_trk(track, "triggers")