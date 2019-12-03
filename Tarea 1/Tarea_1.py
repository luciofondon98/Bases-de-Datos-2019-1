import pyodbc
import random
import csv

meses = {'January': '01', 'February': '02',
		'March': '03', 'April': '04',
		'May': '05', 'June': '06',
		'July': '07', 'August': '08',
		'September': '09', 'October': '10',
		'November': '11', 'December': '12',	
										}
#Métodos utilizados para poblar los campos vacíos y arreglar ciertos strings que a veces tiran error cuando se quieren insertar dentro de una tabla

def fecha_aleatoria():
	lista_meses = ['January','February','March','April','May','June','July','August','September','October','November','December']
	mes = random.choice(lista_meses)
	dia = str(random.randint(1,28))
	if int(dia) < 10:
		dia = '0'+dia

	año = str(random.randint(2017,2020))
	return (dia+'/'+meses[mes]+'/'+año)

def arreglar_fecha(fecha,meses):
	lista = fecha.split(", ")
	mes = lista[0].split()[0] 
	dia = lista[0].split()[1] 
	año = lista[1]
	if int(dia) < 10:
		dia = '0'+dia

	return (dia	+'/'+meses[mes]+'/'+año)

def arreglar_nombre_comilla(nombre):
	return nombre.replace("'", " ")

def precio_aleatorio():
	precios_juegos = [4990,9990,14990,14990,19990,19990,25990,34990,34990,49990,59990]
	return random.choice(precios_juegos)

def stock_aleatorio():
	return random.randint(0,25)

def bodega_aleatorio():
	return random.randint(10,30)

def vendidos_aleatorio():
	return random.randint(0,50)

def ventas_globales_aleatorio():
	return random.randint(100,10000)

def rating_aleatorio():
	return random.randint(0,10)

#--------------------------------------------------------------------------------------------#

#Métodos para el CRUD

def CREATE(nombre,precio,stock,bodega,vendidos,generos,desarrolladores,publicadoras,exclusividad,fecha,ventas_globales,rating):
	query = '''
	INSERT INTO Vista_Join(Nombre_juego,Precio,Stock,En_bodega, vendidos,generos,desarrolladores, Publicadoras, Exclusividad, Fecha_Publicacion, Ventas_globales, Rating)
 	VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}',TO_DATE('{}','DD/MM/YY'),'{}','{}');
 	'''
	cursor.execute(query.format(nombre,str(precio),str(stock),str(bodega),str(vendidos),generos,desarrolladores,publicadoras,exclusividad,str(fecha),str(ventas_globales),str(rating)))
	connection.commit()


def actualizar_stock(id_producto,stock):
	string = '''SELECT en_Bodega
				FROM Vista_Join
				WHERE Id_juego = '{}';
				'''
	query = string.format(id_producto)
	cursor.execute(query)
	for row in cursor.fetchall():
		if stock >= int(row[0]):
			string_reponer = '''UPDATE Sansanoplay SET en_Bodega = 0
								WHERE Id_Juego = '{}';'''

			query = string_reponer.format(id_producto)
			cursor.execute(query)
			connection.commit()

			string_reponer = '''UPDATE Sansanoplay SET Stock = Stock + '{}'
								WHERE Id_juego = '{}';'''


			query = string_reponer.format(row[0],id_producto)
			cursor.execute(query)		
			connection.commit()
			print("\n\n---ADVERTENCIA: EL PRODUCTO DE ID {} QUEDÓ CON NULA RESERVA DE BODEGA, FAVOR DE REPONER---\n\n".format(id_producto))


		elif stock < int(row[0]):
			string_reponer = '''UPDATE Sansanoplay SET en_Bodega = en_Bodega - '{}'
								WHERE Id_Juego = '{}';'''

			query = string_reponer.format(stock,id_producto)
			cursor.execute(query)
			connection.commit()

			string_reponer = '''UPDATE Sansanoplay SET Stock = Stock + '{}'
								WHERE Id_juego = '{}';'''

			query = string_reponer.format(stock,id_producto)
			cursor.execute(query)
			connection.commit()


	connection.commit()


def revisar_bodega(id_producto):
	string = '''SELECT en_Bodega
				FROM Vista_Join
				WHERE Id_juego = '{}';
				'''
	query = string.format(id_producto)
	cursor.execute(query)
	for row in cursor.fetchall():
		if row[0] == 0:
			return 0

	connection.commit()

