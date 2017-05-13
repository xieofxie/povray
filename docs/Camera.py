import xml.etree.ElementTree as ET
import numpy as np
from pyquaternion import Quaternion
from Math import GetTranslationArray, GetPos, GetQuat

class Camera:
  def __init__(self, file):
    self.total = 0
    self.names = []
    self.poses = []
    self.posMatrices = []
    self.quats = []
    self.quatMatrices = []
    doc = ET.parse(file)
    for camera in doc.getroot():
      self.total += 1
      name = camera.attrib["name"]
      self.names.append(name)
      v = GetPos(camera.find('pos').text)
      self.poses.append(v)
      self.posMatrices.append(GetTranslationArray(v))
      q = GetQuat(camera.find("quat").text)
      self.quats.append(q)
      self.quatMatrices.append(q.transformation_matrix)
      #print(name,v,q)

  def GetPose(self, id, pose):
    qThis = pose[1] * self.quats[id]
    pThis = np.dot(pose[2],np.dot(pose[3],np.dot(self.posMatrices[id], np.array([0,0,0,1]))))[:3]
    lookAt = qThis.rotate(np.array([0,0,1])) + pThis
    sky = qThis.rotate(np.array([0,1,0]))
    return (pThis, qThis, lookAt, sky)

  def GetName(self, id):
    return self.names[id]
