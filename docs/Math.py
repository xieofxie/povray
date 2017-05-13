import numpy as np
from pyquaternion import Quaternion

def GetTranslationArray(vec):
	a = np.identity(4)
	for i in range(0,3):
		a[i][3] = vec[i]
	return a

def GetArray(str):
	str = str.split(',')
	for i in range(0,len(str)):
		str[i] = float(str[i])
	return str

def GetPos(str):
	return np.array(GetArray(str))

def GetQuat(str):
	return Quaternion(GetArray(str))