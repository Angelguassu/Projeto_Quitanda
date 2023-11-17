
from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql

import uuid

app = Flask(__name__)
app.secret_key = "quitandadozezinho"


usuario = "admin"
senha = "1234"
login = False

# ------------------------------ FUNÇÃO PARA VERIFICAR A SESSÃO ------------------------------

#FUNÇÃO PARA VERIFICAR SESSÃO
def verifica_sessao():
    if "login" in session and session["login"]:
        return True
    else:
        return False


#CONEXÃO COM O BANCO DE DADOS
def conecta_database():
    conexao = sql.connect("db_quitanda.db")
    conexao.row_factory = sql.Row
    return conexao


#INICIAR O BANCO DE DADOS
def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
    conexao.commit()
    conexao.close()


#ROTA DA PÁGINA INICIAL
@app.route('/')
def index():
    global login
    iniciar_db() #chamando o BD
    conexao = conecta_database()
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
    conexao.close()
    if verifica_sessao():
        login = True
    else:
        login = False
    return render_template("home.html", produtos=produtos,login=login)
   
#ROTA PARA ABRIR O FORMULÁRIO DE CADASTRO
@app.route("/novopost")
def novopost():
    if verifica_sessao():
        return render_template("novopost.html")
    else:
        return render_template("login.html")




#ROTA PARA RECEBER A POSTAGEM DO FORMULÁRIO
@app.route("/cadpost", methods=['POST'])
def cadpost():
    titulo = request.form['titulo']
    conteudo = request.form['conteudo']
    conexao = conecta_database()
    conexao.execute('INSERT INTO produtos (titulo, conteudo) VALUES (?, ?)', (titulo, conteudo))
    conexao.commit()
    conexao.close()
    return redirect('/')

# ROTA DE EXCLUSÃO
@app.route("/excluir/<id>")
def excluir(id):
    #id = int(id)
    conexao = conecta_database()
    conexao.execute('DELETE FROM produtos WHERE id = ?',(id,))
    conexao.commit()
    conexao.close()
    return redirect('/')

#ROTA DA PÁGINA LOGIN
    
# ------------------------------ ROTA DA PÁGINA LOGIN ------------------------------
@app.route("/login")
def login():
    return render_template("login.html")


#ROTA PARA VERIFICAR O ACESSO O ADMIN
# ------------------------------ ROTA DA PAGINA ADM ------------------------------
@app.route ("/adm")
def adm():
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database()
        produtos = conexao.execute( 'SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
        conexao.close()
        title = "Administração"
        return render_template("adm.html" , produtos=produtos , title=title)
    else:
        return redirect("/login")
    
# ------------------------------ ROTA PARA VERIFICAR O ACESSO AO ADMIN ------------------------------
@app.route("/acesso", methods=['POST'])
def acesso():
    global usuario, senha
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]


    if usuario == usuario_informado and senha == senha_informada:
        session["login"] = True
        return redirect('/') #homepage
    else:
        return render_template("login.html",msg="Usuário/Senha estão errados!")
   


#código do LOGOUT
        return render_template("login.html",msg="O usuário e a sua senha estão INCORRETOS!!")
    
# ------------------------------ CÓDIGO DO LOGOUT ------------------------------´
@app.route("/logout")
def logout():
    global login
    login = False
    session.clear()
    return redirect('/')
    
# ------------------------------ CONEXÃO COM O BANCO DE DADOS ------------------------------

def conecta_database():
    conexao = sql.connect("db_quitanda.db")
    conexao.row_factory = sql.Row
    return conexao

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")
# ------------------------------ INICIAR O BANCO DE DADOS ------------------------------

#CRIAR A ROTA DO EDITAR
@app.route("/editar/<id>")
def editar(id):
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database()
        posts = conexao.execute('SELECT * FROM posts WHERE id = ?',(id,)).fetchall()
def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
        conexao.commit()
        conexao.close()
        return render_template("editar.html", posts=posts)

# ------------------------------ ROTA DA PÁGINA INICIAL ------------------------------

#CRIAR A ROTA PARA TRATAR A EDIÇÃO
@app.route("/editpost", methods=['POST'])
def editpost():
    id = request.form['id']
    titulo = request.form['titulo']
    conteudo = request.form['conteudo']