def revisar_stock(id_producto):
	string ='''SELECT Stock
			   FROM Vista_Join
			   WHERE Id_juego = '{}';
			   '''
	query = string.format(id_producto)
	cursor.execute(query)
	for row in cursor.fetchall():
		if row[0] - 1 < 10 and row[0] > 0:
			print("\n\n---ADVERTENCIA: STOCK CRÍTICO DE {}---\n\n".format(row[0]-1))
		elif row[0] == 0:
			return 0

	connection.commit()

def cinco_exclusivos_mas_caros():
	print( '''\n\n||||||||||5 EXCLUSIVOS MÁS CAROS|||||||||\n\n''' )
	query = '''SELECT * FROM cinco_exc_mas_caros
			   WHERE ROWNUM <= 5;'''

	cursor.execute(query)
	for row in cursor.fetchall():
			print('Nombre juego: '+ row[0])
			print('Precio: ' + str(int(row[1]))+ '\n')
			connection.commit()

def mas_ventas_locales_generos():
	print( '''\n\n||||||||||VENTAS LOCALES|||||||||\n\n''' )
	query = '''SELECT * FROM tres_gen_locales_mas_vendidos
			   WHERE ROWNUM <= 3;'''

	cursor.execute(query)
	for row in cursor.fetchall():
			print('Nombre género: '+ row[0])
			print('Cantidad de juegos vendidos localmente: ' + str(int(row[1]))+ '\n')

def mas_ventas_globales_generos():
	print( '''\n\n||||||||||VENTAS GLOBALES|||||||||\n\n''' )
	query = '''SELECT * FROM tres_gen_globales_mas_vendidos
			   WHERE ROWNUM <= 3;'''

	cursor.execute(query)
	for row in cursor.fetchall():
			print('Nombre género: '+ row[0])
			print('Cantidad de juegos vendidos globalmente: ' + str(int(row[1]))+ '\n')


def tres_desarrolladores_mas_ventas_locales():
	print( '''\n\n||||||||||3 DESARROLLADORES CON MÁS VENTAS LOCALES|||||||||\n''' )
	query = '''SELECT * FROM tres_desarr_locales_mas_vendidos
			   WHERE ROWNUM <= 5;'''

	cursor.execute(query)
	for row in cursor.fetchall():
			print('Nombre desarrollador: '+ row[0])
			print('Cantidad de juegos vendidos localmente: ' + str(int(row[1]))+ '\n')

def rating_exclusivos_fecha():
	print( '''\n\n||||||||||JUEGOS CON MEJOR RATING ORDENADOS POR FECHA DE LANZAMIENTO|||||||||\n\n''' )
	query = "SELECT * FROM rating_exclusivos_fecha;"

	cursor.execute(query)
	for row in cursor.fetchall():
			print('Nombre juego: '+ row[0])
			print('Fecha de Publicacion: ' + str(row[1]))
			print('Rating: ' + str(row[2]) + '\n')

#--------------------------------------------------------------------------------------------#


#Conexión a la BD

connection = pyodbc.connect('DSN=Lucio;DBQ=orcl;Uid=SYSTEM;Pwd=Picopico123')

cursor = connection.cursor()

#Creación de secuencias

secuenciaSansanoplay = "CREATE SEQUENCE aumentarIdSansanoplay START WITH 1;"
secuenciaNintendo = "CREATE SEQUENCE aumentarIdNintendo START WITH 1;"

cursor.execute(secuenciaSansanoplay)
cursor.execute(secuenciaNintendo)
connection.commit()

#Creación de tablas

Sansanoplay = '''CREATE TABLE Sansanoplay 
				(Id_juego int NOT NULL PRIMARY KEY,
				 Nombre_juego varchar2(100),
				 Precio integer, Stock integer, 
				 En_bodega integer, Vendidos integer)
				 '''

Nintendo = '''CREATE TABLE Nintendo 
			  (Id_juego int NOT NULL PRIMARY KEY,
			   Nombre_juego varchar2(100),
			   Generos varchar2(100), 
			   Desarrolladores varchar2(100), 
			   Publicadoras varchar2(100), 
			   Exclusividad Binary_Double, 
			   Fecha_Publicacion date, 
			   Ventas_globales integer, 
			   Rating integer)
			   '''

