from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
from flask_bcrypt import Bcrypt

app=Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = 'caroline'

#route -> 
#funcao -> o que vc quer exibir naquela pagina
@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def renderLogin():
    return render_template("login.html")

@app.route("/login", methods=['GET', 'POST'])
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

        if user[2]=='0':
            if user and bcrypt.check_password_hash(user[1], password):
                session['usuario_autenticado'] = username
                return redirect("/homepage")
            else:
                flash ('DADOS INVÁLIDOS', 'dadosInvalidosLogin')
                return redirect("/login")
        else:
            flash ('USUARIO INATIVO. CONTACTE O ADMINISTRADOR!', 'usuarioInativoLogin')
            return redirect("/login")
        
def verificar_autenticacao():
    if 'usuario_autenticado' not in session or not session['usuario_autenticado']:
        return False
    else:
        return True
    
@app.route('/logout')
def logout():
    session.pop('usuario_autenticado', None)
    flash('LOGOUT EFETUADO COM SUCESSO!','logoutEfetuadoComSucesso')
    return redirect("/login")

@app.route("/homepage")
def homepage():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("homepage.html")
       
@app.route("/registarUsuario")
def renderRegistarUsuario():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("registarUsuario.html")

@app.route("/registarUsuario", methods=['POST'])
def registarUsuario():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
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
            
@app.route("/registarCliente")
def renderRegistarCliente():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("registarCliente.html")

@app.route("/registarCliente", methods=['POST'])
def registarCliente():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
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
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("dadosCliente.html")

@app.route("/mostrarDadosCliente", methods=['POST'])
def dadosCliente():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
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
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
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

@app.route("/atualizarDados", methods=['POST'])
def atualizarDados():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
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
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("registarProduto.html")

@app.route("/registarProduto", methods=['POST'])
def registarProduto():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    descricao = request.form.get('descricao')
    valor_venda= request.form.get('valor_venda')
    stock = request.form.get('stock')
    categoria = request.form.get('categoria')
    foto = request.form.get('foto')
    data_validade= request.form.get('data_validade')

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "INSERT INTO t_produto (descricao, valor_venda, stock, categoria, foto, data_validade) VALUES (%s, %s, %s, %s, %s, %s);"
        val = (descricao, valor_venda, stock, categoria, foto, data_validade)
        cursor.execute(sql, val)

        conexao.commit()

        flash('PRODUTO REGISTADO COM SUCESSO!', 'produto_registadoComSucesso')
        
        cursor.close()
        conexao.close()
     
        return redirect("/registarProduto")

@app.route("/listarProdutos", methods=['GET', 'POST'])
def listarProdutos():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_produto WHERE ativo='0';"
        cursor.execute(sql)
        bdtProdutos=cursor.fetchall()
        conexao.commit()
        cursor.close()
    
    conexao.close()
    return render_template("listarProdutos.html", bdtProdutos=bdtProdutos)

@app.route("/listarProdutosPorCategoria", methods=['GET', 'POST'])
def listarProdutosPorCategoria():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    categoria=request.form.get('categoria')
 
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_produto WHERE categoria = %s and ativo='0';"
        cursor.execute(sql, (categoria,))
        bdtProdutosCategoria=cursor.fetchall()
        conexao.commit()
        cursor.close()
    
    conexao.close()
    return render_template("listarProdutos.html", bdtProdutosCategoria=bdtProdutosCategoria)

@app.route("/listarProdutosPorCodigo", methods=['GET', 'POST'])
def listarProdutosPorCodigo():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
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
        sql = "SELECT * FROM t_produto WHERE id_produto = %s and ativo='0';"
        cursor.execute(sql, (idProduto,))
        bdtProdutoEspecifico=cursor.fetchall()
 
    conexao.commit()
    cursor.close()
    conexao.close()
    
    return render_template("listarProdutos.html", bdtProdutoEspecifico=bdtProdutoEspecifico)
    
@app.route("/listarProdutosAdm", methods=['GET', 'POST'])
def listarProdutosAdm():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    idProduto=request.form.get('id_prod')
     
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    bdtProdutosAdm = []
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_produto WHERE id_produto = %s;"
        cursor.execute(sql, (idProduto,))
        bdtProdutosAdm=cursor.fetchall()
        cursor.close()
    
    conexao.close()
    
    return render_template("desativarProduto.html", bdtProdutosAdm=bdtProdutosAdm)
 
