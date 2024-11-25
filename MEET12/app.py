from flask import Flask, request, render_template
import secrets
from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="projectx",
    password=""
)

@app.route('/')
@app.route('/google')
def google():
    return render_template('google.html')

@app.route('/home.html')
def home():
    return render_template('home.html')


@app.route('/simpan', methods=["POST", "GET"])
def simpan():
    if request.method == "POST":
        try:
            name = request.form["name"]
            gender = request.form["gender"]
            country = request.form["country"]
            cursor = mydb.cursor()
            query = "INSERT INTO user (id, name, gender, country) VALUES (%s, %s, %s, %s)"
            data = (None, name, gender, country)
            cursor.execute(query, data)
            mydb.commit()
            cursor.close()
            return redirect(url_for('tampil'))
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"
    else:
        return render_template('home.html')

    
@app.route('/tampil', methods=["GET"])
def tampil():
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        cursor.close()
        return render_template('tampil.html', users=users)
    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}"
    
@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    if request.method == "POST":
        try:
            name = request.form["name"]
            gender = request.form["gender"]
            country = request.form["country"]
            
            cursor = mydb.cursor()
            query = "UPDATE user SET name = %s, gender = %s, country = %s WHERE id = %s"
            data = (name, gender, country, id)
            cursor.execute(query, data)
            mydb.commit()
            cursor.close()
            return f"Data dengan ID {id} berhasil diperbarui."
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"
    else:
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM user WHERE id = %s", (id,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                return render_template('update.html', user=user)
            else:
                return f"Data dengan ID {id} tidak ditemukan."
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

@app.route('/delete/<int:user_id>', methods=['POST', 'GET'])
def delete_user(user_id):
    try:
        cursor = mydb.cursor()
        query = "DELETE FROM user WHERE id = %s"
        cursor.execute(query, (user_id,))
        mydb.commit()
        cursor.close()
        return redirect(url_for('tampil'))
    except Exception as e:
        return f"Terjadi kesalahan saat menghapus data: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
