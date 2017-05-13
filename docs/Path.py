import math
import numpy as np
from pyquaternion import Quaternion
from Math import GetTranslationArray

class Path:
  def __init__(self, file):
    self.total = 3

  def GetPose(self, id):
    v = np.array([-1.5,1.5,1.5])
    q = Quaternion(axis=[0,0,1], radians=math.pi * 0.05 * id)
    vM = GetTranslationArray(v) 
    qM = q.transformation_matrix 
    return (v,q,vM,qM)
