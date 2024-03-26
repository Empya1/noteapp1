import sqlite3
from sqlite3 import Error

# database class
class Database:
	def __init__(self, name): 
	
		"""name of database"""
		self.name = name
		# creating connection
		self.conn = sqlite3.connect(f"{self.name}.db")
		#cursor object
		self.cursor = None
		
	#create table method
	"""
	create_table(TABLE_NAME, "COLUMN_NAME WITH SQL ARGS")
	
	create_table(string, strings)
	
	"""
	
	def op(self): 
		self.conn = sqlite3.connect(f"{self.name}.db")
		#cursor object
		self.cursor = self.conn.cursor()
		
	def close(self): 
		self.conn.close()
	
	def create_table(self, *args):
		self.op()
		self.cursor = self.conn.cursor()
		#print("create_table(table_name)")
		
		#function to create and return sql
		def make_sql(a, b):
		
			sql = f"""
		CREATE TABLE IF NOT EXISTS  {a}(
		
		{b}
		)
		"""
			return sql
			
		# get table name and leave args
		
		p = """
		"""
		length = len(args)
		
		all_args = list(args)	
		
		tn = all_args[0]
		
		all_args.remove(tn)
		
		
		for any in all_args: 
			p += any
		
		try:
			self.cursor.execute(make_sql(tn, p))
			self.conn.commit()
			#print("TABLE CREATED SUCCESSFULLY")
		
			
		except Error as e:
			
			#print("TABLE CREATION FAILED")
			#print(e)
			"""pass"""
			
		self.close()
			
	
	#Insert method
	"""
	
	insert(TABLE_NAME, [(COLUMN1_VALUE, COLUMN2_VALUE, COLUMN3_VALUE....)])
	
	insert(string, list)
	
	"""
			
	def insert(self, *args): 
		self.op()
	
		"""insert(
		table_name, 
		[ (value1, value2, value3, ......),  (value1, value2, value3, ......)]
		"""
		
		all_args = list(args)
		
		tn = all_args[0]
		
		records_list = args[1]
		
		for record in records_list:  
			sql = f"""
		
		INSERT INTO {tn} VALUES {record}
		
		"""
			try:
				self.cursor.execute(sql)
				self.conn.commit()
				#print("Records inserted")
				
				
			except Error as e: 
				#print("Error inserting records") 
				#print(e)
				#print("Check your records")
				pass
				
			self.close()
				
	def select_all(self,tn): 
		#print("select_all(table_name)")
		self.op()
		data = self.cursor.execute(f"""
		
		SELECT * FROM {tn}
		
		""")
		
			
		self.conn.commit()
		
		b = self.cursor.fetchall()
		
		#print(b)
		self.close()
			
		return b
		
	def get_column(self, table_name, col): 
	
		"""get_column(
		table_name, 
		str : column or column_name
		)"""
		self.op()
	
		
		sql = f"""
		SELECT {col} FROM {table_name}
		"""
		try:
			self.cursor.execute(sql)		
			self.conn.commit()
			#print("getting  %s column from %s table"%(col,table_name))
			
			columns = self.cursor.fetchall()
			
			return columns
			
		except Error as e: 
			#print("Failed to get column") 
			#print(e) 
			#print("Check if column or table actually exists")
			return int(0)
			
		self.close()
			
	def get_row_by_value(self, tn, col, value): 
		self.op()
	
		"""
		
		get_row(
		str : table_name, 
		
		str: column or column name ,
		
		value
		)
		
		"""
	
		colnames = []
		
		ROWS = []
	
		all = self.select_all(tn)
		#print(all)
		
		for any in self.cursor.description: 
			#print(any[0])
			colnames.append(any[0])
			
		indx = colnames.index(col)
		
		for row in all: 
			if row[indx] == value: 
				ROWS.append(row)
				
		self.close()
				
		return ROWS
				
	def update(self, *args): 
	
		self.op()
	
		
		"""
		update(
		table_name, 
		tuple : (column or column_name, value), 
		[ (column, new_value), (column, new_value) ]
		)
		"""
		
		
		tn = args[0]
		condition = args[1]
		changes = args[2]
		
		for change in changes:
		
			sql = f"""
	
		UPDATE {tn} 
		SET {change[0]}  = ? WHERE  {condition[0]} = {condition[1]}
		
			"""
			
			#print(sql)
			
			try: 
				self.op()
				self.cursor.execute(sql, (change[1],))
				self.conn.commit()
				self.close()
				
				#print("Data Update Successful")
				
				
			except Error as e: 
				#print("Error updating Table")
				#print(e)
				pass
			
			self.close()
				
			
			
	def delete_specific(self,*args): 
		self.op()
	
		"""
		
		table_name, 
		
		[str:column, value]
		
		"""
		tn = args[0]
		condition = args[1]
		
		sql = f"""
		
		DELETE FROM {tn} WHERE {condition[0]} = ?
		
		"""
		
		try: 
			self.cursor.execute(sql, (condition[1],))
			self.conn.commit()
			#print("Deleted Successfully")
			
		except Error as e: 
			#print("Delete Failed") 
			#print(e)
			pass
			
		self.close()
			
	def delete_all(self, tn): 
		self.op()
		ids = self.get_column("Notes", "id")
		#print(ids)
		
		for id in ids:
			self.op()
			sql = f"""
			
			DELETE FROM {tn} WHERE id = {id[0]}
			
			"""
			
			try: 
				self.cursor.execute(sql)
				self.conn.commit()
				self.close()
				
			except Error as e: 
				print("Failed to delete all from table", e)
				
		