@app.route("/desativarProduto")
def desativarProduto():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("desativarProduto.html")

@app.route("/desativarProduto2", methods=['GET','POST'])
def desativarProduto2():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    codProduto = request.form.get('codigoProduto')
    
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "UPDATE t_produto SET ativo='1' WHERE id_produto = %s;"
        cursor.execute(sql, (codProduto,))
        conexao.commit()
        cursor.close()
        
    conexao.close()

    flash('PRODUTO DESATIVADO COM SUCESSO!','produtoDesativadoComSucesso')
    
    return redirect("/desativarProduto")

@app.route("/ativarProduto", methods=['GET','POST'])
def ativarProduto():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    codProduto = request.form.get('codigoProduto')
    
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "UPDATE t_produto SET ativo='0' WHERE id_produto = %s;"
        cursor.execute(sql, (codProduto,))
        conexao.commit()
        cursor.close()
        
    conexao.close()

    flash('PRODUTO ATIVADO COM SUCESSO!','produtoAtivadoComSucesso')
    
    return redirect("/desativarProduto")

@app.route("/listarProdutosValidadeProxima")
def renderListarProdutosValidadeProxima():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("listarProdutosValidade.html")

@app.route("/listarProdutosValidadeProxima", methods=['POST'])
def listarProdutosValidadeProxima():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    bdtProdutosValidadeProxima=[]
 
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_produto WHERE data_validade <= DATE_ADD(CURDATE(), INTERVAL 3 DAY);"
        cursor.execute(sql)
        bdtProdutosValidadeProxima=cursor.fetchall()

        cursor.close()
        conexao.close()
        return render_template("listarProdutosValidade.html", bdtProdutosValidadeProxima=bdtProdutosValidadeProxima)

@app.route("/registarCartao")
def registarCartao():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("registarCartao.html")

@app.route("/registarCartao", methods=['POST'])
def verificarCliente():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
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

@app.route("/renderCancelarCartao")
def rendercancelarCartao():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("cancelarCartao.html")

@app.route("/cancelarCartao")
def cancelarCartao():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    
    n_cartao = session['nCartao']
    
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
    
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT ativo FROM t_cartao WHERE n_cartao = %s;"
        cursor.execute(sql, (n_cartao,))
        ativo=cursor.fetchone()[0]

        if ativo=='1':
            flash ('CARTÃO JÁ CONSTA CANCELADO', 'cartaoJaConstaCancelado')
        else:
            sql1 = "UPDATE t_cartao SET ativo = '1' WHERE n_cartao = %s;"
            cursor.execute(sql1, (n_cartao,))
            conexao.commit()
            flash ('CARTÃO CANCELADO COM SUSCESSO!', 'cartaoCanceladoComSucesso')

    cursor.close()
    conexao.close()

    return redirect("/renderCancelarCartao")

@app.route("/acaoCartao", methods=['GET', 'POST'])
def acaoCartao():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    n_cartao=request.form.get('n_cartao')
    session['nCartao']=n_cartao
    acao=request.form.get('acao')

    if acao=="substituir":
        return render_template("substituirCartao.html")
    else:
        return redirect("/cancelarCartao")

@app.route("/substituirNumeroCartao", methods=['POST','GET'])
def substituirNumeroCartao():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    n_cartao = request.form.get('n_cartao')
    novo_cartao = request.form.get('novo_cartao')

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
    
    if conexao.is_connected():
        cursor = conexao.cursor()

        sql3 = "SELECT ativo FROM t_cartao WHERE n_cartao = %s;"
        cursor.execute(sql3, (n_cartao,))
        ativo=cursor.fetchone()[0]

        if ativo=='1':
        
            sql = "SELECT nif FROM t_cliente WHERE n_cartao = %s;"
            cursor.execute(sql, (n_cartao,))
            nif=cursor.fetchone()[0]
            
            sql2 = "UPDATE t_cliente SET n_cartao = %s WHERE nif=%s;"
            cursor.execute(sql2, (novo_cartao,nif,))
            conexao.commit()

            sql4 = "SELECT valorCartao FROM t_cartao WHERE n_cartao = %s;"
            cursor.execute(sql4, (n_cartao,))
            valorCartao=cursor.fetchone()[0]

            sql5 = "UPDATE t_cartao SET valorCartao = %s WHERE n_cartao=%s;"
            cursor.execute(sql5, (valorCartao,novo_cartao,))
            conexao.commit()

            sql6 = "UPDATE t_cartao SET valorCartao = 0 WHERE n_cartao=%s;"
            cursor.execute(sql6, (n_cartao,))
            conexao.commit()

            cursor.close()

            flash('CARTAO SUBSTITUÍDO COM SUCESSO!', 'cartaoSubstituidoComSucesso')
            return render_template('substituirCartao.html')

        else:
            flash('CARTAO AINDA ATIVO. CANCELE-O ANTES DE O SUBSTITUIR.', 'cartaoAindaAtivo')
            return render_template('cancelarCartao.html')
    
    conexao.close()

    return redirect("/homepage")

