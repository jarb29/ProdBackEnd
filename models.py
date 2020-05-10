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
    nestic_id = db.relationship('Nestic',  backref= 'Modelo_seleccionado', lazy = True)

    def __repr__(self):
        return f"usuario('{self.nombre_programa}', '{self.numero_ot}', '{self.date_created}', '{self.cantiadUnidadesFabricarEnLaOt}')"

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
    modelo_elegido = db.Column(db.String(100), db.ForeignKey('modelo.id'), nullable=False)
    pieza_id = db.relationship('Piezas',  backref= 'Modelo_seleccionado', lazy = True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"usuario('{self.programa_nestic }', '{self.numero_piezas_criticas}', '{self.tiempo_corte }', '{self.espesor}', '{self.longitud_nestic}', '{self.modelo_elegido}', '{self.date_created}')"

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
    nesticElegido = db.Column(db.Integer, db.ForeignKey('nestic.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"usuario('{self.nombre_pieza}', '{self.cantidadPiezasPorPlancha}', '{self.crearLongitudCortePieza}', '{self.nesticElegido}', '{self.date_created}')"

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
        return f"usuario('{self.modelo_produccion}', '{self.ot_produccion}', '{self.cantidad_producir}', '{self.date_created}')"

    def serialize(self):
        return {
            "id":self.id,
            "modelo_produccion": self.modelo_produccion,
            "ot_produccion": self.ot_produccion,
            "cantidad_producir": self.cantidad_producir,
            "date_created": self.date_created
        }  




