from flask import Flask, render_template, request, redirect, flash, session, url_for
import mysql.connector
import json

app=Flask(__name__)
#criar a 1 pagina do site

#Adding a secret key to our app - is used to secure the session cookie 
app.secret_key = 'caroline'
#define o tipo de armazenamento a ser usado para armazenar dados de sessão no Flask.
#Quando você configura a aplicação Flask para usar o armazenamento de sessão no sistema de arquivos, as informações de sessão são salvas em arquivos no sistema de arquivos do servidor.
app.session_interface = 'filesystem'

#route -> 
#funcao -> o que vc quer exibir naquela pagina
@app.route("/")
def renderHome():
    return render_template("home.html")

def verificar_autenticacao():
    if 'usuario_autenticado' not in session:
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
        sql = "select * from t_login;"
        cursor.execute(sql)
        bdtLogin=cursor.fetchall()

        for cliente in bdtLogin:
            
            if cliente[0]==username and cliente[1]==password:
                    session['usuario_autenticado'] = True
                    return render_template("homepage.html")

        flash ('DADOS INVÁLIDOS')
        return redirect("/login")
            
@app.route("/homepage")
def homepage():
    verificar_autenticacao()
    return render_template("homepage.html")

@app.route('/logout')
def logout():
    session['usuario_autenticado'] = False
    return redirect("/login")
    
            
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

    
@app.route("/listarProdutos")
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