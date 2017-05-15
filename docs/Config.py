import os, platform
import numpy as np
from pyquaternion import Quaternion

class Config:
  def __init__(self, args):
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
    a = (args.e,args.file,args.i)
    #-d Turns graphic display off
    #+A anti-aliasing setting
    # TODO remove use_baking
    self.cmdBase = '%s +I%s -d Declare=use_baking=2 +A0.0 %s' % a
    if args.t != 0:
      self.cmdBase += ' +WT%d' % args.t

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

  def Output(self, cameraPose, cameraData):
    args = self.args
    if self.currentID >= args.s:
      location = self.GetVector3Declare(cameraPose.pos,'val_loc')
      look_at = self.GetVector3Declare(cameraPose.lookAt,'val_look')
      sky = self.GetVector3Declare(cameraPose.sky,'val_sky')
      val = location + look_at + sky
      # TODO any format one like
      output = os.path.join(args.output,'%d-%s.png' % (self.currentID,cameraData.name))
      a = (self.cmdBase,output,val,cameraData.paramStr)
      cmd = '%s +O%s %s %s' % a
      #print(cmd)
      os.system(cmd)
    self.OutputLine(cameraData.name)
    self.OutputLine(cameraPose.pos)
    self.OutputLine(cameraPose.quat)
    self.outputParams.flush()

  def PrepareID(self,id,pathData):
    self.currentID = id
    # TODO any format one like
    self.OutputLine(id)
    self.OutputLine(pathData.pos)
    self.OutputLine(pathData.quat)

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
