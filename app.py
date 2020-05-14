import os
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Modelo, Nestic, Piezas, ModeloProduccion, NesticProduccion
from flask_mail import Mail, Message
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static')
ALLOWED_EXTENSIONS_IMG = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'jarb29@gmail.com'
app.config['MAIL_PASSWORD'] = 'Amesti2020'


JWTManager(app)
CORS(app)
bcrypt = Bcrypt(app)
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
mail = Mail(app)
manager.add_command("db", MigrateCommand)



@app.route('/')
def root():
    return render_template('index.html')


@app.route("/api/cargarprograma", methods=['POST'])
def crearProgramas():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':

        numero_ot = request.json.get('numero_ot', None)
        nombre_programa = request.json.get('nombre_programa', None)
        cantiadUnidadesFabricarEnLaOt = request.json.get('cantiadUnidadesFabricarEnLaOt', None)
        if not numero_ot:
            return jsonify({"msg": "Falta introducir el numero OT"}), 400
        if not nombre_programa:
            return jsonify({"msg": "Falta introducir el nombre del programa"}), 400
        if not cantiadUnidadesFabricarEnLaOt:
            return jsonify({"msg": "Falta introducir la cantidad"}), 400
        
        usua = Modelo()
        usua.numero_ot = numero_ot
        usua.nombre_programa = nombre_programa
        usua.cantiadUnidadesFabricarEnLaOt = cantiadUnidadesFabricarEnLaOt
        db.session.add(usua)
        db.session.commit()

    data = {
        "Modelo": usua.serialize() 
    }
    return jsonify({'msg': 'Modelo agregado exitosamente'}),  200



@app.route('/api/modelodisponibles', methods=['GET'])
def modelosDisponibles():
    listaModelos = Modelo.query.all()
    listaModelos = list(map(lambda listaModelos: listaModelos.serialize(), listaModelos))
    return jsonify(listaModelos), 200


@app.route("/api/crearnesctic", methods=['POST'])
def crearNestic():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        modelo_elegido = request.json.get('modelo_elegido', None)
        programa_nestic = request.json.get('programa_nestic', None)
        numero_piezas_criticas = request.json.get('numero_piezas_criticas', None)
        tiempo_corte = request.json.get('tiempo_corte', None)
        espesor = request.json.get('espesor', None)
        longitud_nestic = request.json.get('longitud_nestic', None)
        
        if not modelo_elegido:
            return jsonify({"msg": "Falta introducir el modelo_elegido"}), 400
        if not programa_nestic:
            return jsonify({"msg": "Falta introducir el nombre del programa_nestic"}), 400
        if not numero_piezas_criticas:
            return jsonify({"msg": "Falta introducir el numero_piezas_criticas"}), 400
        if not tiempo_corte:
            return jsonify({"msg": "Falta introducir el tiempo_corte"}), 400
        if not espesor:
            return jsonify({"msg": "Falta introducir el espesor"}), 400
        if not longitud_nestic:
            return jsonify({"msg": "Falta introducir la longitud_nestic"}), 400
        
        usua = Nestic()
        usua.modelo_elegido = modelo_elegido
        usua.programa_nestic = programa_nestic
        usua.numero_piezas_criticas = numero_piezas_criticas
        usua.tiempo_corte = tiempo_corte
        usua.espesor = espesor
        usua.longitud_nestic = longitud_nestic
        db.session.add(usua)
        db.session.commit()

    data = {
        "Nestic": usua.serialize() 
    }
    return jsonify({'msg': 'Modelo agregado exitosamente'}),  200





@app.route("/api/crearpieza", methods=['POST'])
def crearPiezas():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        nombre_pieza = request.json.get('nombre_pieza', None)
        cantidadPiezasPorPlancha = request.json.get('cantidadPiezasPorPlancha', None)
        crearLongitudCortePieza = request.json.get('crearLongitudCortePieza', None)
        nesticElegido = request.json.get('nesticElegido', None)

        
        if not nombre_pieza:
            return jsonify({"msg": "Falta introducir el nombre de la pieza "}), 400
        if not cantidadPiezasPorPlancha:
            return jsonify({"msg": "Falta introducir el nombre la cantidad"}), 400
        if not crearLongitudCortePieza:
            return jsonify({"msg": "Falta introducirla longitud"}), 400
        if not nesticElegido:
            return jsonify({"msg": "Falta seleccionar el programa nestic"}), 400

        
        usua = Piezas()
        usua.nombre_pieza = nombre_pieza
        usua.cantidadPiezasPorPlancha = cantidadPiezasPorPlancha
        usua.crearLongitudCortePieza = crearLongitudCortePieza
        usua.nesticElegido = nesticElegido
        db.session.add(usua)
        db.session.commit()

    data = {
        "Piezas": usua.serialize() 
    }
    return jsonify({'msg': 'Pieza agregada exitosamente'}),  200


