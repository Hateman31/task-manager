import pyodbc

CONFIG_STR = (
	'DRIVER={SQL Server};'+
    'SERVER=localhost;'+
    'DATABASE=test_db;'+
	'UID=usr;'+
	'PWD=pswd'
)

TASKS = []

def sp_getTask(num = None):
	try:
		return TASKS[num]
	except IndexError:
		return None

def sp_getCCList(num = None):
	
	q = 'sp_getCCList ?'
	
	con = pyodbc.connect( CONFIG_STR)
	cur = con.cursor()
	cur.execute(q,num)
	
	table = [list(x) for x in cur.fetchall()]
	cols = [column[0] for column in cur.description]
	
	res = []
	for row in table:
		res += [{col:value for col,value in zip(cols,row)}]			
	
	return res

def sp_addAccessTask(form = {} ):
	
	con = pyodbc.connect( CONFIG_STR)

	cur = con.cursor()
	
	q = 'insert into mkt_extCC_project(ccid,project_id) values(?,?)'
	
	try:
		for cc_id in form['cc_list']:
			#~ print((cc_id,form['task_id']))
			cur.execute(q,(int(cc_id),form['task_id']))
			cur.commit()
	finally:	
		cur.close()
		con.close()

def createTask(form = {}):
	global TASKS
	#print(TASKS)
	TASKS += [{x:y for x,y in form.items()}]
	
def setTask(form = {}):
	
	fields = [
		'task_id',
		'name',
		'author',
		'client',
		'type',
	]
	
	q = 'sp_setTask ' + ','.join(['?' for x in fields])
	
	print(q)
	
	options = [form[field] for field in fields]
	
	con = pyodbc.connect(CONFIG_STR)
	
	cur = con.cursor()
	try:
		cur.execute(q,*options)
		cur.commit()
	finally:
		cur.close()
		con.close()
	
def sp_getLinks(num = None):
	
	q = 'sp_getLinksData ?'
	
	con = pyodbc.connect( CONFIG_STR)
	cur = con.cursor()
	cur.execute(q,num)
	
	table = [list(x) for x in cur.fetchall()]
	cols = [column[0] for column in cur.description]
	
	res = []
	for row in table:
		res += [{col.lower():value for col,value in zip(cols,row)}]			
	
	return res


def sp_getCCListByTask(num = None):
	q = 'sp_getCCListByTask ?'
	con = pyodbc.connect( CONFIG_STR)
	cur = con.cursor()
	cur.execute(q,num)
	
	table = [list(x) for x in cur.fetchall()]
	cols = [column[0] for column in cur.description]
	
	res = []
	for row in table:
		res += [{col.lower():value for col,value in zip(cols,row)}]			
	
	return res
	
def sp_delAccessTask(form = {} ):
	
	con = pyodbc.connect( CONFIG_STR)
	cur = con.cursor()
	
	q = 'sp_delAccessTask ?,?'
	
	for cc_id in form['cc_list']:
		print((form['project_id'],cc_id))
		cur.execute(q,(form['project_id'],int(cc_id)))
		cur.commit()
		
	cur.close()
	con.close()


def sp_getView(num = None):
	q = 'sp_getView ?'
	
	con = pyodbc.connect(CONFIG_STR)
	cur = con.cursor()
	cur.execute(q,num)
	
	lines = [list(x)[0] for x in cur.fetchall()]
	
	return lines

def getActiveTaskList():

	print(TASKS)
	return enumerate(TASKS)

if __name__ == '__main__':
	
	try:
		print(sp_getTask(490))
		print(sp_getTask(489))
		
	finally:
		
		q = ''' delete from mkt_ExtCC_Project
		where project_id = 1 '''
		
		con = pyodbc.connect(CONFIG_STR)
		cur = con.cursor()
		cur.execute(q)
		
		cur.commit()
		cur.close()
		con.close()
	
	
	
