import os
from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db, Modelo, Nestic, Piezas, ModeloProduccion, NesticProduccion, Plegado, Pintura, SubProducto, PiezasIntegranSubProducto, Produccion
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
        tiempo_por_corte = round(planchas*(nest.tiempo_corte + 0.4))
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
                total_pieza_suma += total_pieza
                if total_pieza_suma <= modelo.cantidad_producir:
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


# desde aca en adelante datos para plegado
# 1 obtener las piezas disponibles por modelo

@app.route('/api/plegadopiezas/<int:id>', methods=['GET'])
def plegadopiezasDisponible(id):
    piezas_por_modelo = []
    modelo_ot = Modelo.query.filter_by(numero_ot=id).first()
    modelo_ot = modelo_ot.nombre_programa
    nesti_ot = Nestic.query.filter_by(modelo_elegido=modelo_ot).all()
    for nest in nesti_ot:
        nombre = nest.programa_nestic
        piezas = Piezas.query.filter_by(nesticElegido = nombre).all()
        for pieza in piezas:
            data = {
                "nombre_pieza": pieza.nombre_pieza,
                "nestic": pieza.nesticElegido,
                "piezas_por_plancha": pieza.cantidadPiezasPorPlancha
            }
            piezas_por_modelo.append(data)
    
    return jsonify(piezas_por_modelo), 200


# Logica para crear la tabla de piezas de plegado
@app.route("/api/piezasplegado", methods=['POST'])
def crearPiezasPlegado():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        plegado_ot_seleccionado = request.json.get('plegado_ot_seleccionado', None)
        plegadoPiezaSeleccionada = request.json.get('plegadoPiezaSeleccionada', None)
        plegadoMaquinaSeleccionada = request.json.get('plegadoMaquinaSeleccionada', None)
        plegadoOperadorSeleccionado = request.json.get('plegadoOperadorSeleccionado', None)
        plegadoCantidadPiezas = request.json.get('plegadoCantidadPiezas', None)

        
        if not plegado_ot_seleccionado:
            return jsonify({"msg": "Falta introducir Ot"}), 400
        if not plegadoPiezaSeleccionada:
            return jsonify({"msg": "Falta introducir las piezas"}), 400
        if not plegadoMaquinaSeleccionada:
            return jsonify({"msg": "Falta plegadora"}), 400
        if not plegadoOperadorSeleccionado:
            return jsonify({"msg": "Falta operador"}), 400
        if not plegadoCantidadPiezas:
            return jsonify({"msg": "Falta cantidad de piezas"}), 400
        
        usua = Plegado()
        usua.plegado_ot_seleccionado = plegado_ot_seleccionado
        usua.plegadoPiezaSeleccionada = plegadoPiezaSeleccionada
        usua.plegadoMaquinaSeleccionada  = plegadoMaquinaSeleccionada 
        usua.plegadoOperadorSeleccionado  = plegadoOperadorSeleccionado
        usua.plegadoCantidadPiezas  = plegadoCantidadPiezas
        db.session.add(usua)
        db.session.commit()

    data = {
        "Piezas_plegado": usua.serialize() 
    }
    return jsonify({'msg': 'Modelo a produccion agregada exitosamente'}, data),  200


