from lru_cache import *


c = LRUCache(2); c.put(1,1); c.put(2,2); assert c.get(1)==1; c.put(3,3); assert c.get(2)==-1; c.put(4,4); assert c.get(1)==-1; assert c.get(3)==3; assert c.get(4)==4

c = LRUCache(1); c.put(2,1); assert c.get(2)==1; c.put(3,2); assert c.get(2)==-1; assert c.get(3)==2

c = LRUCache(2); assert c.get(2)==-1; c.put(2,6); assert c.get(1)==-1; c.put(1,5); c.put(1,2); assert c.get(1)==2; assert c.get(2)==6