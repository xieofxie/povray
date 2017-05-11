#!/usr/bin/python3

import os, argparse, platform
import numpy as np
#https://github.com/moble/quaternion
import quaternion

parser = argparse.ArgumentParser(description='run many povray calls')
parser.add_argument('file',help='pov file')
parser.add_argument('output',help='output prefix')
parser.add_argument('-e',help='povray executable or project path')
parser.add_argument('-i',default=[],nargs='*',help='''
  included path. automatically include pov file's folder.
  if e is project path, also project/include
  ''')
parser.add_argument('-oh',type=int,default=128,help='output height')
parser.add_argument('-ow',type=int,default=128,help='output width')
args = parser.parse_args()
print(args)

# handle executable
if not args.e:
  # TODO use povray from environment
  args.e = os.getcwd()
if os.path.isdir(args.e):
  args.i.append(os.path.join(args.e,'include'))
  args.i.append(os.path.join(args.e,'distribution/include'))
  if platform.system() == 'Lunux':
    args.e = os.path.join(args.e,'unix/povray')
  elif platform.system() == 'Windows':
    args.e = os.path.join(args.e,'windows/vs10/bin32/povconsole32.exe')
# handle file
args.i.append(os.path.dirname(os.path.abspath(args.file)))
# handle inc
incPath = ''
for inc in args.i:
  incPath += ' +L%s' % inc
args.i = incPath

def Matrix2Val(matrix):
  val = ''
  for i in range(0,4):
    for j in range(0,3):
      val += ' Declare=val%d%d=%f' % (i,j,matrix.getA()[i][j])
  return val

def Output(args,matrix):
  val = Matrix2Val(matrix)
  cmd = '%s +I%s +O%s +W%d +H%d +FN16 +wt1 -d %s Declare=use_baking=2 +A0.0 %s' % (args.e,args.file,args.output,args.ow,args.oh,args.i,val)
  print(cmd)
  os.system(cmd)

matrix0 = np.matrix([
[-0.999762,0,0.0217992,0],
[0,1,0,0],
[-0.0217992,0,-0.999762,0],
[1.3705,1.51739,1.44963,1]
])
print(matrix0)
matrixI = np.matrix(np.identity(4))
print(matrixI)
Output(args,matrix0)