# logica para las piezas fabricadas en plegado
@app.route('/api/piezasPlegadas', methods=['GET'])
def piezasPlegadas():
    modelosEnProduccion = ModeloProduccion.query.all()
    piezas_modelo = {}
    for modelo in modelosEnProduccion:
        piezas = Piezas.query.all()
        piezas_plegadas = {}
        for pieza in piezas:
            pieza_plegado = []
            total_pieza_suma = 0 
            piezas_en_plegado = Plegado.query.filter_by(plegado_ot_seleccionado = modelo.ot_produccion, plegadoPiezaSeleccionada=pieza.nombre_pieza).all()
            i = 1
            for pieza_en_plegado in piezas_en_plegado:
                total_pieza = pieza_en_plegado.plegadoCantidadPiezas
                total_pieza_suma += total_pieza
                if total_pieza_suma <= modelo.cantidad_producir: 

                    data = {
                        "operador": pieza_en_plegado.plegadoOperadorSeleccionado,
                        "ot_produccion": pieza_en_plegado.	plegado_ot_seleccionado,
                        "nombre_pieza": pieza_en_plegado.plegadoPiezaSeleccionada,
                        "cantidad_fabricada_por_dia": pieza_en_plegado.plegadoCantidadPiezas,
                        "total pieza": total_pieza_suma,
                         "fecha": pieza_en_plegado.date_created
                        }
                    pieza_plegado.append(data)
                total ={
                    "total_pieza": total_pieza_suma,
                     "fecha": pieza_en_plegado.date_created
                    } 
                if (i == len(piezas_en_plegado)):
                    pieza_plegado.append(total)
                i +=1
                piezas_plegadas[pieza.nombre_pieza] = pieza_plegado 
        piezas_modelo[modelo.modelo_produccion] = piezas_plegadas

# Logica para obtener la cantidad de peizas disponibles (Plegado - usado) primera parte (usado)


    piezas_modelo_plegado = {}
    for modelo in modelosEnProduccion:
        piezas = Piezas.query.all()
        piezas_plegadas = {}
        for pieza in piezas:
            pieza_plegado = []
            total_pieza_suma = 0 
            piezas_en_plegado = Plegado.query.filter_by(plegado_ot_seleccionado = modelo.ot_produccion, plegadoPiezaSeleccionada=pieza.nombre_pieza).all()
            i = 1
            for pieza_en_plegado in piezas_en_plegado:
                total_pieza = pieza_en_plegado.plegadoCantidadPiezas
                total_pieza_suma += total_pieza
                total ={
                    "ot_produccion": modelo.ot_produccion,
                    "total_por_pieza": total_pieza_suma,
                    "fecha": pieza_en_plegado.date_created
                    } 
                if (i == len(piezas_en_plegado)):
                    pieza_plegado.append(total)
                i +=1
                piezas_plegadas[pieza.nombre_pieza] = total
        piezas_modelo_plegado[modelo.modelo_produccion] = piezas_plegadas

    # Logica para obtener la cantidad de peizas disponibles (Plegado - usado) primera parte (usado)

    piezas_modelo_produccion = {}
    for modelo in modelosEnProduccion:
        sub_productos = SubProducto.query.filter_by(subProducto_ot_seleccionado = modelo.ot_produccion).all()
      
        sub_producto_total = {}
        for sub_producto in sub_productos:
            sub_producto_por_dia = []
            total_pieza_suma = 0 
            sub_productos_produccion = Produccion.query.filter_by(ot_seleccionada = modelo.ot_produccion, sub_producto_seleccionado=sub_producto.Linea1NombreSubproducto).all()
            i = 1
      

            for sub_producto_produccion in sub_productos_produccion:
                total_pieza = sub_producto_produccion.produccion_Cantidad_fabricada
                total_pieza_suma += total_pieza
                if (i == len(sub_productos_produccion)):
                  
                    piezas_por_produccion = PiezasIntegranSubProducto.query.filter_by(subProducto_ot_seleccionado = modelo.ot_produccion, subProductoSeleccionado=sub_producto_produccion.sub_producto_seleccionado).all()
         
                    for pieza in piezas_por_produccion:
                        numero_de_pieza_por_subpro = pieza.cantidad_utilizada_por_subproducto * total_pieza_suma
                   
                        data_total_pieza ={
                            "ot_produccion": sub_producto_produccion.ot_seleccionada,
                            "total_por_pieza": numero_de_pieza_por_subpro,
                            "fecha": sub_producto_produccion.date_created
                            }
                        #sub_producto_por_dia.append(data_total_pieza)
                        sub_producto_total[pieza.piezaSeleccionaIntegraSubproducto] = data_total_pieza
                i +=1            
        piezas_modelo_produccion[modelo.modelo_produccion] = sub_producto_total

 #Logica para obtener la cantidad de peizas disponibles (plegado - usado) segunda parte (plegado)
    modelos_tot = {}
    
    for keys_corte in piezas_modelo_plegado:
        #print(piezas_modelo_produccion)
        for keys_prod in piezas_modelo_produccion:
            if keys_corte == keys_prod:
               
                cantidad_dispoble={}
                for key_despues_corte in piezas_modelo_plegado[keys_corte]:
                    for key_despues_prod in piezas_modelo_produccion[keys_corte]:
                        if key_despues_corte == key_despues_prod:
                            
                            pieza = []
                            for keys_final_produc in piezas_modelo_produccion[keys_prod][key_despues_prod]:
                                for keys_final_corte in piezas_modelo_plegado[keys_prod][key_despues_prod]:
                                    #pprint(keys_final_produc, "lo que llega de modelo")
                                    #pprint(keys_final_corte)
                                    if keys_final_produc  == keys_final_corte:
                                        
                                        total_disponible = piezas_modelo_plegado[keys_prod][key_despues_prod]["total_por_pieza"]-piezas_modelo_produccion[keys_prod][key_despues_prod]["total_por_pieza"]
                                        
                                        #print(keys_final_corte["total_por_pieza"], "lo que llega de usado")
                                        #print(piezas_modelo_produccion[keys_prod][key_despues_prod]["total_por_pieza"], "lo que se corte")
                                        #pprint(total_disponible)
                                        total = {
                                            "total_disponlie": total_disponible,
                                            "fecha": piezas_modelo_produccion[keys_prod][key_despues_prod]["fecha"],
                                            "OT": piezas_modelo_produccion[keys_prod][key_despues_prod]['ot_produccion']
                                        }
                                        

                            pieza.append(total)
                            cantidad_dispoble[key_despues_corte] =  pieza            
                            modelos_tot[keys_corte] = cantidad_dispoble
 


    











    return jsonify(piezas_modelo, modelos_tot), 200


