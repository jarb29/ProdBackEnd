import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Modelo(db.Model):
    __tablename__ = 'modelo'
    id = db.Column(db.Integer, primary_key = True)
    nombre_programa = db.Column(db.String(100), nullable = False)
    numero_ot = db.Column(db.Integer)
    cantiadUnidadesFabricarEnLaOt = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    nestic_id = db.Column(db.String(100))

    def __repr__(self):
        return f"modelo('{self.nombre_programa}', '{self.numero_ot}', '{self.date_created}', '{self.cantiadUnidadesFabricarEnLaOt}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre_programa": self.nombre_programa,
            "numero_ot": self.numero_ot,
            "date_created": self.date_created,
            "cantiadUnidadesFabricarEnLaOt": self.cantiadUnidadesFabricarEnLaOt
        }  



class Nestic(db.Model):
    __tablename__ = 'nestic'
    id = db.Column(db.Integer, primary_key = True)
    programa_nestic = db.Column(db.String(100), nullable = False)
    numero_piezas_criticas = db.Column(db.Integer)
    tiempo_corte = db.Column(db.Integer)
    espesor = db.Column(db.Integer)
    longitud_nestic = db.Column(db.Integer)
    modelo_elegido = db.Column(db.String(100))
    pieza_id = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"nestic('{self.programa_nestic }', '{self.numero_piezas_criticas}', '{self.tiempo_corte }', '{self.espesor}', '{self.longitud_nestic}', '{self.modelo_elegido}', '{self.date_created}')"

    def serialize(self):
        return {
            "id":self.id,
            "programa_nestic": self.programa_nestic,
            "numero_piezas_criticas": self.numero_piezas_criticas,
            "tiempo_corte": self.tiempo_corte ,
            "espesor": self.espesor,
            "longitud_nestic":self.longitud_nestic,
            "modelo_elegido":self.modelo_elegido,
            "date_created":self.date_created,
        }  

class Piezas(db.Model):
    __tablename__ = 'piezas'
    id = db.Column(db.Integer, primary_key = True)
    nombre_pieza = db.Column(db.String(100), nullable = False)
    cantidadPiezasPorPlancha = db.Column(db.Integer)
    crearLongitudCortePieza = db.Column(db.Integer)
    nesticElegido = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"piezas('{self.nombre_pieza}', '{self.cantidadPiezasPorPlancha}', '{self.crearLongitudCortePieza}', '{self.nesticElegido}', '{self.date_created}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre_pieza": self.nombre_pieza ,
            "cantidadPiezasPorPlancha": self.cantidadPiezasPorPlancha,
            "crearLongitudCortePieza": self.crearLongitudCortePieza,
            "nesticElegido":self.nesticElegido,
            "date_created":self.date_created,
        }  

class ModeloProduccion(db.Model):
    __tablename__ = 'modeloProduccion'
    id = db.Column(db.Integer, primary_key = True)
    modelo_produccion = db.Column(db.String(100), nullable = False)
    ot_produccion = db.Column(db.Integer)
    cantidad_producir = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"modeloProduccion('{self.modelo_produccion}', '{self.ot_produccion}', '{self.cantidad_producir}', '{self.date_created}')"

    def serialize(self):
        return {
            "id":self.id,
            "modelo_produccion": self.modelo_produccion,
            "ot_produccion": self.ot_produccion,
            "cantidad_producir": self.cantidad_producir,
            "date_created": self.date_created
        }

class NesticProduccion(db.Model):
    __tablename__ = 'nesticProduccion'
    id = db.Column(db.Integer, primary_key = True)
    planchas_cortadas = db.Column(db.Integer)
    ot_cortada = db.Column(db.Integer)
    operador = db.Column(db.String(100), nullable = False)
    nestic_cortado = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"nesticProduccion('{self.planchas_cortadas }', '{self.ot_cortada}', '{self.operador}', '{self.nestic_cortado}', '{self.date_created}')"

    def serialize(self):
        return {
            "id":self.id,
            "planchas_cortadas": self.planchas_cortadas,
            "ot_cortada": self.ot_cortada,
            "operador": self.operador,
            "nestic_cortado":self.nestic_cortado,
            "date_created": self.date_created
        } 



class Plegado(db.Model):
    __tablename__ = 'plegado'
    id = db.Column(db.Integer, primary_key = True)
    plegado_ot_seleccionado = db.Column(db.Integer)
    plegadoPiezaSeleccionada = db.Column(db.String(100), nullable = False)
    plegadoMaquinaSeleccionada = db.Column(db.String(100), nullable = False)
    plegadoOperadorSeleccionado = db.Column(db.String(100), nullable = False)
    plegadoCantidadPiezas = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"plegado('{self.plegado_ot_seleccionado}', '{self.plegadoPiezaSeleccionada}', '{self.plegadoMaquinaSeleccionada}', '{self.plegadoOperadorSeleccionado}', '{self.plegadoCantidadPiezas}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre_pieza": self.plegado_ot_seleccionado,
            "plegadoPiezaSeleccionada": self.plegadoPiezaSeleccionada,
            "plegadoMaquinaSeleccionada": self.plegadoMaquinaSeleccionada,
            "plegadoOperadorSeleccionado":self.plegadoOperadorSeleccionado,
            "date_created":self.plegadoCantidadPiezas,
        }  


