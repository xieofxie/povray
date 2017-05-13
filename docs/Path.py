import math
import numpy as np
from pyquaternion import Quaternion
from Math import GetTranslationArray, GetPos, GetQuat
import xml.etree.ElementTree as ET

class Path:
	def __init__(self, file):
		self.total = 0
		# TODO simply save them
		self.poses = []
		self.quats = []
		self.posMs = []
		self.quatMs = []
		doc = ET.parse(file)
		for path in doc.getroot():
			if path.attrib['type'] == 'linear':
				self.HandleLinear(path)
		#print(self.poses,self.quats,self.total)

	def GetPose(self, id):
		return (self.poses[id],self.quats[id],self.posMs[id],self.quatMs[id])

	def HandleLinear(self, node):
		poses = []
		quats = []
		steps = []
		total = 0
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
				quat = Quaternion.slerp(quats[i],quats[i+1],rate)
				self.Add(pos,quat)

	def Add(self, pos, quat):
		self.poses.append(pos)
		self.quats.append(quat)
		self.posMs.append(GetTranslationArray(pos))
		self.quatMs.append(quat.transformation_matrix)
		self.total += 1