@app.route("/consultarCartao")
def renderConsultarPontos():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("consultarCartao.html")
    
@app.route("/consultarCartao", methods=['POST'])
def consultarCartao():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
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
        bdtValorCartao=cursor.fetchall()
        cursor.close()

        if bdtValorCartao:
            # [0][2] -> posicao da coluna valorCartao na base de dados
            valor_total = bdtValorCartao[0][2]
            return render_template("mostrarDadosCartao.html", bdtValorCartao=bdtValorCartao, valor_total=valor_total)
        else:
            flash('CARTÃO INEXISTENTE OU INATIVO','cartaoNaoExistente')

    conexao.close()
    return render_template("consultarCartao.html")

@app.route("/registarFatura")
def renderRegistarFatura():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("registarFatura.html")

@app.route("/registarFatura", methods=['POST'])
def registarFatura():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    
    nif=request.form.get('nif')
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if 'produtosDaFatura' in session:
        session.pop('produtosDaFatura', None)

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    cursor = conexao.cursor()

    sql = "INSERT INTO t_fatura (nif,data) VALUES (%s,%s);"
    cursor.execute(sql, (nif, data_atual,))
    conexao.commit()

    sql1 = "SELECT * FROM t_fatura WHERE data= %s and nif=%s;"
    cursor.execute(sql1, (data_atual, nif,))
    dadosFatura = cursor.fetchall()
    session['id_fatura']=dadosFatura[0][0]

    cursor.close()
    conexao.close()
    
    return redirect("/registarLinhaFatura")

@app.route("/registarLinhaFatura")
def renderRegistarLinhaFatura():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("registarLinhaFatura.html")

@app.route("/registarLinhaFatura", methods=['GET', 'POST'])
def registarLinhaFatura():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    
    session['id_produto']=request.form.get('id_produto')
        
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    cursor = conexao.cursor()
    sql = "SELECT * FROM t_produto WHERE id_produto = %s;"
    cursor.execute(sql, (session['id_produto'],))
    resultado= cursor.fetchall()
    session['descricaoItem']= resultado[0][1]
    ativo = resultado[0][7]

    if ativo=='0':

        sql1 = "INSERT INTO t_linhafat (id_produto, descricao, id_fatura) VALUES (%s, %s, %s);"
        val= (session['id_produto'], session['descricaoItem'], session['id_fatura'])
        cursor.execute(sql1, val)
        conexao.commit()

        sql2 = "SELECT * FROM t_linhafat WHERE id_produto = %s and qtd is null and id_fatura=%s;"
        cursor.execute(sql2, (session['id_produto'], session['id_fatura'],))
        bdIdDescr = cursor.fetchall()
        session['id_linhaFatura']= bdIdDescr[0][0]
            
    else: 
        flash('PRODUTO DESATIVADO. SE PRECISO CONTACTE O ADMINISTRADOR', 'produtoDesativado')
        return render_template("registarLinhaFatura.html")
    
    cursor.close()

    conexao.close()
    
    return render_template("registarLinhaFatura2.html", bdIdDescr=bdIdDescr)

@app.route("/registarLinhaFatura2")
def renderRegistarLinhaFatura2():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    return render_template("registarLinhaFatura2.html")

