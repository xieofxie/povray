import os

paths = {
  'jni':['../../../../../../',
  'docs/IDE/app/src/main/jni/'],
  'prebuilt':['../../../../',
  'docs/IDE/prebuilt/include/']
}

folders = [
['jni','source','source'],
['prebuilt','libraries/boost','boost'],
['prebuilt','libraries/png','png'],
['jni','vfe','vfe']
]

for f in folders:
  path = paths[f[0]]
  src = path[0] + f[1]
  dst = path[1] + f[2]
  os.system('rm %s' % dst)
  os.system('ln -s %s %s' % (src, dst))