# Logica para crear la tabla de piezas de pintura
@app.route("/api/piezaspintura", methods=['POST'])
def crearPiezasPintura():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        pintura_ot_seleccionado = request.json.get('pintura_ot_seleccionado', None)
        pinturaPiezaSeleccionada = request.json.get('pinturaPiezaSeleccionada', None)
        pinturaCantidadPiezas = request.json.get('pinturaCantidadPiezas', None)

        
        if not pintura_ot_seleccionado:
            return jsonify({"msg": "Falta introducir Ot"}), 400
        if not pinturaPiezaSeleccionada:
            return jsonify({"msg": "Falta introducir la pieza"}), 400
        if not pinturaCantidadPiezas:
            return jsonify({"msg": "Falta introducir cantidad"}), 400

        
        usua = Pintura()
        usua.pintura_ot_seleccionado = pintura_ot_seleccionado
        usua.pinturaPiezaSeleccionada = pinturaPiezaSeleccionada
        usua.pinturaCantidadPiezas  = pinturaCantidadPiezas
        db.session.add(usua)
        db.session.commit()

    data = {
        "Piezas_pintadas": usua.serialize() 
    }
    return jsonify({'msg': 'Modelo a produccion agregada exitosamente'}, data),  200

# Logica para obter la tabla de piezas de pintura
@app.route('/api/piezasPintadas', methods=['GET'])
def piezasPintadas():
    modelosEnProduccion = ModeloProduccion.query.all()
    piezas_modelo = {}
    for modelo in modelosEnProduccion:
        piezas = Piezas.query.all()
        piezas_pintadas = {}
        for pieza in piezas:
            pieza_pintura = []
            total_pieza_suma = 0 
            piezas_en_pintura = Pintura.query.filter_by(pintura_ot_seleccionado = modelo.ot_produccion, pinturaPiezaSeleccionada=pieza.nombre_pieza).all()
            i = 1
            for pieza_en_pintura in piezas_en_pintura:
                total_pieza = pieza_en_pintura.pinturaCantidadPiezas
                total_pieza_suma += total_pieza
                if total_pieza_suma <= modelo.cantidad_producir: 

                    data = {
                        "ot_produccion": pieza_en_pintura.pintura_ot_seleccionado,
                        "nombre_pieza": pieza_en_pintura.pinturaPiezaSeleccionada,
                        "cantidad_fabricada_por_dia": pieza_en_pintura.pinturaCantidadPiezas,
                        "total pieza": total_pieza_suma,
                         "fecha": pieza_en_pintura.date_created
                        }
                    pieza_pintura.append(data)
                total ={
                    "total_pieza": total_pieza_suma,
                     "fecha": pieza_en_pintura.date_created
                    } 
                if (i == len(piezas_en_pintura)):
                    pieza_pintura.append(total)
                i +=1
                piezas_pintadas[pieza.nombre_pieza] = pieza_pintura
        piezas_modelo[modelo.modelo_produccion] = piezas_pintadas
    
    return jsonify(piezas_modelo), 200

