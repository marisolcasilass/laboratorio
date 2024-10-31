from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Información de conexión
nombre_servidor = 'KRISTEN\\KRISTEN3' 
nombre_db = 'API'  
driver_odbc = 'ODBC Driver 17 for SQL Server'  

#TODO: Cadena de conexión con autenticación de Windows (trusted_connection=yes)
cadena_conexion = f'mssql+pyodbc://@{nombre_servidor}/{nombre_db}?driver={driver_odbc}&trusted_connection=yes'

#TODO: Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = cadena_conexion
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#TODO: Lista de usuarios
@app.route('/api/usuarios', methods=['GET'])
def usuarios():
    try: 
        nombre_procedure = 'SP_L_Usuarios_01'
        sql_query = text(f'EXEC {nombre_procedure}')
        resultados = db.session.execute(sql_query)
        usuarios_json = [dict(row._asdict()) for row in resultados]
        return jsonify({'usuarios': usuarios_json})
    except Exception as e:
        return jsonify({'Error':str(e)})
    
#TODO: Buscar usuario por Id
@app.route('/api/usuario/<int:id>', methods=['GET'])
def usuario(id):
    try: 
        nombre_procedure = 'SP_L_Usuarios_02'
        sql_query = text(f'EXEC {nombre_procedure} @Id=:id')
        resultados = db.session.execute(sql_query, {'id':id})
        usuarios_json = [dict(row._asdict()) for row in resultados]
        return jsonify({'usuarios': usuarios_json})
    except Exception as e:
        return jsonify({'Error':str(e)})
    
#TODO: Insertar usuario
@app.route('/api/insertar',methods=['POST'])
def insertar ():
    try:    
        datos_json = request.get_json()
        nombre=datos_json['Nombre']
        apellido=datos_json['Apellido']
        telefono=datos_json['Telefono']
        edad=datos_json['Edad']

        nombre_procedure = 'SP_I_Usuarios_01'
        sql_query = text(f'EXEC {nombre_procedure} @Nombre=:Nombre, @Apellido=:Apellido, @Telefono=:Telefono, @Edad=:Edad')
        db.session.execute(sql_query, {'Nombre':nombre,'Apellido':apellido, 'Telefono':telefono, 'Edad':edad })
        db.session.commit()

        return jsonify({'Mensaje': 'Usuario registrado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)})

#TODO: Actualizar usuario    
@app.route('/api/update',methods=['PUT'])
def update():
    try:    
        datos_json = request.get_json()
        id=datos_json['Id']
        nombre=datos_json['Nombre']
        apellido=datos_json['Apellido']
        telefono=datos_json['Telefono']
        edad=datos_json['Edad']

        nombre_procedure = 'SP_U_Usuarios_01'
        sql_query = text(f'EXEC {nombre_procedure} @Id=:Id,@Nombre=:Nombre, @Apellido=:Apellido, @Telefono=:Telefono, @Edad=:Edad')
        db.session.execute(sql_query, {'Id':id,'Nombre':nombre,'Apellido':apellido, 'Telefono':telefono, 'Edad':edad })
        db.session.commit()

        return jsonify({'Mensaje': 'Usuario actualizado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)})

#TODO: Eliminar usuario
@app.route('/api/delete',methods=['DELETE'])
def delete():
    try:    
        datos_json = request.get_json()
        id=datos_json['Id']
        nombre_procedure = 'SP_D_Usuarios_01'
        sql_query = text(f'EXEC {nombre_procedure} @Id=:Id')
        db.session.execute(sql_query, {'Id':id})
        db.session.commit()

        return jsonify({'Mensaje': 'Usuario eliminado correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    #TODO: Configuración para ejecutar la aplicación en modo depuración
    app.run(debug=True)