cursor.execute(Sansanoplay)
cursor.execute(Nintendo)
connection.commit()

#-----------------Creación de triggers para id de autoincremento------------------------#
cursor.execute("""CREATE OR REPLACE TRIGGER automaticidNintendo BEFORE INSERT ON Nintendo FOR EACH ROW BEGIN SELECT aumentarIdNintendo.nextval INTO:new.Id_juego FROM dual; END;""")
cursor.execute("""CREATE OR REPLACE TRIGGER automaticidSansanoplay BEFORE INSERT ON Sansanoplay FOR EACH ROW BEGIN SELECT aumentariDSansanoplay.nextval INTO:new.Id_juego FROM dual; END;""")
connection.commit()


#----------------------------------------------------------------------------------------#

#Abrimos el archivo
with open('Sansanoplay.csv') as csv_file: #Insercion de datos en tabla Sansanoplay con datos aleatorios
	csv_reader = csv.reader(csv_file)
	next(csv_reader)

	for linea in csv_reader:
		nombre_juego = linea[1]
		if "'" in nombre_juego: #Si hay una comilla simple, a veces tira error al insertar
			nombre_juego = arreglar_nombre_comilla(nombre_juego)

		precio = precio_aleatorio()
		stock = stock_aleatorio()
		en_bodega = bodega_aleatorio()
		vendidos = vendidos_aleatorio()
		query = '''INSERT INTO Sansanoplay(Nombre_juego, Precio, Stock, En_bodega, Vendidos) 
				   VALUES ('{}','{}','{}','{}','{}');
				   '''
		cursor.execute(query.format(nombre_juego,precio,stock,en_bodega,vendidos))

print("Cargando BD.\n")

#Abrimos el archivo
with open('Nintendo.csv','r') as csv_file:  #Insercion de datos en tabla Nintendo con datos aleatorios
	csv_reader = csv.reader(csv_file)
	next(csv_reader)
	for linea in csv_reader:
		nombre_juego = linea[1]
		if "'" in nombre_juego:
			nombre_juego = arreglar_nombre_comilla(nombre_juego)
		genero = linea[2]
		if "'" in genero:
			genero = arreglar_nombre_comilla(genero)
		desarrolladores = linea[3]
		if "'" in desarrolladores:
			desarrolladores = arreglar_nombre_comilla(desarrolladores)
		publicadoras = linea[4]
		if "'" in publicadoras:
			publicadoras = arreglar_nombre_comilla(publicadoras)

		fecha = linea[5]
		exclusividad = linea[6]
		if exclusividad == "Si":
			exclusividad = 1
		else:
			exclusividad = 0

		ventas_globales = ventas_globales_aleatorio()
		rating = rating_aleatorio()
		if ',' not in fecha:
			fecha = fecha_aleatoria()
		else:
			fecha = arreglar_fecha(fecha,meses)
			
		string = '''INSERT INTO Nintendo(Nombre_juego, Generos, Desarrolladores, Publicadoras, Exclusividad, Fecha_Publicacion, Ventas_globales, Rating) 
					VALUES ('{}','{}','{}','{}','{}',TO_DATE('{}','DD/MM/YY'),'{}','{}');
					'''
		query = string.format(nombre_juego,genero,desarrolladores,publicadoras,exclusividad,fecha,ventas_globales,rating)		
		cursor.execute(query)
		connection.commit()

#Creacion de las vistas, las cuales corresponden a las consultas que son requeridas para la tarea.
print("Cargando BD..\n")


vista = '''CREATE VIEW Vista_join AS
					SELECT Sansanoplay.Id_juego, Sansanoplay.Nombre_juego,
       				   Sansanoplay.Precio, Sansanoplay.Stock, Sansanoplay.en_bodega,
       				   Sansanoplay.Vendidos, Nintendo.Generos, Nintendo.Desarrolladores,
      				   Nintendo.Publicadoras, Nintendo.Exclusividad, Nintendo.Fecha_Publicacion,
      				   Nintendo.Ventas_globales, Nintendo.rating
				FROM Sansanoplay
    			INNER JOIN Nintendo ON Nintendo.Id_Juego = Sansanoplay.Id_juego;
		'''

