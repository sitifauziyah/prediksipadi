import joblib
from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import mysql.connector
import mysql
import pickle
import numpy as np

app = Flask(__name__, template_folder='templates')
app.secret_key = "ziyahcantikbeud"

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prediksi'
mysql = MySQL(app)



model = pickle.load(open('lm.pkl', 'rb'))

@app.route('/')
def welcome_get():
    return render_template('index.html')

@app.route('/menupengunjung')
def menu_pengunjung():
    return render_template('menu_pengunjung.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/prediksi')
def prediksi():
    return render_template('Prediksi.html')

def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(-1, 4)
    loaded_model = joblib.load('lm.pkl')
    result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/prediksi/',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
    provinsi = request.form['provinsi']
    [provinsi]
    if provinsi == '11' :
        provinsi = 'Aceh'
    elif provinsi == '12' :
        provinsi = 'Sumatra Utara'
    elif provinsi == '13' :
        provinsi = 'Sumatera Barat'
    elif provinsi == '14' :
        provinsi = 'Riau'
    elif provinsi == '15' :
        provinsi = 'Jambi'
    elif provinsi == '16' :
        provinsi = 'Sumatra Selatan'
    elif provinsi == '17' :
        provinsi = 'Bengkulu'
    elif provinsi == '18' :
        provinsi = 'Lampung'
    elif provinsi == '19' :
        provinsi = 'Bangka Belitung'
    elif provinsi == '21' :
        provinsi = 'Kepulauan Riau'
    elif provinsi == '31' :
        provinsi = 'DKI Jakarta'
    elif provinsi == '32' :
        provinsi = 'Jawa Barat'
    elif provinsi == '33' :
        provinsi = 'Jawa Tengah'
    elif provinsi == '34' :
        provinsi = 'DI Yogyakarta'
    elif provinsi == '35' :
        provinsi = 'Jawa Timur'
    elif provinsi == '36' :
        provinsi = 'Banten'
    elif provinsi == '51' :
        provinsi = 'Bali'
    elif provinsi == '52' :
        provinsi = 'Nusa Tenggara Barat'
    elif provinsi == '53' :
        provinsi = 'Nusa Tenggara Timur'
    elif provinsi == '61' :
        provinsi = 'Kalimantan Barat'
    elif provinsi == '62' :
        provinsi = 'Kalimantan Tengah'
    elif provinsi == '63' :
        provinsi = 'Kalimantan Selatan'
    elif provinsi == '64' :
        provinsi = 'Kalimantan Timur'
    elif provinsi == '65':
        provinsi = 'Kalimantan Utara'
    elif provinsi == '71':
        provinsi = 'Sulawesi Utara'
    elif provinsi == '72':
        provinsi = 'Sulawesi Tengah'
    elif provinsi == '73':
        provinsi = 'Sulawesi Selatan'
    elif provinsi == '74':
        provinsi = 'Sulawesi Tenggara'
    elif provinsi == '75':
        provinsi = 'Gorontalo'
    elif provinsi == '76':
        provinsi = 'Sulawesi Barat'
    elif provinsi == '81':
        provinsi = 'Maluku'
    elif provinsi == '82':
        provinsi = 'Maluku Utara'
    elif provinsi == '91':
        provinsi = 'Papua'
    elif provinsi == '92':
        provinsi = 'Papua Barat'
    else:
        provinsi == 'provinsi tidak ditemukan'
    tahun = request.form['tahun']
    [tahun]
    to_predict_list = request.form.to_dict()
    to_predict_list=list(to_predict_list.values())
    to_predict_list = list(map(float, to_predict_list))
    result = float(ValuePredictor(to_predict_list))
    return render_template("Prediksi.html", result = result, provinsi=provinsi, tahun=tahun)

@app.route('/dataaktual')
def aktual():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM dataset")
    dataset = cursor.fetchall()
    cursor.close()
    return render_template('DataAktual.html', datasets = dataset )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        msg=''
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE  username =%s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['username'] = user[1]
            return redirect(url_for('homeadmin'))
        else:
            msg= 'USERNAME DAN PASSWORD SALAH!!!!'
            return render_template('LoginAdm.html', msg=msg)
    else:
        return render_template("LoginAdm.html")

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/homeadmin')
def homeadmin():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM dataset")
    dataset = cursor.fetchall()
    cursor.close()
    return render_template('HomeAdm.html', username = session['username'], datasets=dataset)

@app.route('/simpan', methods=['POST'])
def simpan():
    provinsi = request.form['provinsi']
    tahun = request.form['tahun']
    luas_tanah = request.form['luas_tanah']
    produktivitas = request.form['produktivitas']
    produksi = request.form['produksi']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO dataset (provinsi, tahun, luas_tanah, produktivitas, produksi) VALUES (%s, %s, %s, %s, %s)", (provinsi, tahun, luas_tanah, produktivitas, produksi, ))
    mysql.connection.commit()
    return redirect(url_for('homeadmin'))

@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    provinsi = request.form['provinsi']
    tahun = request.form['tahun']
    luas_tanah = request.form['luas_tanah']
    produktivitas = request.form['produktivitas']
    produksi = request.form['produksi']

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE dataset SET provinsi=%s, tahun=%s, luas_tanah=%s, produktivitas=%s, produksi=%s WHERE id=%s", (provinsi, tahun, luas_tanah, produktivitas, produksi, id))
    mysql.connection.commit()
    return redirect(url_for('homeadmin'))

@app.route('/hapus/<int:id>', methods=['GET'])
def hapus(id):

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM dataset WHERE  id =%s", (id, ))
    mysql.connection.commit()
    return redirect(url_for('homeadmin'))

if __name__ == "__main__":
    app.run(debug=True)


