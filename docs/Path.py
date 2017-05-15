import math
import numpy as np
from pyquaternion import Quaternion
from Math import GetTranslationArray, GetPos, GetQuat
import xml.etree.ElementTree as ET

class PathData:
	def __init__(self, pos, quat):
		self.pos = pos
		self.posMatrix = GetTranslationArray(self.pos)
		self.quat = quat
		self.quatMatrix = self.quat.transformation_matrix

class Path:
	def __init__(self, file):
		# TODO simply save them
		self.paths = []
		doc = ET.parse(file)
		for path in doc.getroot():
			if path.attrib['type'] == 'linear':
				self.HandleLinear(path)

	def GetData(self, id):
		return self.paths[id]

	def HandleLinear(self, node):
		poses = []
		quats = []
		steps = []
		for pos in node.findall('pos'):
			poses.append(GetPos(pos.text))
		for quat in node.findall('quat'):
			quats.append(GetQuat(quat.text))
		for step in node.findall('step'):
			step = int(step.text)
			steps.append(step)
		for i in range(0,len(steps)):
			for j in range(0,steps[i]):
				rate = float(j)/(steps[i]-1)
				pos = poses[i]*(1-rate) + poses[i+1]*rate
				if quats[i] == quats[i+1]:
					quat = quats[i]
				else:
					# TODO a bug?
					quat = Quaternion.slerp(quats[i],quats[i+1],rate)
				self.Add(pos,quat)
		if len(steps) == 0:
			self.Add(poses[0],quats[0])

	def Add(self, pos, quat):
		self.paths.append(PathData(pos, quat))

	def GetSize(self):
		return len(self.paths)
