from binary import BinaryStream
from vector_2d import Vector as Vector2d
byteorder = "little"

from lr_utils import *

LineType = linetype()
TrackFeatures = trackfeatures()
TrackMetadata = trackmetadata()
TriggerType = triggertype()


def GetTrackFeatures(trk):
	ret = {}
	for el in vars(TrackFeatures).values():
		ret[el] = False
	if (trk.ZeroStart):
		ret[TrackFeatures.zerostart] = True;
	if (trk.frictionless):
		ret[TrackFeatures.frictionless] = True;
	for l in trk.lines:
		if (l.type == LineType.Scenery):
			if (abs(l.width - 1) > 0.0001):
				ret[TrackFeatures.scenerywidth] = True;
		if (l.type == LineType.Red):
			if (l.Multiplier != 1):
				ret[TrackFeatures.redmultiplier] = True;
		if (l.type == LineType.Blue):
			pass
			#if (l.Trigger != None)
			#	ret[TrackFeatures.ignorable_trigger] = true;
	if (trk.ver == 61):
		ret[TrackFeatures.six_one] = True;
	if (trk.Remount):
		ret[TrackFeatures.remount] = True;
	return ret;



def SaveTrack(trk, savename):
	directory = ""
	filename = directory + savename + ".trk";
	with open(filename, "wb") as f:
		bw = BinaryStream(f);
		bw.WriteBytes(b"TRK\xf2")
		bw.WriteBytes(bytes([1]))
		featurestring = "";
		lines = trk.lines
		featurelist = GetTrackFeatures(trk);
		songinfo = featurelist[TrackFeatures.songinfo]
		redmultiplier = featurelist[TrackFeatures.redmultiplier]
		zerostart = featurelist[TrackFeatures.zerostart]
		scenerywidth = featurelist[TrackFeatures.scenerywidth]
		six_one = featurelist[TrackFeatures.six_one]
		ignorable_trigger = featurelist[TrackFeatures.ignorable_trigger]
		remount = featurelist[TrackFeatures.remount]
		frictionless = featurelist[TrackFeatures.frictionless]
		featurestring = ""
		#print(featurelist)
		for feature in featurelist.items():
			#print(feature)
			if (feature[1]):
				#print(feature)
				featurestring += feature[0] + ";";
		#print(featurestring)
		WriteString(bw, featurestring);
		if (songinfo):
			#bw.Write(trk.Song.ToString());
			# Don't write song info
			pass
		bw.WriteDouble(trk.StartOffset.x);
		bw.WriteDouble(trk.StartOffset.y);
		bw.WriteInt32(len(lines));
		for line in lines:
			#print(line)
			l = line
			type_ = line.type;
			if (l.type == LineType.Blue or l.type == LineType.Red):
				if (l.inv):
					type_ |= 1 << 7;
				ext = l.Extension
				type_ |= ((ext & 0x03) << 5); #bits: 2
				bw.WriteBytes(bytes([type_]));
				if (redmultiplier):
					if (l.type == LineType.Red):
						bw.WriteBytes(bytes([l.Multiplier]));
				if (ignorable_trigger):
					pass
					''' not required
					if (l.Trigger != null)
						if (l.Trigger.ZoomTrigger) # check other triggers here for at least one
						{
							bw.Write(l.Trigger.ZoomTrigger);
							if (l.Trigger.ZoomTrigger)
								bw.Write(l.Trigger.ZoomTarget);
								bw.Write((short)l.Trigger.ZoomFrames);
						else
							bw.Write(false);
					else
						bw.Write(false);#zoomtrigger=false
					'''
				bw.WriteInt32(l.ID);
				if (l.Extension != 0):
					# this was extension writing
					# but we no longer support this.
					bw.WriteBytes(b'\xff\xff\xff\xff');
					bw.WriteBytes(b'\xff\xff\xff\xff');
			else:
				bw.WriteBytes(bytes([type_]));
				if (scenerywidth):
					if (l.type == LineType.Scenery):
						b = bytes([int((round(l.width, 1) * 10))]);
						bw.WriteBytes(b);
			bw.WriteDouble(line.point1.x);
			bw.WriteDouble(line.point1.y);
			bw.WriteDouble(line.point2.x);
			bw.WriteDouble(line.point2.y);
		bw.WriteBytes(b'META');
		
		metadata = []
		metadata.append(TrackMetadata.startzoom + "=" + str(int(trk.StartZoom)))
		#Only add if the values are different from default
		if (trk.YGravity != 1):
			metadata.append(TrackMetadata.ygravity + "=" + str(int(trk.YGravity)));
		if (trk.XGravity != 0):
			metadata.append(TrackMetadata.xgravity + "=" + str(int(trk.XGravity)));
		if (trk.GravityWellSize != 10):
			metadata.append(TrackMetadata.gravitywellsize + "=" + str(int(trk.GravityWellSize)));
		
		if (trk.BGColorR != 244):
			metadata.append(TrackMetadata.bgcolorR + "=" + str(int(trk.BGColorR)));
		if (trk.BGColorG != 245):
			metadata.append(TrackMetadata.bgcolorG + "=" + str(int(trk.BGColorG)));
		if (trk.BGColorB != 249):
			metadata.append(TrackMetadata.bgcolorB + "=" + str(int(trk.BGColorB)));
		
		if (trk.LineColorR != 0):
			metadata.append(TrackMetadata.linecolorR + "=" + str(int(trk.LineColorR)));
		if (trk.LineColorG != 0):
			metadata.append(TrackMetadata.linecolorG + "=" + str(int(trk.LineColorG)));
		if (trk.LineColorB != 0):
			metadata.append(TrackMetadata.linecolorB + "=" + str(int(trk.LineColorB)));
		triggerstring = "";
		for i in range(len(trk.Triggers)):
			t = trk.Triggers[i];
			if (i != 0): triggerstring += "&";
			
			if t["TriggerType"] == TriggerType.Zoom:
				triggerstring += str(TriggerType.Zoom);
				triggerstring += ":";
				triggerstring += str(t["ZoomTarget"]);
				triggerstring += ":";
			if t["TriggerType"] == TriggerType.BGChange:
				triggerstring += str(TriggerType.BGChange);
				triggerstring += ":";
				triggerstring += str(t["backgroundRed"]);
				triggerstring += ":";
				triggerstring += str(t["backgroundGreen"]);
				triggerstring += ":";
				triggerstring += str(t["backgroundBlue"]);
				triggerstring += ":";
			if t["TriggerType"] == TriggerType.LineColor:
				triggerstring += str(TriggerType.LineColor);
				triggerstring += ":";
				triggerstring += str(t["lineRed"]);
				triggerstring += ":";
				triggerstring += str(t["lineGreen"]);
				triggerstring += ":";
				triggerstring += str(t["lineBlue"]);
				triggerstring += ":";
			triggerstring += str(t["Start"]);
			triggerstring += ":";
			triggerstring += str(t["End"]);
		if (len(trk.Triggers) > 0): # If here are not trigger don't add triggers entry
			metadata.append(TrackMetadata.triggers + "=" + str(triggerstring))
		
		bw.WriteInt16(len(metadata));
		for string in metadata:
			WriteString(bw, string);
		return filename;



def WriteString(bw, string):
			#bw.WriteBytes(len(string).to_bytes((len(string).bit_length()), 'little'));
			bw.WriteUInt16(len(string))
			bw.WriteBytes(str.encode(string, "ascii"));