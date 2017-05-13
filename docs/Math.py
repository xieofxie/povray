import numpy as np

def GetTranslationArray(vec):
  a = np.identity(4)
  for i in range(0,3):
    a[i][3] = vec[i]
  return a