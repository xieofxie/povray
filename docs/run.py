import os, argparse, platform, math, time
from pyrr import Quaternion, Matrix44, Vector3
from Camera import Camera
from Path import Path
from Config import Config

parser = argparse.ArgumentParser(description='run many povray calls')
parser.add_argument('file',type=argparse.FileType('r'),help='pov file')
parser.add_argument('output',help='output prefix')
parser.add_argument('camera',type=argparse.FileType('r'),help='camera xml')
parser.add_argument('path',type=argparse.FileType('r'),help='path xml')
parser.add_argument('-e',help='povray executable or project path')
parser.add_argument('-i',default=[],nargs='*',help='''
  included path. automatically include pov file's folder.
  if e is project path, also project/include
  ''')
parser.add_argument('-wh',type=float,default=1,help='width height ratio, default 1')
parser.add_argument('-a',type=float,default=90,help='horizontal viewing angle, default 90')
parser.add_argument('-oh',type=int,default=32,help='output height, default 64')
parser.add_argument('-ow',type=int,default=32,help='output width, default 64')
parser.add_argument('-q',type=int,default=9,help='quality, default 9(0~11)')
parser.add_argument('-s',type=int,default=0,help='skip samples, default 0')
args = parser.parse_args()

config = Config(args)
#print(args)
camera = Camera(args.camera)
path = Path(args.path)

for i in range(0,path.total):
  pathPose = path.GetPose(i)
  config.PrepareID(i,pathPose)
  for j in range(0,camera.total):
    name = camera.GetName(j)
    camPose = camera.GetPose(j,pathPose)
    config.Output(camPose,name)
