from binary import BinaryStream
from vector_2d import Vector as Vector2d
file = "1.trk"
byteorder = "little"
with open(file, "rb") as f:
	data = f.read()

class Track:
	def __init__(self):
		pass
class trackfeatures:
	def __init__(self):
		self.redmultiplier = "REDMULTIPLIER";
		self.scenerywidth = "SCENERYWIDTH";
		self.six_one = "6.1";
		self.songinfo = "SONGINFO";
		self.ignorable_trigger = "IGNORABLE_TRIGGER";
		self.zerostart = "ZEROSTART";
		self.remount = "REMOUNT";
		self.frictionless = "FRICTIONLESS";

class linetype:
	def __init__(self):
		self.Scenery = 0
		self.Blue = 1
		self.Red = 2

LineType = linetype()
TrackFeatures = trackfeatures()
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

''' do later
def ParseMetadata(ret, br):
{
	var count = br.ReadInt16();
	for (int i = 0; i < count; i++)
	{
		var metadata = ReadString(br).Split('=');
		switch (metadata[0])
		{
			case TrackMetadata.startzoom:
				ret.StartZoom = ParseFloat(metadata[1]);
				break;
			case TrackMetadata.ygravity:
				ret.YGravity = ParseFloat(metadata[1]);
				break;
			case TrackMetadata.xgravity:
				ret.XGravity = ParseFloat(metadata[1]);
				break;
			case TrackMetadata.gravitywellsize:
				ret.GravityWellSize = ParseDouble(metadata[1]);
				break;
			case TrackMetadata.bgcolorR:
				ret.BGColorR = ParseInt(metadata[1]);
				break;
			case TrackMetadata.bgcolorG:
				ret.BGColorG = ParseInt(metadata[1]);
				break;
			case TrackMetadata.bgcolorB:
				ret.BGColorB = ParseInt(metadata[1]);
				break;
			case TrackMetadata.linecolorR:
				ret.LineColorR = ParseInt(metadata[1]);
				break;
			case TrackMetadata.linecolorG:
				ret.LineColorG = ParseInt(metadata[1]);
				break;
			case TrackMetadata.linecolorB:
				ret.LineColorB = ParseInt(metadata[1]);
				break;
			case TrackMetadata.triggers:
				string[] triggers = metadata[1].Split('&');
				foreach (var t in triggers)
				{
					string[] tdata = t.Split(':');
					TriggerType ttype;
					try
					{
						ttype = (TriggerType)int.Parse(tdata[0]);
					}
					catch
					{
						throw new TrackIO.TrackLoadException(
							"Unsupported trigger type");
					}
					GameTrigger newtrigger;
					int start;
					int end;
					switch (ttype)
					{
						case TriggerType.Zoom:
							var target = ParseFloat(tdata[1]);
							start = ParseInt(tdata[2]);
							end = ParseInt(tdata[3]);
							newtrigger = new GameTrigger()
							{
								Start = start,
								End = end,
								TriggerType = TriggerType.Zoom,
								ZoomTarget = target,
							};
							break;
						case TriggerType.BGChange:
							var red = ParseInt(tdata[1]);
							var green = ParseInt(tdata[2]);
							var blue = ParseInt(tdata[3]);
							start = ParseInt(tdata[4]);
							end = ParseInt(tdata[5]);
							newtrigger = new GameTrigger()
							{
								Start = start,
								End = end,
								TriggerType = TriggerType.BGChange,
								backgroundRed = red,
								backgroundGreen = green,
								backgroundBlue = blue,
							};
							break;
						case TriggerType.LineColor:
							var linered = ParseInt(tdata[1]);
							var linegreen = ParseInt(tdata[2]);
							var lineblue = ParseInt(tdata[3]);
							start = ParseInt(tdata[4]);
							end = ParseInt(tdata[5]);
							newtrigger = new GameTrigger()
							{
								Start = start,
								End = end,
								TriggerType = TriggerType.LineColor,
								lineRed = linered,
								lineGreen = linegreen,
								lineBlue = lineblue,
							};
							break;
						default:
							throw new TrackIO.TrackLoadException(
								"Unsupported trigger type");
					}
					ret.Triggers.Add(newtrigger);
				}
				break;
		}
	}
}
'''

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
		print(features)
		if (version != 1):
			raise Exception("Unsupported version")
		redmultipier = False;
		scenerywidth = False;
		supports61 = False;
		songinfo = False;
		ignorabletrigger = False;
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
				print("Song found but not required to be parsed")
				#strings = song.Split(new string[] { "\r\n" }, StringSplitOptions.RemoveEmptyEntries);
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
				bl = {"typeName":"StandardLine","type":lt,"data":[Vector2d(x1, y1), Vector2d(x2, y2), inv]}
				bl["ID"] = ID;
				bl["Extension"] = lim;
				l = bl;
			elif lt == LineType.Red:
				rl = {"typeName":"RedLine","type":lt,"data":[Vector2d(x1, y1), Vector2d(x2, y2), inv]}
				rl["ID"] = ID;
				bl["Extension"] = lim;
				if (redmultipier):
					rl["Multiplier"] = multiplier;
				l = rl;
			elif lt == LineType.Scenery:
				l = {"typeName":"SceneryLine","type":lt,"data":[Vector2d(x1, y1), Vector2d(x2, y2)],"width":linewidth}
			else:
				raise Exception("Invalid line type at ID " + str(ID));
			if (l["type"] == "StandardLine"):
				#if (l["ID"] not in list(addedlines.keys())):
				addedlines[ID] = l;
				ret.lines.append(l);
			else:
				ret.lines.append(l);
		
		ret.Triggers = linetriggers
		if (br.base_stream.tell() != len(_bytes)):
			meta = br.ReadBytes(4);
			#print(meta)
			if (meta == b"META"):
				pass
				#ParseMetadata(ret, br);
			else:
				pass
				#raise Exception("Expected metadata tag but got " + str(meta));
		return ret;

def ReadString(br):
		return br.ReadBytes(br.ReadInt16()).decode("ascii")