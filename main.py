from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import json
from flask_bcrypt import Bcrypt

app=Flask(__name__)
bcrypt = Bcrypt(app)

#Antes de usar o flash, certifique-se de inicializar a extensão no seu aplicativo Flask. 
app.secret_key = 'caroline'

#route -> 
#funcao -> o que vc quer exibir naquela pagina
@app.route("/")
def home():
    return render_template("home.html")


def verificar_autenticacao():
    if 'usuario_autenticado' not in session or not session['usuario_autenticado']:
        return redirect("/login")

@app.route("/login")
def renderLogin():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login():
    username=request.form.get('username')
    password=request.form.get('password')

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "select * from t_login WHERE username = %s;"
        cursor.execute(sql, (username,))
        user=cursor.fetchone()

        # if username == user[0] and password==user[1]:
        #     session['usuario_autenticado'] = True
        #     return render_template("homepage.html")

        if user and bcrypt.check_password_hash(user[1], password):
            session['usuario_autenticado'] = True
            return render_template("homepage.html")

        flash ('DADOS INVÁLIDOS')
        return redirect("/login")
    
@app.route('/logout')
def logout():
    session['usuario_autenticado'] = False
    return redirect("/login")

@app.route("/homepageAdmin")
def renderHomepageAdmin():
    return render_template("homepageAdmin.html")

@app.route("/registarUsuario")
def renderRegistarUsuario():
    return render_template("registarUsuario.html")

@app.route("/registarUsuario", methods=['POST'])
def registarUsuario():
    username = request.form.get('username')
    password = request.form.get('password')

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "select * from t_login;"
        cursor.execute(sql)
        bdtLogin=cursor.fetchall()

        for user in bdtLogin:
            
            if user[0]==username:
                    flash('USERNAME JÁ UTILIZADO','usernameUtilizado')
                    return redirect("/registarUsuario")
                
    if conexao.is_connected():
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        sql = "INSERT INTO t_login (username, password) VALUES (%s, %s);"
        cursor.execute(sql, (username, hashed_password,))

        conexao.commit()

        flash('USUARIO REGISTADO COM SUCESSO!', 'usuario_registadoComSucesso')
        
        cursor.close()
        conexao.close()
     
        return redirect("/registarUsuario")
            
@app.route("/homepage")
def homepage():
    verificar_autenticacao()
    return render_template("homepage.html")
            
@app.route("/registarCliente")
def renderRegistarCliente():
    return render_template("registarCliente.html")

@app.route("/registarCliente", methods=['POST'])
def registarCliente():
    nif = int(request.form.get('nif'))
    nome = request.form.get('nome')
    morada = request.form.get('morada')
    email = request.form.get('email')
    telefone = request.form.get('telefone')

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "select * from t_cliente;"
        cursor.execute(sql)
        bdtClientes=cursor.fetchall()

        for cliente in bdtClientes:
            
            if cliente[0]==nif:
                    flash('CLIENTE JÁ POSSUI REGISTO','cliente_jaComRegisto')
                    return render_template("registarCliente.html")
                
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "INSERT INTO t_cliente (nif, nome, morada, email, telefone) VALUES (%s, %s, %s, %s, %s);"
        val = (nif, nome, morada, email, telefone)
        cursor.execute(sql, val)

        conexao.commit()

        flash('CLIENTE REGISTADO COM SUCESSO!', 'cliente_registadoComSucesso')
        
        cursor.close()
        conexao.close()
     
        return redirect("/registarCliente")
    
@app.route("/dadosCliente")
def renderDadosCliente():
    return render_template("dadosCliente.html")
    
@app.route("/mostrarDadosCliente", methods=['POST'])
def dadosCliente():
    nif = int(request.form.get('nif'))
    
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_cliente WHERE nif = %s;"
        cursor.execute(sql, (nif,))
        bdtClientes=cursor.fetchall()
        cursor.close()

        if bdtClientes:
            return render_template("mostrarDadosCliente.html", bdtClientes=bdtClientes)
        else:
            flash('CLIENTE NÃO POSSUI REGISTO','cliente_semRegisto')

    conexao.close()
    return render_template("dadosCliente.html")
    
        
@app.route("/atualizarDadosCliente", methods=['POST'])
def atualizarDadosCliente():
    nif = int(request.form.get('nif_display'))

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_cliente WHERE nif = %s;"
        cursor.execute(sql, (nif,))
        bdtClientes=cursor.fetchall()

    conexao.commit()
    cursor.close()
    conexao.close()
    
    return render_template("atualizarDadosCliente.html", bdtClientes=bdtClientes)

@app.route("/atualizarDadosC", methods=['POST'])
def atualizarDadosC():
    nif = int(request.form.get('nif'))
    nome = request.form.get('nome')
    morada = request.form.get('morada')
    email = request.form.get('email')
    telefone = request.form.get('telefone')

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "UPDATE t_cliente SET nome=%s, morada=%s, email=%s, telefone=%s WHERE nif = %s;"
        val = (nome, morada, email, telefone, nif)
        cursor.execute(sql, val)

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_cliente WHERE nif = %s;"
        cursor.execute(sql, (nif,))
        bdtClientes=cursor.fetchall()
                
        conexao.commit()

        cursor.close()
        conexao.close()
     
        return render_template("mostrarDadosCliente.html", bdtClientes=bdtClientes)

@app.route("/registarProduto")
def renderRegistarProduto():
    return render_template("registarProduto.html")

