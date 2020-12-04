import time 
from multiprocessing import Pool
from anim import *


p = Pool()
result = p.map(zitrus_anim,None)
p.close()
p.join()