cinco_exc_mas_caros = '''CREATE VIEW cinco_exc_mas_caros AS SELECT Nombre_Juego, Precio
FROM (SELECT Sansanoplay.Id_juego, Sansanoplay.Nombre_juego,	
       				   Sansanoplay.Precio, Sansanoplay.Stock, Sansanoplay.en_bodega,
       				   Sansanoplay.Vendidos, Nintendo.Generos, Nintendo.Desarrolladores,
      				   Nintendo.Publicadoras, Nintendo.Exclusividad, Nintendo.Fecha_Publicacion,
      				   Nintendo.Ventas_globales, Nintendo.rating FROM Sansanoplay INNER JOIN Nintendo ON Nintendo.Id_Juego = Sansanoplay.Id_juego)
WHERE Exclusividad = 1
ORDER BY Precio DESC;
		'''
tres_gen_locales_mas_vendidos = '''CREATE OR REPLACE VIEW tres_gen_locales_mas_vendidos AS SELECT Generos, SUM (vendidos)"Ventas Locales"
FROM (SELECT Sansanoplay.Id_juego, Sansanoplay.Nombre_juego,	
       				   Sansanoplay.Precio, Sansanoplay.Stock, Sansanoplay.en_bodega,
       				   Sansanoplay.Vendidos, Nintendo.Generos, Nintendo.Desarrolladores,
      				   Nintendo.Publicadoras, Nintendo.Exclusividad, Nintendo.Fecha_Publicacion,
      				   Nintendo.Ventas_globales, Nintendo.rating FROM Sansanoplay INNER JOIN Nintendo ON Nintendo.Id_Juego = Sansanoplay.Id_juego)
GROUP BY Generos
ORDER BY "Ventas Locales" DESC;
'''

tres_gen_globales_mas_vendidos = '''CREATE OR REPLACE VIEW tres_gen_globales_mas_vendidos AS SELECT Generos, SUM (ventas_globales)"Ventas Globales"
FROM (SELECT Sansanoplay.Id_juego, Sansanoplay.Nombre_juego,	
       				   Sansanoplay.Precio, Sansanoplay.Stock, Sansanoplay.en_bodega,
       				   Sansanoplay.Vendidos, Nintendo.Generos, Nintendo.Desarrolladores,
      				   Nintendo.Publicadoras, Nintendo.Exclusividad, Nintendo.Fecha_Publicacion,
      				   Nintendo.Ventas_globales, Nintendo.rating FROM Sansanoplay INNER JOIN Nintendo ON Nintendo.Id_Juego = Sansanoplay.Id_juego)
GROUP BY Generos
ORDER BY "Ventas Globales" DESC;
		'''
tres_desarr_locales_mas_vendidos = '''CREATE OR REPLACE VIEW tres_desarr_locales_mas_vendidos AS SELECT Desarrolladores, SUM (vendidos)"Ventas Locales"
FROM (SELECT Sansanoplay.Id_juego, Sansanoplay.Nombre_juego,	
       				   Sansanoplay.Precio, Sansanoplay.Stock, Sansanoplay.en_bodega,
       				   Sansanoplay.Vendidos, Nintendo.Generos, Nintendo.Desarrolladores,
      				   Nintendo.Publicadoras, Nintendo.Exclusividad, Nintendo.Fecha_Publicacion,
      				   Nintendo.Ventas_globales, Nintendo.rating FROM Sansanoplay INNER JOIN Nintendo ON Nintendo.Id_Juego = Sansanoplay.Id_juego)
GROUP BY Desarrolladores
ORDER BY "Ventas Locales" DESC;
'''

