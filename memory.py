#coding:utf-8
# 内存工具
import sys
import gc
from types import ModuleType, FunctionType


BLACKLIST = type, ModuleType, FunctionType
def getsize(obj, is_debug=False):
	"""sum size of object & members."""
	if isinstance(obj, BLACKLIST):
		raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
	seen_ids = set()
	size = 0
	objects = [obj]
	while objects:
		need_referents = []
		for obj in objects:
			if isinstance(obj, BLACKLIST):
				continue
			if id(obj) in seen_ids:
				continue
			temp_id, temp_size = id(obj), sys.getsizeof(obj)
			seen_ids.add(temp_id)
			size += temp_size
			if is_debug:
				print "obj: {0} id: {1} size: {2} seen: {3}".format(obj, id(obj), temp_size, seen_ids)
			need_referents.append(obj)
		objects = gc.get_referents(*need_referents)
	return size


class TestClass(object):
	__slots__ =  ("a", "b", "c")
	def __init__(self):
		self.a = 0
		self.b = 0
		self.c = 0


if __name__ == '__main__':
	t = TestClass()
	# print gc.get_referents(t)
	print sys.getsizeof(t)
	print getsize(t, True)