@app.route("/api/modelosproduccion", methods=['POST'])
def crearModeloProducion():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        modelo_produccion = request.json.get('modelo_produccion', None)
        ot_produccion = request.json.get('ot_produccion', None)
        cantidad_producir = request.json.get('cantidad_producir', None)
        nesticElegido = request.json.get('nesticElegido', None)

        
        if not modelo_produccion:
            return jsonify({"msg": "Falta introducir el modelo "}), 400
        if not ot_produccion:
            return jsonify({"msg": "Falta introducir OT"}), 400
        if not cantidad_producir:
            return jsonify({"msg": "Falta introducirla longitud"}), 400
        
        usua = ModeloProduccion.query.filter_by(ot_produccion=ot_produccion).first()
        if usua:
            return jsonify({"msg": "EL producto ya existe"}), 400

        
        usua = ModeloProduccion()
        usua.modelo_produccion = modelo_produccion
        usua.ot_produccion = ot_produccion
        usua.cantidad_producir = cantidad_producir
        db.session.add(usua)
        db.session.commit()

    data = {
        "Piezas": usua.serialize() 
    }
    return jsonify({'msg': 'Modelo a produccion agregada exitosamente'}),  200



@app.route('/api/Nesticsdisponibles', methods=['GET'])
def nesticsDisponibles():
    if request.method == 'GET':
        listaNestics = Nestic.query.all()
        listaNestics = list(map(lambda listaNestics: listaNestics.serialize(), listaNestics))
        return jsonify(listaNestics), 200


@app.route('/api/nesticsmodelar/<name>', methods=['GET'])
def nesticsModelar(name):
    if request.method == 'GET':
        listaNesticsModelar = Nestic.query.filter_by(modelo_elegido=name).all()
        listaNesticsModelar = list(map(lambda listaNesticsModelar: listaNesticsModelar.serialize(), listaNesticsModelar))
        return jsonify(listaNesticsModelar), 200

@app.route('/api/otProduccion', methods=['GET'])
def otProduccion():
    listaOt = ModeloProduccion.query.all()
    listaOt = list(map(lambda listaOt: listaOt.serialize(), listaOt))
    return jsonify(listaOt), 200


@app.route('/api/nesticProduccion/<int:id>', methods=['GET'])
def nesticProduccion(id):
    
    modelo_ot = Modelo.query.filter_by(numero_ot=id).first()
    modelo_ot = modelo_ot.nombre_programa
    nesti_ot = Nestic.query.filter_by(modelo_elegido=modelo_ot).all()
    nesti_ot = list(map(lambda nesti_ot: nesti_ot.serialize(), nesti_ot))
    return jsonify(nesti_ot), 200


@app.route("/api/plachascortadas", methods=['POST'])
def planchasCortadas():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        planchas_cortadas = request.json.get('planchas_cortadas', None)
        ot_cortada = request.json.get('ot_cortada', None)
        operador = request.json.get('operador', None)
        nestic_cortado = request.json.get('nestic_cortado', None)
        
        if not planchas_cortadas:
            return jsonify({"msg": "Falta introducir las planchas cortadas"}), 400
        if not ot_cortada:
            return jsonify({"msg": "Falta introducir la ot cortada"}), 400
        if not operador:
            return jsonify({"msg": "Falta introducir el operador"}), 400
        if not nestic_cortado:
            return jsonify({"msg": "Falta introducir programa cortado"}), 400
        
        usua = NesticProduccion.query.filter_by(planchas_cortadas=planchas_cortadas, ot_cortada=ot_cortada, operador=operador, nestic_cortado=nestic_cortado).first()
        if usua:
            return jsonify({"msg": "Corte ya fue cargado"}), 400

        
        usua = NesticProduccion()
        usua.planchas_cortadas = planchas_cortadas
        usua.ot_cortada = ot_cortada
        usua.operador= operador
        usua.nestic_cortado= nestic_cortado
        db.session.add(usua)
        db.session.commit()

    data = {
        "Nestic": usua.serialize() 
    }
    return jsonify({'msg': 'Planchas cortadas agregadas exitosamente'}),  200



