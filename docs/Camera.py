import xml.etree.ElementTree as ET
import numpy as np
from pyquaternion import Quaternion
from Math import GetTranslationArray, GetPos, GetQuat, GetArray

CameraID = 0

class CameraData:
  def __init__(self, args, camera):
    # config
    global CameraID
    if 'name' in camera.attrib:
      self.name = camera.attrib['name']
    else:
      self.name = 'unnamed-%d' % CameraID
      CameraID += 1
    self.type = camera.attrib.get('type','normal')
    self.wh = float(camera.attrib.get('wh',args.wh))
    self.a = float(camera.attrib.get('a',args.a))
    self.oh = int(camera.attrib.get('oh',args.oh))
    self.ow = int(camera.attrib.get('ow',args.ow))
    self.q = int(camera.attrib.get('q',args.q))
    self.aa = float(camera.attrib.get('a',args.aa))
    noise = camera.find('noise')
    if noise != None:
      self.nt = int(noise.attrib['type'])
      self.np = GetArray(noise.text)
    else:
      self.nt = args.nt
      self.np = args.np
    # prepare str
    #http://vision.in.tum.de/data/datasets/rgbd-dataset/file_formats
    if self.type == 'depth':
      self.paramStr = ' +FNg Declare=use_depth=1'
    else:
      self.paramStr = ' +FN Declare=use_depth=0'
    a = (self.wh,self.a,self.oh,self.ow,self.q)
    self.paramStr += ' Declare=val_right0=%f Declare=val_angle=%f +H%d +W%d Quality=%d' % a
    if self.aa != 3.0:
      self.paramStr += ' +A%f' % self.aa
    if self.nt != 0:
      self.paramStr += ' +NT%d' % self.nt
      for i in range(0,len(self.np)):
        self.paramStr += ' +NP%s%f' %(chr(65+i), self.np[i])
    # data
    self.pos = GetPos(camera.find('pos').text)
    self.posMatrix = GetTranslationArray(self.pos)
    self.quat = GetQuat(camera.find('quat').text)
    self.quatMatrix = self.quat.transformation_matrix

class CameraPose:
  def __init__(self, cameraData, pathData):
    self.quat = pathData.quat * cameraData.quat
    self.pos = cameraData.posMatrix.dot(np.array([0,0,0,1]))
    self.pos = pathData.quatMatrix.dot(self.pos)
    self.pos = pathData.posMatrix.dot(self.pos)[:3]
    self.lookAt = self.quat.rotate(np.array([0,0,1])) + self.pos
    self.sky = self.quat.rotate(np.array([0,1,0]))

class Camera:
  def __init__(self, args):
    self.cameras = []
    doc = ET.parse(args.camera)
    for camera in doc.getroot():
      self.cameras.append(CameraData(args, camera))

  def GetPose(self, id, pathData):
    return CameraPose(self.cameras[id], pathData)

  def GetData(self, id):
    return self.cameras[id]

  def GetSize(self):
    return len(self.cameras)