# Logica para crear la tabla del subProducto en las lineas
@app.route("/api/creandoSubProductos", methods=['POST'])
def crearSubproductos():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        Linea1NombreSubproducto = request.json.get('Linea1NombreSubproducto', None)
        subProducto_ot_seleccionado = request.json.get('subProducto_ot_seleccionado', None)
        
        verificador = SubProducto.query.filter_by(Linea1NombreSubproducto=Linea1NombreSubproducto, subProducto_ot_seleccionado=subProducto_ot_seleccionado).first()
        if verificador:
            return jsonify({"msg": "Sub-Producto ya fue agregado"}), 400

        if not Linea1NombreSubproducto:
            return jsonify({"msg": "Falta introducir nombre del subproducto"}), 400
        if not subProducto_ot_seleccionado:
            return jsonify({"msg": "Falta introducir la ot del modelo"}), 400


        
        usua = SubProducto()
        usua.Linea1NombreSubproducto  = Linea1NombreSubproducto 
        usua.subProducto_ot_seleccionado= subProducto_ot_seleccionado
        db.session.add(usua)
        db.session.commit()

    data = {
        "Sub_Producto": usua.serialize() 
    }
    return jsonify({'msg': 'Sub-producto agregada exitosamente'}, data),  200


# Logica para Obtener subprodutos de las lineas

@app.route('/api/obtenerSubproducto/<int:id>', methods=['GET'])
def lineaSubProductoDisponible(id):

    sub_Products = SubProducto.query.filter_by(subProducto_ot_seleccionado=id).all()
    sub_Products = list(map(lambda sub_Products: sub_Products.serialize(), sub_Products))

    return jsonify(sub_Products), 200

# Logica para crear los subProductos que integran las lineas
@app.route("/api/creandopiezasIntegranSubProductos", methods=['POST'])
def crearPiezasIntegranSubproductos():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        subProductoSeleccionado = request.json.get('subProductoSeleccionado', None)
        subProducto_ot_seleccionado = request.json.get('subProducto_ot_seleccionado', None)
        piezaSeleccionaIntegraSubproducto = request.json.get('piezaSeleccionaIntegraSubproducto', None)
        cantidad_utilizada_por_subproducto = request.json.get('cantidad_utilizada_por_subproducto', None)

        verificador = PiezasIntegranSubProducto.query.filter_by(piezaSeleccionaIntegraSubproducto=piezaSeleccionaIntegraSubproducto, subProducto_ot_seleccionado=subProducto_ot_seleccionado).first()
        if verificador:
            return jsonify({"msg": "pieza que integra el Sub-Producto ya fue agregado"}), 400
        
        if not subProductoSeleccionado:
            return jsonify({"msg": "Falta introducir nombre del subproducto"}), 400
        if not subProducto_ot_seleccionado:
            return jsonify({"msg": "Falta introducir la ot del modelo"}), 400
        if not piezaSeleccionaIntegraSubproducto:
            return jsonify({"msg": "Falta introducir la pieza que integra el subproducto"}), 400
        if not cantidad_utilizada_por_subproducto:
            return jsonify({"msg": "Falta introducir la cantidad"}), 400


        
        usua = PiezasIntegranSubProducto()
        usua.subProductoSeleccionado  = subProductoSeleccionado
        usua.subProducto_ot_seleccionado= subProducto_ot_seleccionado
        usua.piezaSeleccionaIntegraSubproducto = piezaSeleccionaIntegraSubproducto
        usua.cantidad_utilizada_por_subproducto = cantidad_utilizada_por_subproducto
        db.session.add(usua)
        db.session.commit()

    data = {
        "piezas_Sub_Producto": usua.serialize() 
    }
    return jsonify({'msg': 'piezas que integran Sub-producto agregada exitosamente'}, data),  200

