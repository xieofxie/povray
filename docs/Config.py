import os, platform
import numpy as np
from pyquaternion import Quaternion

class Config:
  def __init__(self,args):
    self.args = args
     # handle executable
    if not args.e:
      # TODO use povray from environment
      args.e = os.getcwd()
    if os.path.isdir(args.e):
      args.i.append(os.path.join(args.e,'include'))
      args.i.append(os.path.join(args.e,'distribution/include'))
      if platform.system() == 'Linux':
        args.e = os.path.join(args.e,'unix/povray')
      elif platform.system() == 'Windows':
        args.e = os.path.join(args.e,'windows/vs10/bin32/povconsole32.exe')
    # handle file
    file = args.file.name
    args.file.close()
    args.file = file
    args.i.append(os.path.dirname(os.path.abspath(args.file)))
    # handle inc
    incPath = ''
    for inc in args.i:
      incPath += ' +L%s' % inc
    args.i = incPath
    # output params
    self.outputParams = open(args.output + 'params.txt','w+')

  def GetMatrix44Declare(self, matrix, prefix):
    val = ''
    for i in range(0,4):
      for j in range(0,3):
        val += ' Declare=%s%d%d=%f' % (prefix,i,j,matrix[i][j])
    return val

  def GetVector3Declare(self, vector, prefix):
    val = ''
    for i in range(0,3):
      if i == 0:
        val += ' Declare=%s%d=%f' % (prefix,i,-vector[i])
      else:
        val += ' Declare=%s%d=%f' % (prefix,i,vector[i])
    return val

  def Output(self, camPose, name):
    args = self.args
    if self.currentID >= args.s:
      location = self.GetVector3Declare(camPose[0],'val_loc')
      look_at = self.GetVector3Declare(camPose[2],'val_look')
      sky = self.GetVector3Declare(camPose[3],'val_sky')
      right = ' Declare=val_right0=%f' % args.wh
      angle = ' Declare=val_angle=%f' % args.a
      val = location + look_at + sky + right + angle
      # TODO any format one line
      output = os.path.join(args.output,'%d-%s.png' % (self.currentID,name))
      a = (args.e,args.file,output,args.ow,args.oh,args.i,args.q,val)
      cmd = '%s +I%s +O%s +W%d +H%d +FN16 +wt1 -d %s Declare=use_baking=2 +A0.0 Quality=%d %s' % a
      #print(cmd)
      os.system(cmd)
    self.OutputLine(name)
    self.OutputLine(camPose[0])
    self.OutputLine(camPose[1])
    self.outputParams.flush()

  def PrepareID(self,id,pathPose):
    self.currentID = id
    # TODO any format one like
    self.OutputLine(id)
    self.OutputLine(pathPose[0])
    self.OutputLine(pathPose[1])

  def Finish(self):
    self.outputParams.close()

  def OutputLine(self, value):
    if type(value) is np.ndarray:
      value = '%f %f %f' % (value[0],value[1],value[2])
    elif type(value) is Quaternion:
      #x,y,z,w
      value = '%f %f %f %f' %(value[1],value[2],value[3],value[0])
    elif not type(value) is str:
      value = str(value)
    self.outputParams.write(value)
    self.outputParams.write('\n')