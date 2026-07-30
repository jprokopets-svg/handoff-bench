from median_stream import *


mf = MedianFinder(); mf.add_num(1); mf.add_num(2); assert mf.find_median() == 1.5

mf = MedianFinder(); mf.add_num(1); assert mf.find_median() == 1.0

mf = MedianFinder(); mf.add_num(1); mf.add_num(2); mf.add_num(3); assert mf.find_median() == 2.0