# Agregando la produccion Logica 
@app.route("/api/produccion", methods=['POST'])
def produccion():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    if request.method == 'POST':
        
        ot_seleccionada = request.json.get('ot_seleccionada', None)
        sub_producto_seleccionado = request.json.get('sub_producto_seleccionado', None)
        produccion_Cantidad_fabricada = request.json.get('produccion_Cantidad_fabricada', None)
        
        if not ot_seleccionada:
            return jsonify({"msg": "Falta introducir OT"}), 400
        if not sub_producto_seleccionado:
            return jsonify({"msg": "Falta introducir subproducto"}), 400
        if not produccion_Cantidad_fabricada:
            return jsonify({"msg": "Falta introducir la produccion"}), 400
        
        verificador = PiezasIntegranSubProducto.query.filter_by(subProducto_ot_seleccionado = ot_seleccionada, subProductoSeleccionado = sub_producto_seleccionado).first()
        
        if not verificador:
            return jsonify({"msg": "Tiene que agregar piezas al sub-producto antes de cargar produccion"}), 400


        usua = Produccion()
        usua.ot_seleccionada = ot_seleccionada
        usua.sub_producto_seleccionado = sub_producto_seleccionado
        usua.produccion_Cantidad_fabricada = produccion_Cantidad_fabricada
        db.session.add(usua)
        db.session.commit()

    data = {
        "produccion": usua.serialize() 
    }
    return jsonify({'msg': 'Produccion agregada exitosamente'}, data),  200



# Logica para obter la tabla de produccion disponibles
@app.route('/api/produccionDisponible', methods=['GET'])
def produccionDisponible():
    modelosEnProduccion = ModeloProduccion.query.all()
    piezas_modelo = {}
    for modelo in modelosEnProduccion:
        sub_productos = SubProducto.query.all()
        sub_producto_total = {}
        for sub_producto in sub_productos:
            sub_producto_por_dia = []
            total_pieza_suma = 0 
            sub_productos_produccion = Produccion.query.filter_by(ot_seleccionada = modelo.ot_produccion, sub_producto_seleccionado=sub_producto.Linea1NombreSubproducto).all()
            i = 1
            for sub_producto_produccion in sub_productos_produccion:
                total_pieza = sub_producto_produccion.produccion_Cantidad_fabricada
                total_pieza_suma += total_pieza
                data = {
                        "ot_produccion": sub_producto_produccion.ot_seleccionada,
                        "nombre_subproducto": sub_producto_produccion.sub_producto_seleccionado,
                        "cantidad_fabricada_por_dia": sub_producto_produccion.produccion_Cantidad_fabricada,
                        "total_pieza": total_pieza_suma,
                         "fecha": sub_producto_produccion.date_created
                        }
                sub_producto_por_dia.append(data)
                total ={
                    "total_pieza": total_pieza_suma,
                     "fecha": sub_producto_produccion.date_created
                    } 
                if (i == len(sub_productos_produccion)):
                    sub_producto_por_dia .append(total)
                i +=1
                sub_producto_total[sub_producto_produccion.sub_producto_seleccionado] = sub_producto_por_dia 
        piezas_modelo[modelo.modelo_produccion] = sub_producto_total
    
    return jsonify(piezas_modelo), 200


