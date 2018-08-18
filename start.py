from flask import Flask, request, render_template, url_for, redirect, send_file,abort
import utils

app = Flask(__name__)

@app.route("/",methods = ['GET','POST'])
def start():
    
    if request.method == 'POST':
        num = request.form['num']
        if num:
            return redirect(url_for('getTask',num = num))
        else:
            return render_template("error.html")
    
    task_list = utils.getActiveTaskList()
    return render_template("choice.html",task_list=task_list)
    #try:
        #task_list = utils.getActiveTaskList()
        #return render_template("choice.html",task_list=task_list)
    #except:
        #return render_template("error.html")

@app.route("/<int:num>",methods = ['GET','POST'])
def getTask(num = None):
    
    if request.method == 'POST':
        form = {}
        form['Project_ID'] = num
        for field in request.form:
            form[field] = request.form[field]
        utils.setTask(form)
        
    try:
        task_options = utils.sp_getTask(num)
        return render_template (
            'task.html',
            task_options = task_options,
            num = num
        )
    except:
        return render_template("error.html")
    
@app.route("/edit/<int:num>",methods = ['GET','POST'])
def editTask(num = None):
    
    if request.method == 'POST':
        form = {}
        form['task_id'] = num
        for field in request.form:
            form[field] = request.form[field]
        utils.setTask(form)
        
    task_options = utils.sp_getTask(num)
    
    return render_template (
        'edit.html',
        task_options = task_options,
        num = num
    )
    
@app.route("/access/<int:num>",methods = ['GET','POST'])
def getAccess(num = None):
    
    if request.method == 'POST':
        form = {}
        form['task_id'] = num
        form['cc_list'] = [x for x in request.form]
        utils.sp_addAccessTask(form)
        return redirect(url_for('getTask',num = num))
        
    cc_list = utils.sp_getCCList(num)
    return render_template (
        'access.html',
        cc_list = cc_list,
        num = num
    )   

@app.route("/new",methods = ['GET','POST'])
def newTask():
    if request.method == 'POST':
        utils.createTask(request.form)
        return redirect(url_for('start'))
    
    return render_template('new.html')

@app.route("/access/link/<int:num>")
def getLinks(num = None):
    
    cc_data = utils.sp_getLinks(num)
    
    return render_template(
        'link.html',
        cc_data = cc_data,
        num = num
    )

@app.route("/access/del/<int:num>",methods = ['GET','POST'])
def delAccess(num = None):
    
    if request.method == 'POST':
        
        form = {}
        form['project_id'] = num
        
        form['cc_list'] = [x for x in request.form]
        
        utils.sp_delAccessTask(form)
        
        return redirect(url_for('getTask',num = num))
        
    cc_list = utils.sp_getCCListByTask(num)
    
    #~ return str(cc_list)
    
    return render_template (
        'access.html',
        cc_list = cc_list,
        num = num
    )   


@app.route("/get_view/<int:num>")
def get_view(num = None):
    try:
        lines = utils.sp_getView(num)
    
        if lines:
            with open('temp.sql','w') as f:
                for line in lines:
                    f.write(line.replace('\r',''))  
            
            file_name = '{}.sql'.format(num)
            
            return send_file('temp.sql',
                attachment_filename= file_name,
                 as_attachment=True)
        else:
            return render_template("error.html")
    except:
        return render_template("error.html")

@app.route("/copy/<int:num>",methods = ['GET','POST'])
def copyTask(num = None):
    
    if request.method == 'POST':
        
        form = {}
        target = request.form['target']
        form['source'] = num
        
        for field in request.form:
            form[field] = request.form[field]
        
        try:
            utils.copyTask(form)
        except:
            return render_template("error.html")
            
        if target:
            return redirect(url_for('editTask',num = int(target)))
        else:
            return render_template("error.html")
        
    task_options = utils.sp_getTask(num)
    
    return render_template (
        'copy.html',
        task_options = task_options,
        num = num
    )
        
if __name__ == "__main__":
    app.run(debug = True)
