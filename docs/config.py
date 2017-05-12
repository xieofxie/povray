import os, platform
import numpy as np

def ResolveArgs(args):
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

def GetMatrix44Declare(matrix, prefix):
  val = ''
  for i in range(0,4):
    for j in range(0,3):
      val += ' Declare=%s%d%d=%f' % (prefix,i,j,matrix[i][j])
  return val

def GetVector3Declare(vector, prefix):
  val = ''
  for i in range(0,3):
    if i == 0:
      val += ' Declare=%s%d=%f' % (prefix,i,-vector[i])
    else:
      val += ' Declare=%s%d=%f' % (prefix,i,vector[i])
  return val

def Output(args, pose, id, name):
  location = GetVector3Declare(pose[0],'val_loc')
  look_at = GetVector3Declare(pose[2],'val_look')
  sky = GetVector3Declare(pose[3],'val_sky')
  right = ' Declare=val_right0=%f' % args.wh
  angle = ' Declare=val_angle=%f' % args.a
  val = location + look_at + sky + right + angle
  output = os.path.join(args.output,'%d-%s.png' % (id,name))
  a = (args.e,args.file,output,args.ow,args.oh,args.i,args.q,val)
  cmd = '%s +I%s +O%s +W%d +H%d +FN16 +wt1 -d %s Declare=use_baking=2 +A0.0 Quality=%d %s' % a
  #print(cmd)
  os.system(cmd)

def GetTranslationArray(vec):
  a = np.identity(4)
  for i in range(0,3):
    a[i][3] = vec[i]
  return a