# Logica para obter la tabla disponnible de piezas de corte
@app.route('/api/producionPorModeloDisponible', methods=['GET'])
def produccionPorModeloDisponible():
    modelosEnProduccion = ModeloProduccion.query.all()
    piezas_cortadas_totales = {}
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
                total_pieza_suma += total_pieza
                total ={
                    "total_por_pieza": total_pieza_suma,
                     "ot_produccion": modelo.ot_produccion,
                     "nesti": nesti.nestic_cortado,
            
                    } 
                if (i == len(nestis)):
                    pieza_nestic.append(total)
                i +=1
                piezas_cortadas[pieza.nombre_pieza] = total
        piezas_cortadas_totales[modelo.modelo_produccion] = piezas_cortadas

    #Logica para obtener la cantidad de peizas disponibles (cortado - usado) primera parte (usado)
    piezas_modelo_produccion = {}
    for modelo in modelosEnProduccion:
        sub_productos = SubProducto.query.filter_by(subProducto_ot_seleccionado = modelo.ot_produccion).all()
      
        sub_producto_total = {}
        for sub_producto in sub_productos:
            sub_producto_por_dia = []
            total_pieza_suma = 0 
            sub_productos_produccion = Produccion.query.filter_by(ot_seleccionada = modelo.ot_produccion, sub_producto_seleccionado=sub_producto.Linea1NombreSubproducto).all()
            i = 1
      

            for sub_producto_produccion in sub_productos_produccion:
                total_pieza = sub_producto_produccion.produccion_Cantidad_fabricada
                total_pieza_suma += total_pieza
                if (i == len(sub_productos_produccion)):
                  
                    piezas_por_produccion = PiezasIntegranSubProducto.query.filter_by(subProducto_ot_seleccionado = modelo.ot_produccion, subProductoSeleccionado=sub_producto_produccion.sub_producto_seleccionado).all()
         
                    for pieza in piezas_por_produccion:
                        numero_de_pieza_por_subpro = pieza.cantidad_utilizada_por_subproducto * total_pieza_suma
                   
                        data_total_pieza ={
                            "ot_produccion": sub_producto_produccion.ot_seleccionada,
                            "total_por_pieza": numero_de_pieza_por_subpro,
                            "fecha": sub_producto_produccion.date_created
                            }
                        #sub_producto_por_dia.append(data_total_pieza)
                        sub_producto_total[pieza.piezaSeleccionaIntegraSubproducto] = data_total_pieza
                i +=1            
        piezas_modelo_produccion[modelo.modelo_produccion] = sub_producto_total
    

   
    #Logica para obtener la cantidad de peizas disponibles (cortado - usado) segunda parte (cortado)
    modelos_tot = {}
    for keys_corte in piezas_cortadas_totales:
      
        for keys_prod in piezas_modelo_produccion:
            if keys_corte == keys_prod:

                cantidad_dispoble={}
                for key_despues_corte in piezas_cortadas_totales[keys_corte]:
                    for key_despues_prod in piezas_modelo_produccion[keys_corte]:
                        if key_despues_corte == key_despues_prod:

                            pieza = []
                            for keys_final_produc in piezas_modelo_produccion[keys_prod][key_despues_prod]:
                                for keys_final_corte in piezas_cortadas_totales[keys_prod][key_despues_prod]:
                                    
                                    if keys_final_produc  == keys_final_corte:

                                        total_disponible = piezas_cortadas_totales[keys_prod][key_despues_prod]["total_por_pieza"]-piezas_modelo_produccion[keys_prod][key_despues_prod]["total_por_pieza"]
                                      
                                        total = {
                                            "total_disponlie": total_disponible,
                                            "fecha": piezas_modelo_produccion[keys_prod][key_despues_prod]["fecha"],
                                            "OT": piezas_modelo_produccion[keys_prod][key_despues_prod]['ot_produccion'],
                                            "nest": piezas_cortadas_totales[keys_prod][key_despues_prod]['nesti']
                                        }

                            pieza.append(total)
                            cantidad_dispoble[key_despues_corte] =  pieza            
                            modelos_tot[keys_corte] = cantidad_dispoble

    
    
    #logica para obtener el valor mas critico
    valores_minimos_por_modelos_corte = []
    for key in modelos_tot:
        piezas_del_modelo = []
        valores_de_piezas = []
        nestic_del_valor = []
        orden_trabajo = []
        for key_in in modelos_tot[key]:
            
        
            piezas_del_modelo.append(key_in)
            for key_sec in modelos_tot[key][key_in]:
                valores_de_piezas.append(key_sec['total_disponlie'])
                nestic_del_valor.append(key_sec['nest'])
                orden_trabajo.append(key_sec['OT'])
                #print(modelos_tot[key][key_in], "buscando la OT")
        a = min(valores_de_piezas)
        #print(a)
        indice = valores_de_piezas.index(a)
        data = {
            "valor_minimo": a,
            "modelo": key,
            "nestic": nestic_del_valor[indice],
            "pieza": piezas_del_modelo[indice],
            "Ot": orden_trabajo[indice]
            }
        valores_minimos_por_modelos_corte.append(data)
    

    
    #Logica para obtener la cantidad de planchas cortadas por nestics
    programa_nest_estufa = {}
    prueba_cortes = []
    for modelo in modelosEnProduccion:
        nestic_disponibles = Nestic.query.filter_by(modelo_elegido = modelo.modelo_produccion).all()
        cortes_totales_nestis =[]
        nestic_cortados = []
        for nestic_disponible in nestic_disponibles:
            nestis_produccion = NesticProduccion.query.filter_by(ot_cortada = modelo.ot_produccion , nestic_cortado = nestic_disponible.programa_nestic).all()
            i = 1
            total_cortado= 0
            
            for nesti in nestis_produccion:
       
                total_cortado_por_nectic = nesti.planchas_cortadas
                total_cortado += total_cortado_por_nectic
                if (i == len(nestis_produccion)):
                    
                    data = {
                        "total_planchas_cortadas": total_cortado,
                        "ot_produccion": modelo.ot_produccion,
                        "nestic_produccion": nesti.nestic_cortado,
                        "total_ot": modelo.cantidad_producir,
                        "modelo": modelo.modelo_produccion
                        }
      
                    nestic_cortados.append(data)
                    
                i +=1
            cortes_totales_nestis.append(nestic_cortados)
        programa_nest_estufa[modelo.modelo_produccion] = nestic_cortados  
        prueba_cortes.append(nestic_cortados)


 #Logica para obtener la cantidad de estufas minimas a fabricar
    disponibilidad_fabricacion = []
    for values  in valores_minimos_por_modelos_corte:

        piezas_cantidad_usada_estufa = PiezasIntegranSubProducto.query.filter_by(subProducto_ot_seleccionado = values["Ot"], piezaSeleccionaIntegraSubproducto = values["pieza"]).first()
        disponibilidad = round(values["valor_minimo"] / piezas_cantidad_usada_estufa.cantidad_utilizada_por_subproducto)

        data = {
            "ot":  piezas_cantidad_usada_estufa.subProducto_ot_seleccionado,
            "pieza": piezas_cantidad_usada_estufa.piezaSeleccionaIntegraSubproducto,
            "valor_minimo":values["valor_minimo"],
            "modelo": values["modelo"],
            "nestic": values["nestic"],
            "cantidad_usada_por_subproducto": piezas_cantidad_usada_estufa.cantidad_utilizada_por_subproducto,
            "sub_producto": piezas_cantidad_usada_estufa.subProductoSeleccionado,
            "disponibilidad_estufas": disponibilidad

        }
        disponibilidad_fabricacion.append(data)
       
                
           

    return jsonify(modelos_tot, valores_minimos_por_modelos_corte, prueba_cortes, disponibilidad_fabricacion), 200

if __name__ == '__main__':
    manager.run()

