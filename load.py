from binary import BinaryStream
from vector_2d import Vector as Vector2d
byteorder = "little"

from track import *

from lr_utils import *

LineType = linetype()
TrackFeatures = trackfeatures()
TrackMetadata = trackmetadata()
TriggerType = triggertype()


linetriggers = []
supported_features = [
	"REDMULTIPLIER",
	"SCENERYWIDTH",
	"6.1","SONGINFO",
	"IGNORABLE_TRIGGER",
	"ZEROSTART",
];
	
REDMULTIPLIER_INDEX = 0;
SCENERYWIDTH_INDEX = 1;
SIX_ONE_INDEX = 2;
SONGINFO_INDEX = 3;
IGNORABLE_TRIGGER_INDEX = 4;
ZEROSTART_INDEX = 5;

def ParseFloat(f: str) -> float:
	ret = float(f) # will raise ValueError if not a valid float
	return ret;

def ParseDouble(f: str) -> float:
	ret = float(f) # will raise ValueError if not a valid float
	return ret;

def ParseInt(f: str) -> int:
	ret = int(f) # will raise ValueError if not a valid float
	return ret;


def ParseMetadata(ret, br):
	count = br.ReadInt16();
	for i in range(count):
		metadata = ReadString(br).split('=');
		if metadata[0] == TrackMetadata.startzoom:
			#print(metadata[1])
			ret.StartZoom = ParseFloat(metadata[1])
		if metadata[0] == TrackMetadata.ygravity:
			ret.YGravity = ParseFloat(metadata[1]);
		if metadata[0] == TrackMetadata.xgravity:
			ret.XGravity = ParseFloat(metadata[1]);
		if metadata[0] == TrackMetadata.gravitywellsize:
			ret.GravityWellSize = ParseDouble(metadata[1]);
		if metadata[0] == TrackMetadata.bgcolorR:
			ret.BGColorR = ParseInt(metadata[1]);
		if metadata[0] == TrackMetadata.bgcolorG:
			ret.BGColorG = ParseInt(metadata[1]);
		if metadata[0] == TrackMetadata.bgcolorB:
			ret.BGColorB = ParseInt(metadata[1]);
		if metadata[0] == TrackMetadata.linecolorR:
			ret.LineColorR = ParseInt(metadata[1]);
		if metadata[0] == TrackMetadata.linecolorG:
			ret.LineColorG = ParseInt(metadata[1]);
		if metadata[0] == TrackMetadata.linecolorB:
			ret.LineColorB = ParseInt(metadata[1]);
		if metadata[0] == TrackMetadata.triggers:
			triggers = metadata[1].split('&');
			#print(triggers)
			for t in triggers:
				tdata = t.split(':');
				try:
					ttype = ParseInt(tdata[0]);
				except:
					raise Exception(
						"Unsupported trigger type");
				#GameTrigger newtrigger;
				#int start;
				#int end;
				if ttype == TriggerType.Zoom:
					target = ParseFloat(tdata[1]);
					start = ParseInt(tdata[2]);
					end = ParseInt(tdata[3]);
					newtrigger = {
						"Start" : start,
						"End" : end,
						"TriggerType" : TriggerType.Zoom,
						"ZoomTarget" : target,
					};
				elif ttype == TriggerType.BGChange:
					red = ParseInt(tdata[1]);
					green = ParseInt(tdata[2]);
					blue = ParseInt(tdata[3]);
					start = ParseInt(tdata[4]);
					end = ParseInt(tdata[5]);
					newtrigger = {
						"Start" : start,
						"End" : end,
						"TriggerType" : TriggerType.BGChange,
						"backgroundRed" : red,
						"backgroundGreen" : green,
						"backgroundBlue" : blue,
					};
				elif ttype == TriggerType.LineColor:
					linered = ParseInt(tdata[1]);
					linegreen = ParseInt(tdata[2]);
					lineblue = ParseInt(tdata[3]);
					start = ParseInt(tdata[4]);
					end = ParseInt(tdata[5]);
					newtrigger = {
						"Start" : start,
						"End" : end,
						"TriggerType" : TriggerType.LineColor,
						"lineRed" : linered,
						"lineGreen" : linegreen,
						"lineBlue" : lineblue,
					};
				else:
					raise Exception(
						"Unsupported trigger type");
				ret.Triggers.append(newtrigger);
	return ret