class Pintura(db.Model):
    __tablename__ = 'pintura'
    id = db.Column(db.Integer, primary_key = True)
    pintura_ot_seleccionado = db.Column(db.Integer)
    pinturaPiezaSeleccionada = db.Column(db.String(100), nullable = False)
    pinturaCantidadPiezas = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"pintura('{self.pintura_ot_seleccionado}', '{self.pinturaPiezaSeleccionada}', '{self.pinturaCantidadPiezas}', '{self.date_created }')"

    def serialize(self):
        return {
            "id":self.id,
            "pintura_ot_seleccionado": self.pintura_ot_seleccionado,
            "pinturaPiezaSeleccionada": self.pinturaPiezaSeleccionada,
            "pinturaCantidadPiezas": self.pinturaCantidadPiezas,
            "date_created":self.date_created
        }  
    
class SubProducto(db.Model):
    __tablename__ = 'subproducto'
    id = db.Column(db.Integer, primary_key = True)
    Linea1NombreSubproducto = db.Column(db.String(100), nullable = False)
    subProducto_ot_seleccionado  = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"subproducto('{self.Linea1NombreSubproducto}', '{self.subProducto_ot_seleccionado}', '{self.date_created }')"

    def serialize(self):
        return {
            "id":self.id,
            "Linea1NombreSubproducto": self.Linea1NombreSubproducto,
            "subProducto_ot_seleccionado": self.subProducto_ot_seleccionado,
            "date_created":self.date_created
        }  

class PiezasIntegranSubProducto(db.Model):
    __tablename__ = 'piezasIntegranSubProducto'
    id = db.Column(db.Integer, primary_key = True)
    subProductoSeleccionado = db.Column(db.String(100), nullable = False)
    piezaSeleccionaIntegraSubproducto = db.Column(db.String(100), nullable = False)
    subProducto_ot_seleccionado = db.Column(db.Integer)
    cantidad_utilizada_por_subproducto = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"subproducto('{self.subProductoSeleccionado}', '{self.piezaSeleccionaIntegraSubproducto}', '{self.cantidad_utilizada_por_subproducto}', '{self.subProducto_ot_seleccionado}', '{self.date_created }')"

    def serialize(self):
        return {
            "id":self.id,
            "subProductoSeleccionado": self.subProductoSeleccionado,
            "piezaSeleccionaIntegraSubproducto": self.piezaSeleccionaIntegraSubproducto,
            "subProducto_ot_seleccionado": self.subProducto_ot_seleccionado,
            "cantidad_utilizada_por_subproducto": self.cantidad_utilizada_por_subproducto,
            "date_created":self.date_created
        }  

class Produccion(db.Model):
    __tablename__ = 'produccion'
    id = db.Column(db.Integer, primary_key = True)
    ot_seleccionada = db.Column(db.Integer)
    sub_producto_seleccionado = db.Column(db.String(100), nullable = False)
    produccion_Cantidad_fabricada = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"subproducto('{self.ot_seleccionada}', '{self.sub_producto_seleccionado}', '{self.produccion_Cantidad_fabricada}', '{self.date_created }')"

    def serialize(self):
        return {
            "id":self.id,
            "ot_seleccionada": self.ot_seleccionada,
            "sub_producto_seleccionado": self.sub_producto_seleccionado,
            "produccion_Cantidad_fabricada": self.produccion_Cantidad_fabricada,
            "date_created":self.date_created
        }  


class PiezasIntegranProductoTerminado(db.Model):
    __tablename__ = 'piezasIntegranProductoTerminado'
    id = db.Column(db.Integer, primary_key = True)
    ot_seleccionada = db.Column(db.Integer)
    sub_producto_seleccionado = db.Column(db.String(100), nullable = False)
    producto_terminado_utilizado_estufa = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"subproductoterminado('{self.ot_seleccionada}', '{self.sub_producto_seleccionado}', '{self.producto_terminado_utilizado_estufa}', '{self.date_created }')"

    def serialize(self):
        return {
            "id":self.id,
            "ot_seleccionada": self.ot_seleccionada,
            "sub_producto_seleccionado": self.sub_producto_seleccionado,
            "producto_terminado_utilizado_estufa": self.producto_terminado_utilizado_estufa,
            "date_created":self.date_created
        }  

    
class ProduccionProductoTerminado(db.Model):
    __tablename__ = 'produccionProductoTerminado'
    id = db.Column(db.Integer, primary_key = True)
    ot_seleccionada = db.Column(db.Integer)
    sub_producto_seleccionado = db.Column(db.String(100), nullable = False)
    producto_terminado_utilizado_estufa = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"subproductoterminado('{self.ot_seleccionada}', '{self.sub_producto_seleccionado}', '{self.producto_terminado_utilizado_estufa}', '{self.date_created }')"

    def serialize(self):
        return {
            "id":self.id,
            "ot_seleccionada": self.ot_seleccionada,
            "sub_producto_seleccionado": self.sub_producto_seleccionado,
            "producto_terminado_utilizado_estufa": self.producto_terminado_utilizado_estufa,
            "date_created":self.date_created
        }  


class PlanProduccionMensual(db.Model):
    __tablename__ = 'planProduccionMensual'
    id = db.Column(db.Integer, primary_key = True)
    ot_en_produccion = db.Column(db.Integer)
    estufas_plan_producc = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"planProduccionMensual('{self.estufas_plan_producc}', '{self.ot_en_produccion}', '{self.date_created}')"

    def serialize(self):
        return {
            "id":self.id,
            "modelo_produccion": self.estufas_plan_producc,
            "ot_produccion": self.ot_en_produccion,
            "date_created": self.date_created
        }

class User(db.Model):
    _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    clave = db.Column(db.String(100), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"usuarios('{self.nombre }', '{self.email}', '{self.clave}', '{self.date_created}')"

    def serialize(self):
        return {
            "id":self.id,
            "nombre": self.nombre,
            "email": self.email,
            "date_created": self.date_created
        }