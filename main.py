import psycopg2
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="python", host="localhost", user="postgres", password="root", port="5432")
    return conn

@app.route('/')
def index():
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM USERS ORDER BY ID ASC''')
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/create', methods=['POST'])
def create():
    conn = db_conn()
    cursor = conn.cursor()
    name = request.form['name']
    cursor.execute('''INSERT INTO USERS (name) VALUES (%s)''', (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    conn = db_conn()
    cursor = conn.cursor()
    name = request.form['name']
    id = request.form['id']
    cursor.execute('''UPDATE USERS SET name=%s WHERE ID=%s''', (name, id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete():
    conn = db_conn()
    cursor = conn.cursor()
    id = request.form['id']
    cursor.execute('''DELETE FROM USERS WHERE ID=%s''', (id))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

#aqui começa os endpoint para apirest
@app.route('/api/index', methods=['GET'])
def api_index():
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM USERS ORDER BY ID ASC''')
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/edit/<resource_id>', methods=['GET'])
def api_edit(resource_id):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM USERS WHERE ID=%s''', (resource_id))
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route('/api/create', methods=['POST'])
def api_create():
    new_request = request.get_json()
    conn = db_conn()
    cursor = conn.cursor()
    name = new_request['name']
    cursor.execute('''INSERT INTO USERS (name) VALUES (%s)''', (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message:":"Criado com sucesso"})

@app.route('/api/update/<int:resource_id>', methods=['PUT'])
def api_update(resource_id):
    update_data = request.get_json()
    conn = db_conn()
    cursor = conn.cursor()
    name = update_data['name']
    cursor.execute('''UPDATE USERS SET name=%s WHERE ID=%s''', (name, resource_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message:":"Atualizado com sucesso"})

@app.route('/api/delete/<resource_id>', methods=['DELETE'])
def api_delete(resource_id):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM USERS WHERE ID=%s''', (resource_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message:":"Registro deletado com sucesso"})


if __name__ == "__main__":
    app.run(debug=True, port=8000)