def LoadTrack(trackfile, trackname):
	linetriggers = []
	addedlines = []
	ret = Track();
	ret.lines = []
	ret.Filename = trackfile;
	ret.Name = trackname;
	ret.Remount = False;
	addedlines = {};
	location = trackfile;
	with open(trackfile, "rb") as f:
		File = f
		_bytes = File.read()
		File.seek(0,0)
		#print(str(_bytes))
		br = BinaryStream(File)
		magic = br.ReadBytes(4)
		if magic != b"TRK\xf2":
			raise Exception("File was read as .trk but it is not valid")
		version = int.from_bytes(br.ReadByte(), byteorder)
		#print(_bytes)
		features = list(filter(None, ReadString(br).split(';')))
		#print(features)
		if (version != 1):
			raise Exception("Unsupported version")
		redmultipier = False;
		scenerywidth = False;
		supports61 = False;
		songinfo = False;
		ignorabletrigger = False;
		ret.ZeroStart = False;
		ret.Remount = False;
		ret.frictionless = False;
		for i in range(len(features)):
			if features[i] == TrackFeatures.redmultiplier:
				redmultipier = True;
			elif features[i] == TrackFeatures.scenerywidth:
				scenerywidth = True;
			elif features[i] == TrackFeatures.six_one:
				supports61 = True;
			elif features[i] == TrackFeatures.songinfo:
				songinfo = True;
			elif features[i] == TrackFeatures.ignorable_trigger:
				ignorabletrigger = True;
			elif features[i] == TrackFeatures.zerostart:
				ret.ZeroStart = True;
			elif features[i] == TrackFeatures.remount:
				ret.Remount = True;
			elif features[i] == TrackFeatures.frictionless:
				ret.frictionless = True;
			else:
				raise Exception("Unsupported feature");
		if (supports61):
			# this is useless to because this isn't actually LRA 
			# so physics doesnt matter
			ret.ver = 61;
		else:
			ret.ver = 62;
		
		if (songinfo):
			song = br.ReadStringSingleByteLength();
			try:
				pass
				#print("Song found but not required to be parsed")
				#strings = list(filter(None, song.split("\r\n")));
				#print(strings)
			except:
				pass

		ret.StartOffset = Vector2d(br.ReadDouble(), br.ReadDouble());
		lines = br.ReadInt32();
		#print("Lines:",lines)
		linetriggers = []
		for i in range(lines):
			#GameLine l;
			ltype = int.from_bytes(br.ReadByte(), byteorder);
			lt = ltype & 0x1F
			#print("LineType:",lt)
			inv = (ltype >> 7) != 0;
			lim = (ltype >> 5) & 0x3;
			ID = -1;
			prvID = -1;
			nxtID = -1;
			multiplier = 1;
			linewidth = 1.0
			tr = None
			if (redmultipier):
				if (lt == LineType.Red):
					multiplier = int.from_bytes(br.ReadByte(), byteorder);
			if (lt == LineType.Blue or lt == LineType.Red):
				if (ignorabletrigger):
					# Read trigger and store as dictionary
					tr = {}
					zoomtrigger = br.ReadBoolean();
					if (zoomtrigger):
						tr["ZoomTrigger"] = True;
						target = br.ReadSingle();
						frames = br.ReadInt16();
						tr["ZoomFrames"] = frames;
						tr["ZoomTarget"] = target;
					else:
						tr = None;
				ID = br.ReadInt32();
				if ID > ret.current_id:
					ret.current_id = ID
				#print("ID:",ID)
				if (lim != 0):
					prvID = br.ReadInt32();# ignored
					nxtID = br.ReadInt32();# ignored
			if (lt == LineType.Scenery):
				if (scenerywidth):
					b = int.from_bytes(br.ReadByte(), byteorder);
					linewidth = b / 10.0
			x1 = br.ReadDouble();
			y1 = br.ReadDouble();
			x2 = br.ReadDouble();
			y2 = br.ReadDouble();
			#print(x1,y1,x2,y2)
			if (tr != None):
				tr["LineID"] = ID;
				linetriggers.append(tr);
			if lt == LineType.Blue:
				ret.addLine(Line(lt, Vector2d(x1, y1), Vector2d(x2, y2), ID=ID, inv=inv, Extension=lim))
			elif lt == LineType.Red:
				if (redmultipier):
					ml = multiplier;
				else:
					ml = 0
				ret.addLine(Line(lt, Vector2d(x1, y1), Vector2d(x2, y2), ID=ID, inv=inv, Extension=lim, Multiplier=ml))
			elif lt == LineType.Scenery:
				ret.addLine(Line(lt, Vector2d(x1, y1), Vector2d(x2, y2), width=linewidth))
			else:
				raise Exception("Invalid line type at ID " + str(ID));
			#if (l["type"] == "StandardLine"):
				#if (l["ID"] not in list(addedlines.keys())):
				#addedlines[ID] = l;
				#ret.lines.append(l);
			#else:
				#pass
				#ret.lines.append(l);
			#print(l)
		
		ret.Triggers = linetriggers
		if (br.base_stream.tell() != len(_bytes)):
			meta = br.ReadBytes(4);
			#print(meta)
			if (meta == b"META"):
				ret = ParseMetadata(ret, br);
			else:
				raise Exception("Expected metadata tag but got " + str(meta));
		return ret;

def ReadString(br):
		return br.ReadBytes(br.ReadInt16()).decode("ascii")