rating_exclusivos_fech = '''CREATE OR REPLACE VIEW rating_exclusivos_fecha AS SELECT Nombre_Juego, Fecha_Publicacion, Rating
FROM (SELECT Sansanoplay.Id_juego, Sansanoplay.Nombre_juego,	
       				   Sansanoplay.Precio, Sansanoplay.Stock, Sansanoplay.en_bodega,
       				   Sansanoplay.Vendidos, Nintendo.Generos, Nintendo.Desarrolladores,
      				   Nintendo.Publicadoras, Nintendo.Exclusividad, Nintendo.Fecha_Publicacion,
      				   Nintendo.Ventas_globales, Nintendo.rating FROM Sansanoplay INNER JOIN Nintendo ON Nintendo.Id_Juego = Sansanoplay.Id_juego)
                       
WHERE Rating = (SELECT MAX(Rating) FROM (SELECT Sansanoplay.Id_juego, Sansanoplay.Nombre_juego,	
       				   Sansanoplay.Precio, Sansanoplay.Stock, Sansanoplay.en_bodega,
       				   Sansanoplay.Vendidos, Nintendo.Generos, Nintendo.Desarrolladores,
      				   Nintendo.Publicadoras, Nintendo.Exclusividad, Nintendo.Fecha_Publicacion,
      				   Nintendo.Ventas_globales, Nintendo.rating FROM Sansanoplay INNER JOIN Nintendo ON Nintendo.Id_Juego = Sansanoplay.Id_juego))
ORDER BY Fecha_Publicacion DESC;
'''
cursor.execute(vista)
connection.commit()
cursor.execute(cinco_exc_mas_caros)
connection.commit()
cursor.execute(tres_gen_locales_mas_vendidos)
connection.commit()
cursor.execute(tres_gen_globales_mas_vendidos)
connection.commit()
cursor.execute(tres_desarr_locales_mas_vendidos)
connection.commit()
cursor.execute(rating_exclusivos_fech)
connection.commit()

#-----------------------------------------------Creación triggers para la vista------------------# 
print("Cargando BD...\n")

#Triggers creados para el CRUD

trigger_insert = ('''CREATE OR REPLACE TRIGGER Join_Insert
INSTEAD OF INSERT ON Vista_Join
FOR EACH ROW
BEGIN
    INSERT INTO Sansanoplay(Nombre_juego, Precio, Stock, En_bodega, Vendidos)
    VALUES (:NEW.Nombre_Juego,:NEW.Precio,:NEW.Stock,:NEW.En_bodega,:NEW.Vendidos);
    INSERT INTO Nintendo(Nombre_juego, Generos, Desarrolladores, Publicadoras, Exclusividad, Fecha_Publicacion, Ventas_globales, Rating)
    VALUES (:NEW.Nombre_Juego,:NEW.Generos,:NEW.Desarrolladores, :NEW.Publicadoras, :NEW.Exclusividad, :NEW.Fecha_Publicacion,
            :NEW.Ventas_globales ,:NEW.Rating);
END;''')

trigger_update = ('''CREATE OR REPLACE TRIGGER Join_Update
INSTEAD OF UPDATE ON Vista_Join
FOR EACH ROW
DECLARE
    bodega integer;
    old_stock integer;
BEGIN
    old_stock := :OLD.Stock;
    IF :NEW.Stock < old_stock THEN
        UPDATE Sansanoplay SET Stock = :NEW.Stock
        WHERE Id_Juego = :OLD.id_juego;
        UPDATE Nintendo SET Ventas_globales = Ventas_globales + 1
        WHERE Id_Juego = :OLD.id_juego;
        UPDATE Sansanoplay SET Vendidos = Vendidos + 1
        WHERE Id_Juego = :OLD.Id_juego;
    END IF;
    
    bodega := :OLD.En_bodega;
    IF :NEW.en_Bodega > bodega THEN
        UPDATE Sansanoplay SET En_bodega = :NEW.En_bodega
        WHERE Id_Juego = :NEW.id_juego;
    END IF;
    
    UPDATE Sansanoplay SET Precio = :NEW.Precio
    WHERE Id_juego = :NEW.Id_juego;
END;''')

trigger_delete = ('''CREATE OR REPLACE TRIGGER Join_Delete
INSTEAD OF DELETE ON Vista_Join
FOR EACH ROW
BEGIN
    DELETE FROM Sansanoplay WHERE id_juego= :OLD.Id_juego;
    DELETE FROM Nintendo WHERE id_juego= :OLD.Id_juego;
END;
''')

cursor.execute(trigger_insert)
connection.commit()
cursor.execute(trigger_update)
connection.commit()
cursor.execute(trigger_delete)
connection.commit()

#-----------------------------------------------#

#Menú CRUD

print("Se ha conectado exitosamente con el servidor de la base de datos.")
print("¡Bienvenido a la Base de Datos! ¿Qué deseas hacer?\n")

