from . import db #import db from init
from sqlalchemy.sql import func

import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="book"
)

mycursor = mydb.cursor()

class Book(db.Model):
    id_buku = db.Column(db.Integer, primary_key = True)
    judul = db.Column(db.String(10000))
    author = db.Column(db.String(10000))
    isbn = db.Column(db.String(10000))
    genre= db.Column(db.String(10000))
    img_path = db.Column(db.String(10000))

# # mycursor.execute("SHOW DATABASES")

# # # List All Databases
# # for x in mycursor:
# #   print(x)

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #not capital


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key = True)
#     email = db.Column(db.String(150), unique = True)
#     password = db.Column(db.String(150))
#     firstName = db.Column(db.String(150))
#     notes = db.relationship('Note') #capital

# class Nilai(db.Model):
#     __tablename__="nilai_kab_bangkalan"
#     id_siswa = db.Column(db.Integer)
#     nama = db.Column(db.String(150))
#     nrp = db.Column(db.String(150))
#     id_mapel = db.Column(db.Integer, primary_key = True)
#     score = db.Column(db.Numeric(precision=1, asdecimal=False, decimal_return_scale=None))
#     id_nilai = db.Column(db.Integer, primary_key=True)

def parseCSV(filePath, id_kota):
    # CVS Column Names
    col_names = ['id_siswa','nama','nrp', 'id_mapel', 'score']
    
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath,names=col_names, header=None, skiprows=1)

    # id to string
    print(id_kota)
    tablename = id_to_string(id_kota)

    # Loop through the Rows
    for i,row in csvData.iterrows():
        sql = f"INSERT INTO {tablename} (id_siswa, nama, nrp, id_mapel, score) VALUES (%s, %s, %s, %s, %s)"
        value = (row['id_siswa'],row['nama'],row['nrp'],row['id_mapel'],row['score'])
        mycursor.execute(sql, value)
        mydb.commit()
        print(i,row['id_siswa'],row['nama'],row['nrp'],row['id_mapel'],row['score'])

def id_to_string(argument):
    match argument:
        case "1":
            return "nilai_kab_bangkalan"
        case "2":
            return "nilai_kab_banyuwangi"
        case "3":
            return "nilai_kab_blitar"
        case "4":
            return "nilai_kab_bojonegoro"
        case "5":
            return "nilai_kab_bondowoso"
        case "6":
            return "nilai_kab_gresik"
        case "7":
            return "nilai_kab_jember"
        case "8":
            return "nilai_kab_jombang"
        case "9":
            return "nilai_kab_kediri"
        case "10":
            return "nilai_kab_lamongan"
        case "11":
            return "nilai_kab_lumajang"
        case "12":
            return "nilai_kab_madiun"
        case "13":
            return "nilai_kab_magetan"
        case "14":
            return "nilai_kab_malang"
        case "15":
            return "nilai_kab_mojokerto"
        case "16":
            return "nilai_kab_nganjuk"
        case "17":
            return "nilai_kab_ngawi"
        case "18":
            return "nilai_kab_pacitan"
        case "19":
            return "nilai_kab_pamekasan"
        case "20":
            return "nilai_kab_pasuruan"
        case "21":
            return "nilai_kab_ponorogo"
        case "22":
            return "nilai_kab_probolinggo"
        case "23":
            return "nilai_kab_sampang"
        case "24":
            return "nilai_kab_sidoarjo"
        case "25":
            return "nilai_kab_situbondo"
        case "26":
            return "nilai_kab_sumenep"
        case "27":
            return "nilai_kab_trenggalek"
        case "28":
            return "nilai_kab_tuban"
        case "29":
            return "nilai_kab_tulungagung"
        case "30":
            return "nilai_kota_batu"
        case "31":
            return "nilai_kota_blitar"
        case "32":
            return "nilai_kota_kediri"
        case "33":
            return "nilai_kota_madiun"
        case "34":
            return "nilai_kota_malang"
        case "35":
            return "nilai_kota_mojokerto"
        case "36":
            return "nilai_kota_pasuruan"
        case "37":
            return "nilai_kota_probolinggo"
        case "38":
            return "nilai_kota_surabaya"
    