
#Universidad del valle de Guatemala
#Josue Valenzuela 171001

import psycopg2 as sql
import os
from subprocess import call

"""
--Procedimiento almacenado Inciso 4
CREATE OR REPLACE PROCEDURE insert_PC(INT, FLOAT, FLOAT, FLOAT, FLOAT)
LANGUAGE plpgsql
AS $$
DECLARE
	found_model BOOL := False;
	model_number INT := $1;
BEGIN
	LOOP
		SELECT INTO found_model
		EXISTS(
		SELECT model FROM PC
		WHERE model = model_number);
		EXIT WHEN found_model = False;
		model_number = model_number + 1;
	END LOOP;

	INSERT INTO PC VALUES (model_number, $2, $3, $4, $5);
	INSERT INTO Product VALUES('unknown', model_number, 'PC');
	
END;
$$;
"""

class PC(object):
	"""
	"""
	__TRANS_READ = "BEGIN TRANSACTION READ ONLY ISOLATION LEVEL READ COMMITTED;"
	__TRANS_READ_WRITE = "BEGIN TRANSACTION READ WRITE ISOLATION LEVEL READ COMMITTED;"

	__GET_PC_BY_PRICE = """
					SELECT * FROM PC
					ORDER BY ABS(%s - price)
					LIMIT 1
				"""

	__GET_LAPTOP_MIN_REQ = """
						SELECT Product.model, ram, speed, hd, Laptop.price, Product.maker FROM Laptop
						JOIN Product 
						ON Product.model = Laptop.model
						WHERE ram >= %s AND speed >= %s AND hd >= %s
					"""

	__GET_PC_PRINTER_BUDGET = """
							SELECT PC.model, PC.speed, Printer.model, Printer.type, Printer.color, 
							(PC.price + Printer.price) AS total_price
							FROM PC, Printer
							WHERE (PC.price + Printer.price) <= %s;
							"""
	__INSERT_PC = "CALL insert_PC(%s,%s,%s,%s,%s);"

	__instance = None

	def __new__(cls, *args):
		"""
		"""
		if PC.__instance is None:
			PC.__instance = object.__new__(cls)
		return PC.__instance

	def __init__(self):
		"""
		"""
		try:
			self.__connection = sql.connect(user="omixggql",
											password = "VRj2fdOYyIq1V6eWOn--gQ0gBNAbzr0G",
											host= "isilo.db.elephantsql.com",
											port = "5432",
											database = "omixggql")
			self.__cursor = self.__connection.cursor()
		except Exception as e:
			raise e

	def __del__(self):
		self.__cursor.close()
		self.__connection.close()
		print("Close connection")

	def getPcByprice(self, price):
		"""
		"""
		self.__cursor.execute(self.__TRANS_READ)
		self.__cursor.execute(self.__GET_PC_BY_PRICE, (price,))
		self.__connection.commit()
		return self.__cursor.fetchone()

	def getLaptop(self, ram, speed, hd):
		"""
		"""
		self.__cursor.execute(self.__TRANS_READ)
		self.__cursor.execute(self.__GET_LAPTOP_MIN_REQ, (ram, speed, hd,))
		self.__connection.commit()
		return self.__cursor.fetchall()

	def getPcPrinter(self, max_budget, color):
		"""
		"""
		self.__cursor.execute(self.__TRANS_READ)
		self.__cursor.execute(self.__GET_PC_PRINTER_BUDGET, (max_budget,))
		self.__connection.commit()
		return self.__cursor.fetchall()

	def insertPC(self, model, speed, ram, hd, price):
		"""
		"""
		self.__cursor.execute(self.__TRANS_READ_WRITE)
		self.__cursor.execute(self.__INSERT_PC, (model, speed, ram, hd, price))
		self.__connection.commit()

	def getQuantityMinPrice(self, price):
		"""
		"""
		self.__cursor.execute(self.__TRANS_READ)
		self.__cursor.execute("SELECT count(*) FROM PC WHERE price > %s;", (price,))
		qt_PC = self.__cursor.fetchone()[0]
		self.__cursor.execute("SELECT count(*) FROM Laptop WHERE price > %s;", (price,))
		qt_Laptop = self.__cursor.fetchone()[0]
		self.__cursor.execute("SELECT count(*) FROM Printer WHERE price > %s;", (price,))
		qt_Printer = self.__cursor.fetchone()[0]
		self.__connection.commit()
		return (qt_PC, qt_Laptop, qt_Printer)


def main():
	"""
	"""
	db = PC()

	while True:
		call = os.system('clear') if os.name =='posix' else os.system('cls')
		print("""
			-------------------- Menu Opciones --------------------
				1. Obtener PCs por precio
				2. Buscar Laptop
				3. Insertar PC nuevo
				4. Buscar combo PC + Printer
				5. Buscar PCs, Laptops y Printers por precio
				6. Salir
			-------------------------------------------------------
		""")

		opt =input("Ingrese una opcion: ")
		call = os.system('clear') if os.name =='posix' else os.system('cls')

		if opt == "6":
			break

		elif opt == "1":
			while True:
				price = input("Ingresar precio: ")
				try:
					price = float(price)
					break
				except:
					print("Ingresar valor valido!")
			results = db.getPcByprice(price)
			print("Modelo: %d | Speed: %f | RAM %f | HD: %f | Price: %f" % (results))
			input("Presiona enter para regresar al menu principal")

		elif opt == "2":
			while True:
				try:
					speed = input("Ingrese speed: ")
					speed = float(speed)
					ram = input("Ingrese RAM: ")
					ram = float(ram)
					hd = input("Ingrese HD: ")
					hd = float(hd)
					break
				except:
					print("Ingrese valor valido!")
			results = db.getLaptop(ram, speed, hd)
			for result in results:
				print("Model: %s Ram: %s Speed: %s HD: %s Price: %s Maker: %s" % result)
			input("Presiona enter para regresar al menu principal")

		elif opt == "3":
			while True:
				budget = input("Ingresar presupuesto: ")
				try:
					budget = float(budget)
					break
				except:
					print("Ingresar valor valido!")
			results = db.getPcPrinter(budget, True)
			for result in results:
				print("PC Model: %s PC Speed: %s Printer Model: %s Printer Type: %s Color: %s Precio Combo: %s" % result)
			input("Presiona enter para regresar al menu principal")

		elif opt == "4":
			while True:
				try:
					model = input("Ingrese model: ")
					model = int(model)
					speed = input("Ingrese speed: ")
					speed = float(speed)
					ram = input("Ingrese RAM: ")
					ram = float(ram)
					hd = input("Ingrese HD: ")
					hd = float(hd)
					price = input("Ingrese price: ")
					price = float(price)
					break
				except:
					print("Ingresar valor valido!")
			db.insertPC(model, speed, ram, hd, price)
			print("PC guardada...\n")
			input("Presiona enter para regresar al menu principal")

		elif opt == "5":
			while True:
				price = input("Ingresar precio: ")
				try:
					price = float(price)
					break
				except:
					print("Ingresar valor valido!")
			results = db.getQuantityMinPrice(price)
			print("| PC: %s | Laptop: %s| Printer: %s |" % (results))
			input("Presiona enter para regresar al menu principal")

		else:
			print("Ingresevalor valido!!!")
			input("Ok")


if __name__ == '__main__':
	main()