flag = True
while(flag):
	print('''Elige una opción:\n
	1)Acciones CRUD\n
	2)Mostrar los 5 exclusivos mas caros\n
	3)Mostrar los 3 géneros más vendidos localmente y globalmente\n
	4)Mostrar las 3 desarrolladoras con más ventas locales\n
	5)Mostrar los juegos con mejor rating ordenados por fecha de lanzamiento\n
	6)Salir\n''')

	opcion = int(input())

	if (opcion == 1):
	 	print("¿Que acción deseas realizar?\n1)CREATE\n2)UPDATE\n3)READ\n4)DELETE\n5)Volver al menú principal\n")
	 
	 	crud = int(input())
	 	if (crud == 1):
	 		n = str(input("Ingrese nombre del juego\n"))
	 		p = int(input("Ingrese precio del juego\n"))
	 		s = int(input("Ingrese la cantidad de copias en stock del juego\n"))
	 		en_b = int(input("Ingrese la cantidad de copias en bodega del juego\n"))
	 		v = int(input("Ingrese cantidad de copias vendidas del juego\n"))
	 		g = str(input("Ingrese género del juego\n"))
	 		d = str(input("Ingrese desarrolladores del juego\n"))
	 		pub = str(input("Ingrese las publicadoras del juego\n"))
	 		e = int(input("Ingrese la exclusividad del juego, 1 si es exlusivo y 0 si no lo es\n"))
	 		f = str(input("Ingrese fecha de lanzamiento del juego en formato DD/MM/AA\n"))
	 		vg = int(input("Ingrese las ventas globales del juego\n"))
	 		rat = int(input("Ingrese un rating del 0 al 10\n"))
	 		CREATE(n,p,s,en_b,v,g,d,pub,e,f,vg,rat)
	 		print("Datos cargados correctamente a la BD.\n\n")
	 		
	 	elif (crud == 2):
	 		opcion_update = int(input("¿Qué desea realizar?\n1)Realizar ventas\n2)Actualizar stock\n3)Actualizar bodega\n4)Actualizar precio de producto\n"))
	 		if (opcion_update == 1):
	 			cantidad = int(input("Indique cuántos productos procederá a vender\n"))

	 			if (cantidad == 1): 
	 				aidi = int(input("Ingrese el ID del producto a vender\n"))

	 				
	 				if (revisar_stock(aidi) == 0):
	 					print("\n\nNO HAY STOCK DISPONIBLE DEL PRODUCTO, FAVOR CHEQUEAR SU STOCK EN BODEGA (Opción 3 de Update)\n\n")
	 				else:
	 					string = '''UPDATE Vista_Join
	 							     	 SET Stock = Stock - 1
	 							     	 WHERE Id_Juego = {};'''

	 					query = string.format(aidi)
	 					cursor.execute(query)
	 					connection.commit()
	 					print("\n\nVenta realizada correctamente.\n\n")

	 			else:
	 				i = 0
	 				while (i < cantidad):
	 					aidi = int(input("Ingrese el ID del producto numero " + str(i + 1) +" a vender\n"))
	 					if (revisar_stock(aidi) == 0):
	 						print("\n\nNO HAY STOCK DISPONIBLE DEL PRODUCTO, FAVOR CHEQUEAR SU STOCK EN BODEGA\n\n")
	 						break
	 					else:
	 						string = '''UPDATE Vista_Join
	 							     	 SET Stock = Stock - 1
	 							     	 WHERE Id_Juego = {};'''
	 						query = string.format(aidi)
	 						cursor.execute(query)
	 						connection.commit()
	 						i += 1
	 						print("\n\nVenta realizada correctamente.\n\n")

	 		elif (opcion_update == 2):
	 			aidi = int(input("Ingrese el ID del producto que quiere actualizar stock\n"))
	 			cant_stock = int(input("Ingrese la cantidad de stock que quiere reponer\n"))
	 			if (revisar_bodega(aidi) == 0):
	 				print("\n\n---NO TIENES PRODUCTOS EN BODEGA, NO ES POSIBLE REPONER STOCK---\n\n")

	 			else:
	 				actualizar_stock(aidi,cant_stock)
	 				print("\n\nStock actualizado correctamente.\n\n")


	 		elif (opcion_update == 3):
	 			aidi = int(input("Ingrese el ID del producto que quiere actualizar bodega\n"))
	 			new_bodega = int(input("Ingrese la cantidad de producto en bodega que quiere reponer\n"))
	 			string = ('''UPDATE Vista_Join
							   SET En_bodega = En_bodega + '{}'
							   WHERE Id_Juego = '{}';
							  ''')
	 			query = string.format(new_bodega,aidi)
	 			cursor.execute(query)
	 			connection.commit()
	 			print("\n\nBodega actualizada correctamente.\n\n")

	 		elif (opcion_update == 4):
	 			aidi = int(input("Ingrese el ID del producto que quiere actualizar su precio\n"))
	 			new_precio = int(input("Ingrese el nuevo precio del juego\n"))
	 			string = ('''UPDATE Vista_Join
							   SET Precio = '{}'
							   WHERE Id_Juego = '{}';
							  ''')
	 			query = string.format(new_precio,aidi)
	 			cursor.execute(query)
	 			connection.commit()
	 			print("\n\nPrecio actualizado correctamente.\n\n")

	 	elif (crud == 3):
	 		aidi = int(input("Ingrese el ID del producto a leer\n"))
	 		string = ('''SELECT * FROM Vista_Join
						 WHERE Id_juego = '{}';
							''')	
	 		query = string.format(aidi)
	 		cursor.execute(query)
	 		for row in cursor.fetchall():
	 			print("\n\n")
	 			print("Nombre del juego: " + str(row[1]))
	 			print("\nPrecio: " + str(row[2]))
	 			print("\nStock: " + str(row[3]))
	 			print("\nEn bodega: " + str(row[4]))
	 			print("\nVendidos: " + str(row[5]))
	 			print("\nGenero: " + str(row[6]))
	 			print("\nDesarrolladores: " + str(row[7]))
	 			print("\nPublicadoras: " + str(row[8]))
	 			if (row[9] == 1):
	 				print("\nExclusividad del juego: Sí es exclusivo")
	 			else:
	 				print("\nExclusividad del juego: No es esclusivo")
	 			
	 			print("\nFecha de Publicación: " + str(row[10]))
	 			print("\nVentas globales: " + str(row[11]))
	 			print("\nRating: " + str(row[12]))
	 			print("\n\n")
	 			connection.commit()

	 	elif (crud == 4):
	 		cantidad = int(input("Indique cuántos productos procederá a eliminar\n"))
	 		if (cantidad == 1):
	 			aidi = int(input("Ingrese el ID del producto a eliminar\n"))
	 			string = ('''DELETE FROM Vista_Join
							 WHERE Id_Juego = '{}'
							  ''')
	 			query = string.format(aidi)
	 			cursor.execute(query)
	 			connection.commit()	
	 			print("\n\nProducto eliminado correctamente.\n\n")
	 			
	 		else:
	 			i = 0
	 			while (i < cantidad):
	 				aidi = int(input("Ingrese el ID del producto numero " + str(i + 1) +" a eliminar\n"))
	 				string = ('''DELETE FROM Vista_Join
							     WHERE Id_Juego = '{}'
							  ''')
	 				query = string.format(aidi)
	 				cursor.execute(query)
	 				connection.commit()
	 				i += 1
	 				print("\n\nProducto eliminado correctamente.\n\n")


	elif (opcion == 2):
		cinco_exclusivos_mas_caros()

	elif (opcion == 3):
		mas_ventas_locales_generos()
		mas_ventas_globales_generos()

	elif (opcion == 4):
		tres_desarrolladores_mas_ventas_locales()

	elif (opcion == 5):
		rating_exclusivos_fecha()

	elif (opcion == 6):
		flag = False

	else:
		print("Haz escogido una opción incorrecta\n")

#Borrar todo para poder ejecutarse las veces que se quiera


cursor.execute("DROP TABLE Sansanoplay;")
connection.commit()
cursor.execute("DROP TABLE Nintendo;")
connection.commit()
cursor.execute("DROP SEQUENCE aumentarIdSansanoplay;")
connection.commit()
cursor.execute("DROP SEQUENCE aumentarIdNintendo;")
connection.commit()
cursor.execute("DROP VIEW cinco_exc_mas_caros;")
connection.commit()
cursor.execute("DROP VIEW tres_gen_locales_mas_vendidos;")
connection.commit()
cursor.execute("DROP VIEW tres_gen_globales_mas_vendidos;")
connection.commit()
cursor.execute("DROP VIEW tres_desarr_locales_mas_vendidos;")
connection.commit()
cursor.execute("DROP VIEW rating_exclusivos_fecha;")
connection.commit()
cursor.execute("DROP VIEW Vista_Join;")
connection.commit()
print("Desconectado correctamente de la BD.")