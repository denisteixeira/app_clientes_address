from flask import Flask, render_template, request, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector as sql
from app_clients_db import connect_to_db # to import connection function from app_clients_db.py

app=Flask(__name__)
app.secret_key="admin123"
auth = HTTPBasicAuth()

# Login setup
users = {"admin": generate_password_hash("admin102030")}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    
@app.route("/")
@app.route("/index")
@auth.login_required

def index ():
    con = connect_to_db() # make new connection
    if con is None:
        return "Failed to connect to the database" # message for connection failure
    
    try:
        cur=con.cursor()
        cur.execute("SELECT * FROM clientes")
        data=cur.fetchall()
        print("Fetched data:", data)  # Debugging output
        return render_template("index.html", datas=data)

    except Exception as e:
        return f"An error occurred: {e}" # generate any cursor-related errors
    finally:
        if con.is_connected():
            con.close() #close connection



@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    con=connect_to_db() # make new connection
    if con is None:
        return "Failed to connect to the database" # message for connection failure

    if request.method=="POST":
        nome=request.form["nome"]
        email=request.form["email"]
        idade=request.form.get("idade")
        cidade=request.form["cidade"]
        cpf=request.form["cpf"]
       
        try:
            cur=con.cursor()
            cur.execute("INSERT INTO clientes (NOME, EMAIL, IDADE, CIDADE, CPF) VALUES (%s, %s, %s, %s, %s)", (nome, email, idade, cidade, cpf))
            con.commit()
            flash("Dados cadastrados", "success")
            return redirect (url_for("index"))
        except Exception as e:
                return f"An error occurred: {e}"
        finally:
            if con.is_connected():
                con.close()
            
    return render_template("add_user.html")

@app.route("/edit_user/<string:id>", methods=["POST", "GET"])
def edit_user(id):
    con=connect_to_db() # make new connection
    if con is None:
        return "Failed to connect to the database" # message for connection failure
    
    if request.method=="POST":
        nome=request.form["nome"]
        email=request.form["email"]
        idade=request.form.get("idade")
        cidade=request.form["cidade"]
        cpf=request.form["cpf"]

        try:
            cur=con.cursor()
            cur.execute("UPDATE clientes SET NOME=%s, EMAIL=%s, IDADE=%s, CIDADE=%s, CPF=%s WHERE ID=%s", (nome, email, idade, cidade, cpf, id))
            con.commit()
            flash("Dados atualizados", "success")
            return redirect(url_for("index"))
        except Exception as e:
            return f"An error occurred {e}"
        finally:
            if con.is_connected():
                con.close()

    try:
        if con:
            cur=con.cursor(dictionary=True)
            cur.execute("SELECT * FROM clientes WHERE ID =%s", (id,))
            data=cur.fetchone()
            print("Fetched data for editing:", data)
            return render_template("edit_user.html", datas=data)
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        if con.is_connected():
            con.close()

@app.route("/delete_user/<string:id>", methods=["GET"])
def delete_user(id):
    con=connect_to_db() # make new connection
    if con is None:
        return "Failed to connect to the database" # message for connection failure
    
    try:
        cur=con.cursor()
        cur.execute("DELETE FROM clientes WHERE ID=%s", (id,))
        con.commit()
        flash("Dados deletados", "warning")
        return redirect(url_for("index"))
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        if con.is_connected():
            con.close()


if __name__=='__main__':
    app.run(host='0.0.0.0', port=80, debug=True)