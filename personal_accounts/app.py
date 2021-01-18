''' 
#Actividad : Proyecto final curso python UdeA
#Proyecto : Cuentas Personales
#Desarrollador : David A Torres Perez
#Fecha : Diciembre 2020
#Version 1
'''
#Libreiras
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import json

app = Flask(__name__)
#Conexion DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'accounts'
mysql = MySQL(app)
# Guardo la sesion
app.secret_key = "mysecretkey"
#Archivo principal de la raiz de la app
#Enrutammiento de toda la app
@app.route('/') 
def index():
    return render_template('index.html')
@app.route('/crear_cuentas')
def CrearCuenta():
    return render_template('crear_cuenta.html')
@app.route('/consultar_cuentas')
def ConsultaCuenta():
    return render_template('consultar_cuenta.html')
@app.route('/crear_ingreso')
def CrearIngreso():
    return render_template('crear_ingreso.html')
@app.route('/crear_egreso')
def CrearEgreso():
    return render_template('crear_egreso.html')        

#Acciones de la operaciones desde las vistas front-end para back-end -----------------------------------------------------------------
#Crear las una o varias cuentass
@app.route('/agregar_cuenta', methods=['POST'])
def AgregarCuenta():
    docutel = str(request.form['docutel'].strip())
    nomape = request.form['nomape'].upper()
    ingreso = request.form['ingreso']
    estado = 1
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cuenta (documento, nombre, ingreso, estado) VALUES (%s,%s,%s,%s)", (docutel, nomape, ingreso, estado))
    mysql.connection.commit()
    flash('La cuenta fue creada con exito y ya esta disponible para que hagas uso de ella')
    return redirect(url_for('CrearCuenta'))

#Consultar las cuentas activas e inactivas
@app.route('/consulta_ConsultaC_id/<int:documento>', methods = ['POST', 'GET'])
def ConsultaC_id(documento):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cuenta WHERE documento = %s AND estado=1 ORDER BY id DESC' , (documento,))
    data = cur.fetchall()
    cur.execute('SELECT * FROM cuenta WHERE documento = %s AND estado=0 ORDER BY id DESC' , (documento,))
    data2 = cur.fetchall()
    cur.close()
    return render_template('consultar_cuenta.html', cuentasact = data, cuentasinct = data2)

#Eliminar cuentas
@app.route('/eliminarCuenta/<int:id>/<int:documento>', methods = ['POST','GET'])
def Eliminar_Cuenta(id,documento):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM cuenta WHERE id = {0}'.format(id))
    cur.execute('DELETE FROM ingreso_variable WHERE id_cuenta = {0}'.format(id))
    cur.execute('DELETE FROM egreso_variable WHERE id_cuenta = {0}'.format(id))
    mysql.connection.commit()
    flash('Se elimina la cuenta {0} con exito!'.format(id))
    return redirect(url_for('ConsultaC_id',documento=documento))   

