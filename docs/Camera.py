from xml.dom import minidom
import numpy as np
from pyquaternion import Quaternion
from Math import GetTranslationArray

class Camera:
  def __init__(self, file):
    self.total = 0
    self.names = []
    self.poses = []
    self.posMatrices = []
    self.quats = []
    self.quatMatrices = []
    doc = minidom.parse(file)
    cameras = doc.getElementsByTagName("camera")
    for camera in cameras:
      self.total += 1
      name = camera.getAttribute("name")
      self.names.append(name)
      pos = camera.getElementsByTagName("pos")[0].firstChild.data
      v = np.array(self.Convert(pos))
      self.poses.append(v)
      self.posMatrices.append(GetTranslationArray(v))
      quat = camera.getElementsByTagName("quat")[0].firstChild.data
      q = Quaternion(self.Convert(quat))
      self.quats.append(q)
      self.quatMatrices.append(q.transformation_matrix)
      #print(name,pos,quat)

  def GetPose(self, id, pose):
    #mFinal = self.quatMatrices[id] * self.posMatrices[id] * pose[3] * pose[2]
    qThis = pose[1] * self.quats[id]
    pThis = np.dot(pose[2],np.dot(pose[3],np.dot(self.posMatrices[id], np.array([0,0,0,1]))))[:3]
    qThisM = qThis.transformation_matrix
    lookAt = qThis.rotate(np.array([0,0,1])) + pThis
    sky = qThis.rotate(np.array([0,1,0]))
    return (pThis, qThis, lookAt, sky)

  def GetName(self, id):
    return self.names[id]

  def Convert(self, str):
    str = str.split(',')
    for i in range(0,len(str)):
      str[i] = float(str[i])
    return str
