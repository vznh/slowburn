"""
This is a Python function that calls multiple different functions from different areas.
This is to showcase how deep **splat** could dive into your repository and help solve.
"""
# [START demo/foo.py]
from top.a import func_a
from top.b import func_b
from top.c import func_c

def foo():
  func_a() # This calls func_x, func_y, func_z
  func_b() # This calls func_i, func_j; j calls func_d
  func_c() # This calls func_j, func_k

foo()