@app.route("/")
def index():
    iniciar_db()
    conexao = conecta_database()
    conexao.execute('UPDATE posts SET titulo = ?, conteudo = ? WHERE id = ?',(titulo,conteudo,id,))
    conexao.commit() #Confirma a alteração no BD
    produtos = conexao.execute('SELECT * FROM produtos ORDER BY id_prod DESC').fetchall()
    conexao.close()
    return redirect('/') # Vai para HOME
    title = "Home"
    return render_template("home.html", produtos=produtos, title=title)

# ------------------------------ ROTA PARA ABRIR O FORMULARIO DE CADASTRO ------------------------------
@app.route("/cadprodutos")
def cadprodutos():
    if verifica_sessao():
        title = "Cadastro de produtos"
        return render_template("cadastro.html",title=title)
    else:
        return redirect("/login")

# ------------------------------ ROTA PARA RECEBER A POSTAGEM DO FORMULARIO ------------------------------
@app.route("/cadastro",methods=["post"])
def cadastro():
	if verifica_sessao():
		nome_prod=request.form['nome_prod']
		desc_prod=request.form['desc_prod']
		preco_prod=request.form['preco_prod']
		img_prod=request.files['img_prod']
		id_foto=str(uuid.uuid4().hex)
		filename=id_foto+nome_prod+'.png'
		img_prod.save("static/img/produtos/"+filename )
		conexao = conecta_database()
		conexao.execute('INSERT INTO produtos (nome_prod, desc_prod, preco_prod,img_prod) VALUES (?, ?, ?, ?)', (nome_prod, desc_prod, preco_prod, filename))
		conexao.commit()
		conexao.close()
		return redirect("/adm")
	else:
		return redirect("/login")
     
# ------------------------------ ROTA DE EXCLUSÃO ------------------------------
@app.route("/excluir/<id>")
def excluir(id):
     if verifica_sessao():
          id = int(id)
          conexao = conecta_database()
          conexao.execute('DELETE FROM produtos WHERE id_prod = ?',(id,))
          conexao.commit()
          conexao.close()
          return redirect('/adm')
     else:
          return redirect("/login")
     
# ------------------------------ ROTA DE EDITAR ------------------------------
@app.route("/editprodutos/<id_prod>")
def editar(id_prod):
     if verifica_sessao():
          iniciar_db()
          conexao = conecta_database()
          produtos = conexao.execute('SELECT * FROM produtos WHERE id_prod = ?',(id_prod,)).fetchall()
          conexao.close()
          title = "Edição dos produtos"
          return render_template("editprodutos.html",produtos=produtos,title=title)
     else:
          return redirect("/login")
     
# ------------------------------ CRIAR A ROTA PARA TRATAR A EDIÇÃO ------------------------------
@app.route("/editarprodutos", methods=['POST'])
def editprod():
    id_prod=request.form['id_prod']
    nome_prod=request.form['nome_prod']
    desc_prod=request.form['desc_prod']
    preco_prod=request.form['preco_prod']
    img_prod=request.files [' img_prod']
    id_foto=str(uuid.uuid4().hex)
    filename=id_foto+nome_prod+'.png'
    img_prod.save("static/img/produtos/"+filename)
    conexao = conecta_database()
    conexao.execute('UPDATE produtos SET nome_prod = ?, desc_prod = ?, preco_prod = ?, img_prod = ? WHERE id_prod = ?',(nome_prod,desc_prod,preco_prod,filename,id_prod))
    conexao.commit()
    conexao.close()
    return redirect('/adm')

# ------------------------------ ROTA DE PESQUISA ------------------------------
@app.route("/busca",methods=["post"])
def busca():
     busca=request.form['buscar']
     conexao = conecta_database()
     produtos = conexao.execute('SELECT * FROM produtos WHERE nome_prod LIKE "%" || ? || "%"',(busca,)).fetchall()
     title = "Home"
     return render_template("home.html", produtos=produtos, title=title)

# ------------------------------ FINAL DO CODIGO - EXECUTANDO O SERVIDOR ------------------------------

#FINAL DO CÓDIGO - EXECUTANDO O SERVIDOR
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
app.run(debug=True)