@app.route("/registarLinhaFatura2", methods=['GET', 'POST'])
def registarLinhaFatura2():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    
    qtd=int(request.form.get('qtd'))
        
    if qtd <= 0:
        flash('A QUANTIDADE DEVE SER MAIOR DO QUE ZERO','qtdMenorQzero')
        return redirect("/registarLinhaFatura2")

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()

        sql1 = "SELECT valor_venda FROM t_produto WHERE id_produto = %s;"
        cursor.execute(sql1, (session['id_produto'],))
        valor_unit_raw = cursor.fetchone()
        valor_unit = float(valor_unit_raw[0])
        
        valor_lf= qtd * valor_unit

        sql = "UPDATE t_linhafat SET qtd = %s, valor_linhaFat=%s WHERE id_linhaFat = %s;"
        cursor.execute(sql, (qtd, valor_lf, session['id_linhaFatura'],))
        conexao.commit()

        sql2 = "SELECT * FROM t_linhafat WHERE id_fatura=%s"
        cursor.execute(sql2,(session['id_fatura'],))
        session['produtosDaFatura']= cursor.fetchall()
        
        cursor.close()

    session.pop('id_produto', None)
    session.pop('id_linhaFatura', None)
    session.pop('descricaoItem', None)

    conexao.close()
    
    return render_template("registarLinhaFatura.html")

@app.route("/cancelarProduto", methods=['GET', 'POST'])
def cancelarProduto():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    id_linhaFat=request.form.get('lfParaCancelar')
    id_fatura=session['id_fatura']

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()

        sql1 = "DELETE FROM t_linhafat WHERE id_linhaFat = %s;"
        cursor.execute(sql1, (id_linhaFat,))
        conexao.commit()

        sql2 = "SELECT * FROM t_linhafat WHERE id_fatura=%s"
        cursor.execute(sql2,(id_fatura,))
        bdtLinhaFatura= cursor.fetchall()
        session['produtosDaFatura'] = bdtLinhaFatura

        cursor.close()
    
    conexao.close()
    
    return render_template("registarLinhaFatura.html")

@app.route("/cancelarFatura", methods=['GET', 'POST'])
def cancelarFatura():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    id_fatura=session['id_fatura']

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if conexao.is_connected():
        cursor = conexao.cursor()

        sql2 = "SELECT * FROM t_linhafat WHERE id_fatura=%s"
        cursor.execute(sql2,(id_fatura,))
        bdtLinhaFatura= cursor.fetchall()

        if bdtLinhaFatura and len(bdtLinhaFatura) > 0:
            for lf in bdtLinhaFatura:
                nlf=lf[0]
                sql1 = "DELETE FROM t_linhafat WHERE id_linhaFat = %s;"
                cursor.execute(sql1, (nlf,))
                conexao.commit()

        sql = "DELETE FROM t_fatura WHERE id_fatura = %s;"
        cursor.execute(sql, (id_fatura,))
        conexao.commit()
        cursor.close()

        session.pop('id_fatura', None)
        session.pop('id_produto', None)
        session.pop('id_linhaFatura', None)
        session.pop('produtosDaFatura', None)
        session.pop('valorFatura', None)
        session.pop('nif', None)
        session.pop('qtdItens', None)
        session.pop('valorCartao', None)
       
    conexao.close()
    
    return render_template("registarFatura.html")

@app.route("/finalizarFatura", methods=['GET','POST'])
def finalizarFatura():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
                     
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    cursor = conexao.cursor()

    sql = "SELECT sum(qtd) from t_linhafat where id_fatura=%s;"
    cursor.execute(sql, (session['id_fatura'],))
    qtd_total_itens = cursor.fetchone()
    session['qtdItens']=qtd_total_itens[0]
    
    sql1 = "SELECT sum(valor_linhaFat) from t_linhafat where id_fatura=%s;"
    cursor.execute(sql1, (session['id_fatura'],))
    valor_total_fatura = cursor.fetchone()[0]
    session['valorFatura'] = round(valor_total_fatura, 2)
    
    sql4 = "SELECT nif FROM t_fatura WHERE id_fatura = %s;"
    cursor.execute(sql4, (session['id_fatura'],))
    nif= cursor.fetchone()
    session['nif']=int(nif[0])

    if session['nif'] != 0:
        sql3 = "SELECT valorCartao from t_cartao where nif=%s and ativo='0';"
        cursor.execute(sql3, (session['nif'],))
        valorCartao = cursor.fetchone()
        session['valorCartao'] = valorCartao[0]
    else:
        session['valorCartao'] = '0'

    cursor.nextset()

    sql2 = "UPDATE t_fatura SET valor_fatura = %s WHERE id_fatura = %s;"
    cursor.execute(sql2, (session['valorFatura'], session['id_fatura'],))
    conexao.commit()
    
    cursor.close()
    conexao.close()
    
    return render_template("finalizarFatura.html")