@app.route('/api/modelarEstufas/<int:id>/<int:estufas>', methods=['GET'])
def modeloaEtufas(id, estufas):
    modelo_ot = Modelo.query.filter_by(numero_ot=id).first()
    modelo_ot = modelo_ot.nombre_programa
    nesti_ot = Nestic.query.filter_by(modelo_elegido=modelo_ot).all()
    planchasModelar = []
    tiempo_por_nestic = []
    for nest in nesti_ot:
        planchas = round(estufas / nest.numero_piezas_criticas, 0)
        tiempo_por_corte = planchas*(nest.tiempo_corte + 0.4)
        data = {
            "nestic": nest.programa_nestic,
            "plancha": planchas,
            "tiempo_para_esas_planchas": tiempo_por_corte
        }
        planchasModelar.append(data)
        
   
    return jsonify(planchasModelar), 200


@app.route('/api/tablaestufasProduccion/', methods=['GET'])
def estufasProduccion():
    modelosEnProduccion = ModeloProduccion.query.all()
    
    piezas_modelo = {}
    for modelo in modelosEnProduccion:
        piezas = Piezas.query.all()
        piezas_cortadas = {}
        
        for pieza in piezas:
            pieza_nestic = []
            total_pieza_suma = 0 
            nestis = NesticProduccion.query.filter_by(ot_cortada = modelo.ot_produccion, nestic_cortado=pieza.nesticElegido).all()
            i = 1
            for nesti in nestis:
                total_pieza = pieza.cantidadPiezasPorPlancha*nesti.planchas_cortadas
                if total_pieza <= modelo.cantidad_producir:
                    
                    total_pieza_suma += total_pieza
                    data = {
                        "operador":nesti.operador,
                        "ot_produccion": modelo.ot_produccion,
                        "nestic_produccion": nesti.nestic_cortado,
                        "nombre_pieza": pieza.nombre_pieza,
                        "cantidad_fabricada_por_corte": total_pieza,
                        "total pieza": total_pieza_suma,
                         "fecha": nesti.date_created
                        }
                    pieza_nestic.append(data)
                total ={
                    "total_pieza": total_pieza_suma,
                     "fecha": nesti.date_created
                    } 
                if (i == len(nestis)):
                    pieza_nestic.append(total)
                i +=1
                piezas_cortadas[pieza.nombre_pieza] = pieza_nestic
        piezas_modelo[modelo.modelo_produccion] = piezas_cortadas
    return jsonify(piezas_modelo), 200


@app.route('/api/tablaestufasProduccionnn/', methods=['GET'])
def estufasProduccionnn():
    totales_por_modelo = []
    piezas_por_modelo =[]
    
    modelosEnProduccion = ModeloProduccion.query.all()
    for modelo in modelosEnProduccion:
        piezas = Piezas.query.all()
        piezas_en_un_modelo = []
        piezas_cortadas = []
        for pieza in piezas:
            i = 1
            total_pieza_suma = 0
            nestis = NesticProduccion.query.filter_by(ot_cortada = modelo.ot_produccion, nestic_cortado=pieza.nesticElegido).all()
            pieza_nestic = {}
            for nesti in nestis:
                total_pieza = pieza.cantidadPiezasPorPlancha*nesti.planchas_cortadas
                total_pieza_suma += total_pieza
                data = {
                        "operador":nesti.operador,
                        "ot_produccion": modelo.ot_produccion,
                        "nestic_produccion": nesti.nestic_cortado,
                        "nombre_pieza": pieza.nombre_pieza,
                        "cantidad_fabricada_por_corte": total_pieza,
                        "total pieza": total_pieza_suma,
                        "fecha": nesti.date_created
                    }
                pieza_nestic.update(data)
                if i == len(nestis):
                    total ={
                        "total_pieza": total_pieza_suma,
                        "nombre_pieza": pieza.nombre_pieza,
                        "programa": modelo.modelo_produccion,
                        "fecha": nesti.date_created
                    }
                    piezas_en_un_modelo.append(total)
                i +=1
                piezas_cortadas.append(pieza_nestic)
        totales_por_modelo.append(piezas_en_un_modelo)
        piezas_por_modelo.append(piezas_cortadas)
        

    return jsonify(totales_por_modelo, piezas_por_modelo), 200









if __name__ == '__main__':
    manager.run()