#Inactivas o activas cuentas
@app.route('/activaInactivaC/<int:id>/<int:documento>/<int:estado>', methods = ['POST','GET'])
def ActivaInactivaC(id,documento,estado):
    if estado==1:
        state = 0
    else:
        state = 1  
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE cuenta
        SET estado = %s
        WHERE id = %s
    """, (state,id))
    flash('El estado de la cuenta fue modificado correctamente')
    mysql.connection.commit()
    return redirect(url_for('ConsultaC_id',documento=documento))  

#Creo la insercion del ingreso
@app.route('/insertar_ingreso/<int:id_cuenta>/<string:descri_ingreso>/<string:fecha_ingreso>/<int:valor_ingreso>', methods = ['POST', 'GET'])
def InsertarIngreso(id_cuenta,descri_ingreso,fecha_ingreso,valor_ingreso):
    descri_ingreso = descri_ingreso.upper()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO ingreso_variable (id_cuenta, descripcion, valor, fecha) VALUES (%s,%s,%s,%s)", (id_cuenta, descri_ingreso, valor_ingreso, fecha_ingreso))
    mysql.connection.commit() 
    flash('El ingreso de la cuenta {0} se registra con exito'.format(id_cuenta))
    return redirect(url_for('CrearIngreso'))  
   
@app.route('/consultaringreso/<int:id_cuenta>', methods = ['POST','GET'])
def ConsultaIngreso(id_cuenta):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM ingreso_variable WHERE id_cuenta = %s  ORDER BY id DESC' , (id_cuenta,))
    data2 = cur.fetchall()
    cur.close()
    return render_template('consultar_ingresov.html', ingresosv = data2)

 #Creo la insercion del egreso
@app.route('/insertar_egreso/<int:id_cuenta>/<string:descri_egreso>/<string:fecha_egreso>/<int:valor_egreso>', methods = ['POST', 'GET'])
def InsertarEgreso(id_cuenta,descri_egreso,fecha_egreso,valor_egreso):
    descri_egreso = descri_egreso.upper()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO egreso_variable (id_cuenta, descripcion, valor, fecha) VALUES (%s,%s,%s,%s)", (id_cuenta, descri_egreso, valor_egreso, fecha_egreso))
    mysql.connection.commit() 
    flash('El Egreso de la cuenta {0} se registra con exito'.format(id_cuenta))
    return redirect(url_for('CrearEgreso'))  
   
@app.route('/consultaregreso/<int:id_cuenta>', methods = ['POST','GET'])
def ConsultaEgreso(id_cuenta):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM egreso_variable WHERE id_cuenta = %s  ORDER BY id DESC' , (id_cuenta,))
    data2 = cur.fetchall()
    cur.close()
    return render_template('consultar_egresov.html', egresov = data2)

#Ver la cuenta
@app.route('/ver_cuenta/<int:id_cuenta>', methods = ['POST', 'GET'])
def VerCuenta(id_cuenta):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cuenta WHERE id = %s  ORDER BY id DESC' , (id_cuenta,))
    data = cur.fetchall()
    cur.execute('SELECT id,descripcion,valor,fecha FROM ingreso_variable WHERE id_cuenta = %s  ORDER BY id DESC' , (id_cuenta,))
    data2 = cur.fetchall()
    cur.execute('SELECT sum(valor) as total FROM ingreso_variable WHERE id_cuenta = %s  ORDER BY id DESC' , (id_cuenta,))
    data3 = cur.fetchall()
    cur.execute('SELECT id,descripcion,valor,fecha FROM egreso_variable WHERE id_cuenta = %s  ORDER BY id DESC' , (id_cuenta,))
    data4 = cur.fetchall()
    cur.execute('SELECT sum(valor) as total FROM egreso_variable WHERE id_cuenta = %s  ORDER BY id DESC' , (id_cuenta,))
    data5 = cur.fetchall()
    cur.execute("""
        SELECT ingreso, 
        IFNULL((SELECT sum(valor) FROM ingreso_variable WHERE id_cuenta=cuenta.id),0) as total_ing_var,
        IFNULL((SELECT sum(valor) FROM egreso_variable WHERE id_cuenta=cuenta.id),0) as total_eng_var,
        (IFNULL((SELECT sum(valor) FROM ingreso_variable WHERE id_cuenta=cuenta.id),0) + ingreso ) as suma_ingresos,
        ((IFNULL((SELECT sum(valor) FROM ingreso_variable WHERE id_cuenta=cuenta.id),0) + ingreso ) - (IFNULL((SELECT sum(valor) FROM egreso_variable WHERE id_cuenta=cuenta.id),0))) as resta_egresos
        FROM cuenta
        WHERE id = %s 
        """ , (id_cuenta,))
    data6 = cur.fetchall()
    print(data6)
    cur.close()
    return render_template('ver_cuenta.html', cuentasact = data, cuneta_ingvar = data2, totalesing = data3, cuneta_egvar = data4, totaleseg = data5, totaliza = data6)

'''    
#inicio enrutamiento de la app por medio de funciones que seran modulos tipo menu
#Vistas de los formualrios html front-end
#Ruta y vista para form de crear contacto
@app.route('/crear')
def Crear():
    return render_template('crear.html')
#Ruta y vista para form de editar contacto

@app.route('/edit/<string:id>', methods = ['POST', 'GET'])
def editar_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('editar-contacto.html', contacto = data[0])

@app.route('/update/<string:id>', methods=['POST'])
def update_contacto(id):
    if request.method == 'POST':
        tel = request.form['tel']
        nomape = request.form['nomape'].upper()
        edad = request.form['edad']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contactos
            SET telefono = %s,
                nombre = %s,
                correo = %s,
                edad = %s
            WHERE id = %s
        """, (tel, nomape, email, edad, id))
        flash('El contacto fue editado y guardado con exito en la base de datos')
        mysql.connection.commit()
        return redirect(url_for('Consultar'))

#Ruta y vista para form de consultar contacto
@app.route('/consultar')
def Consultar():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos ORDER BY id DESC')
    data = cur.fetchall()
    cur.close()
    return render_template('consultar.html', contacts = data)

@app.route('/consulta_tel', methods = ['POST', 'GET'])
def Consulta_id():
    tel = request.form['tel']
    cur = mysql.connection.cursor()
    if tel!="":
        cur.execute('SELECT * FROM contactos WHERE telefono = %s ORDER BY id DESC' , (tel,))
    else:
        cur.execute('SELECT * FROM contactos ORDER BY id DESC')
    data = cur.fetchall()
    cur.close()
    #print(data[0])
    return render_template('consultar.html', contacts = data)

#Ruta y vista para form de eliminar contacto desde la vista de consultar
@app.route('/eliminar/<string:id>', methods = ['POST','GET'])
def Eliminar_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Se elimina el contacto con exito!')
    return redirect(url_for('Consultar'))

#Acciones que se realiza desde las vistas front-end para back-end
@app.route('/agregar_contacto', methods=['POST'])
def agregar_contacto():
    tel = request.form['tel']
    nomape = request.form['nomape'].upper()
    edad = request.form['edad']
    email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO contactos (telefono, nombre, correo, edad) VALUES (%s,%s,%s,%s)", (tel, nomape, email, edad))
    mysql.connection.commit()
    flash('El contacto fue guardado con exito en la base de datos')
    return redirect(url_for('Crear'))
'''
#Compruebo archivo inicial sea ppal
if __name__ == '__main__':
    app.run(port=3000, debug=True) 