@app.route("/utilizarValorCartao", methods=['GET','POST'])
def utilizarValorCartao():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    valorAutilizar=float(request.form.get('valorCartaoAutilizar'))
    session['valorUtilizado']=valorAutilizar
    valorFatura=float(session['valorFatura'])
    id_fatura=session['id_fatura']
    qtd_total_itens=session['qtdItens']
    nif=session['nif']
    valorCartao= session['valorCartao']
    
    if valorAutilizar>valorCartao:
        flash('VALOR SUPERIOR AO DISPONÍVEL!', 'valorCartaoInsuficiente')
        return render_template("finalizarFatura.html")

    novoValorFatura=valorFatura-valorAutilizar
    session['valorFatura']=novoValorFatura

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    cursor = conexao.cursor()
    
    sql = "UPDATE t_fatura SET valor_fatura = %s WHERE id_fatura = %s;"
    cursor.execute(sql, (novoValorFatura, id_fatura,))
    conexao.commit()

    sql1 = "UPDATE t_cartao SET valorCartao= valorCartao - %s WHERE nif = %s and ativo='0';"
    cursor.execute(sql1, (valorAutilizar, nif,))
    conexao.commit()

    sql2 = "SELECT valorCartao from t_cartao where nif=%s and ativo='0';"
    cursor.execute(sql2, (nif,))
    session['valorCartao'] = cursor.fetchone()[0]
    
    cursor.close()
    conexao.close()
    
    return render_template("finalizarFatura.html", qtd_total_itens=qtd_total_itens)

@app.route("/finalizarFatura2", methods=['GET','POST'])
def finalizarFatura2():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    
    valorFaturaFinal=session['valorFatura']
    produtosDaFatura= session['produtosDaFatura']

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    cursor = conexao.cursor()
    if valorFaturaFinal>10:

        valorCartao=int(valorFaturaFinal/10)
        sql = "UPDATE t_cartao SET valorCartao= valorCartao + %s WHERE nif = %s and ativo='0';"
        cursor.execute(sql, (valorCartao, session['nif'],))
        conexao.commit()
    
    for item in produtosDaFatura:
        qtd=item[3]
        id_produto=item[1]
        sql1= "UPDATE t_produto SET stock= stock - %s WHERE id_produto = %s;"
        cursor.execute(sql1, (qtd, id_produto,))
        conexao.commit()
    cursor.close() 

    session.pop('id_fatura', None)
    session.pop('produtosDaFatura', None)
    session.pop('valorFatura', None)
    session.pop('nif', None)
    session.pop('qtdItens', None)
    session.pop('valorCartao', None)
    session.pop('valorUtilizado', None)
           
    conexao.close()

    flash('FATURA FINALIZADA COM SUCESSO!','faturaFinalizadaComSucesso')  
    return render_template("registarFatura.html")

@app.route("/listarUsuarios")
def listarUsuarios():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    bdtLogin=[]
 
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "SELECT * FROM t_login;"
        cursor.execute(sql)
        bdtLogin=cursor.fetchall()

        cursor.close()
        conexao.close()
    
    return render_template("listarUsuarios.html", bdtLogin=bdtLogin)

@app.route("/desativarUsuario", methods=['GET','POST'])
def desativarUsuario():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    username = request.form.get('username')
    
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "UPDATE t_login SET ativo='1' WHERE username = %s;"
        cursor.execute(sql, (username,))
        conexao.commit()
        cursor.close()
        
    conexao.close()
    
    return redirect("/listarUsuarios")

@app.route("/ativarUsuario", methods=['GET','POST'])
def ativarUsuario():
    if verificar_autenticacao()==True:
        pass
    else:
        flash('USUARIO NAO AUTENTICADO. REALIZE SEU LOGIN.','usuarioNaoLogado')
        return redirect('/login')
    username = request.form.get('username')
    
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    if conexao.is_connected():
        cursor = conexao.cursor()
        sql = "UPDATE t_login SET ativo='0' WHERE username = %s;"
        cursor.execute(sql, (username,))
        conexao.commit()
        cursor.close()
        
    conexao.close()
    
    return redirect("/listarUsuarios")
    
#colocar o site no ar
if __name__=="__main__":
    app.run(debug=True)