
#Universidad del valle de Guatemala
#Josue Valenzuela 171001

import sqlite3 as sql

GET_PC_BY_PRICE = """
					SELECT * FROM pc
					ORDER BY ABS(%d - price)
					LIMIT 1
				"""

class PC(object):
	"""
	"""
	__instance = None

	@staticmethod 
	def getInstance():
		"""
		Static access method.
		"""
		if PC.__instance == None:
			PC()
		return PC.__instance

	def __init__(self, db_path):
		"""
		Virtually private constructor.
		"""
		if PC.__instance != None:
			print('Connection already created!!')
		else:
			PC.connection = sql.connect(db_path)
			PC.__instance = self

	

def main():
	print(GET_PC_BY_PRICE % (5))
if __name__ == '__main__':
	main()
