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

class trackmetadata:
	def __init__(self):
		self.startzoom = "STARTZOOM";
		self.ygravity = "YGRAVITY";
		self.xgravity = "XGRAVITY";
		self.gravitywellsize = "GRAVITYWELLSIZE";
		self.bgcolorR = "BGCOLORR";
		self.bgcolorG = "BGCOLORG";
		self.bgcolorB = "BGCOLORB";
		self.linecolorR = "LINECOLORR";
		self.linecolorG = "LINECOLORG";
		self.linecolorB = "LINECOLORB";
		self.triggers = "TRIGGERS";

class triggertype:
	def __init__(self):
		self.Zoom = 0
		self.BGChange = 1
		self.LineColor = 2