@app.route("/registarProduto", methods=['POST'])
def registarProduto():
    descricao = request.form.get('descricao')
    valor_venda= request.form.get('valor_venda')
    stock = request.form.get('stock')
    categoria = request.form.get('categoria')
    foto = request.form.get('foto')

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "INSERT INTO t_produto (descricao, valor_venda, stock, categoria, foto) VALUES (%s, %s, %s, %s, %s);"
        val = (descricao, valor_venda, stock, categoria, foto)
        cursor.execute(sql, val)

        conexao.commit()

        flash('PRODUTO REGISTADO COM SUCESSO!', 'produto_registadoComSucesso')
        
        cursor.close()
        conexao.close()
     
        return redirect("/registarProduto")

@app.route("/listarProdutos", methods=['GET', 'POST'])
def listarProdutos():

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_produto;"
        cursor.execute(sql)
        bdtProdutos=cursor.fetchall()

    conexao.commit()
    cursor.close()
    conexao.close()
    return render_template("listarProdutos.html", bdtProdutos=bdtProdutos)

@app.route("/listarProdutosPorCategoria", methods=['GET', 'POST'])
def listarProdutosPorCategoria():
    categoria=request.form.get('categoria')
 
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_produto WHERE categoria = %s;"
        cursor.execute(sql, (categoria,))
        bdtProdutosCategoria=cursor.fetchall()
 
    conexao.commit()
    cursor.close()
    conexao.close()
    return render_template("listarProdutos.html", bdtProdutosCategoria=bdtProdutosCategoria)

@app.route("/listarProdutosPorCodigo", methods=['GET', 'POST'])
def listarProdutosPorCodigo():
    idProduto=request.form.get('id_prod')
 
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    bdtProdutoEspecifico = []
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_produto WHERE id_produto = %s;"
        cursor.execute(sql, (idProduto,))
        bdtProdutoEspecifico=cursor.fetchall()
 
    conexao.commit()
    cursor.close()
    conexao.close()
    
    return render_template("listarProdutos.html", bdtProdutoEspecifico=bdtProdutoEspecifico)

@app.route("/registarCartao")
def registarCartao():
    return render_template("registarCartao.html")

@app.route("/registarCartao", methods=['POST'])
def verificarCliente():
    nif = int(request.form.get('nif'))
    n_cartao = request.form.get('n_cartao')
    

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
    
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "select * from t_cliente;"
        cursor.execute(sql)
        bdtClientes=cursor.fetchall()

        cliente_existe = False
        for usuario in bdtClientes:
            if usuario[0] == nif:
                cliente_existe = True
                break
        if cliente_existe:
            pass
        else:
            flash('CLIENTE NÃO REGISTADO', 'cliente_naoRegistado')
            return redirect("/registarCartao")

        cliente_sem_cartao=False    
        for cliente in bdtClientes:
            
            if cliente[0]==nif and cliente[5]=="0" :
                    cliente_sem_cartao=True
                    break
        if cliente_sem_cartao:
            pass
        else:
            flash('CLIENTE JÁ POSSUI CARTÃO ASSOCIADO','cliente_jaComCartao')
            return redirect("/registarCartao")
        
        sql = "UPDATE t_cliente SET n_cartao = %s WHERE nif = %s;"
        val = (n_cartao, nif)
        cursor.execute(sql, val)

    conexao.commit()

    flash('CARTÃO ASSOCIADO COM SUCESSO!','cartao_associadoComSucesso')
                
    cursor.close()
    conexao.close()

    return redirect("/registarCartao")

@app.route("/consultarPontosCartao")
def renderConsultarPontos():
    return render_template("consultarPontos.html")
    
@app.route("/mostrarPontos", methods=['POST'])
def consultarPontos():
    n_cartao = int(request.form.get('n_cartao'))
    
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_cartao WHERE n_cartao = %s;"
        cursor.execute(sql, (n_cartao,))
        bdtPontos=cursor.fetchall()
        cursor.close()

        if bdtPontos:
            # Calcular o valor total dos  pontos
            # [0][2] -> numero cartao e pontos
            pontos = bdtPontos[0][2]
            valor_total = pontos*10
            return render_template("mostrarPontos.html", bdtPontos=bdtPontos, valor_total=valor_total)
        else:
            flash('CLIENTE NÃO POSSUI CARTÃO','cliente_semRegisto')

    conexao.close()
    return render_template("consultarPontos.html")

@app.route("/registarFatura")
def renderRegistarFatura():
    return render_template("registarFatura.html")

@app.route("/registarFatura", methods=['GET', 'POST'])
def registarFatura():
    nif=request.form.get('nif')
    data_atual = datetime.now().strftime("%Y-%m-%d")
 
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "INSERT INTO t_fatura (nif,data) VALUES (%s,%s);"
        cursor.execute(sql, (nif, data_atual,))
        
 
    conexao.commit()
    cursor.close()
    conexao.close()
    
    return render_template("registarFatura.html")

# #CRUD

# #create
# comando = 'INSERT INTO t_cliente (nif,nome,morada,email,telefone) values (586954721, "Caroline Budal Arins", "Rua da Alegria - 15", "carolba@hotmail.com", "985444165")'
# cursor.execute(comando)
# conexao.commit() #edita o banco de dados

# #read
# comando = f'SELECT * FROM t_cliente'
# cursor.execute(comando)
# resultado = cursor.fetchall() #ler o banco de dados
# print(resultado)

# #update
# comando = 'UPDATE t_cliente SET telefone= "" WHERE nif='
# cursor.execute(comando)
# conexao.commit() #edita o banco de dados

# #delete
# comando = 'DELETE FROM t_cliente WHERE nif='
# cursor.execute(comando)
# conexao.commit() #edita o banco de dados


#colocar o site no ar
if __name__=="__main__":
    app.run(debug=True)