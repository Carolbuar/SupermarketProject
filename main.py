from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
from flask_bcrypt import Bcrypt

app=Flask(__name__)
bcrypt = Bcrypt(app)


app.secret_key = 'caroline'

#route -> 
#funcao -> o que vc quer exibir naquela pagina
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

        if user and bcrypt.check_password_hash(user[1], password):
            session['usuario_autenticado'] = username
            return redirect("/homepage")
        else:
            flash ('DADOS INVÁLIDOS')
            return redirect("/login")
        
def verificar_autenticacao():
    if 'usuario_autenticado' not in session or not session['usuario_autenticado']:
        return redirect("/login")
    
@app.route('/logout')
def logout():
    session.pop('usuario_autenticado', None)
    return redirect("/login")

@app.route("/homepage")
def homepage():
    verificar_autenticacao()
    return render_template("homepage.html")

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

@app.route("/listarProdutosValidadeProxima")
def renderListarProdutosValidadeProxima():
    return render_template("listarProdutosValidade.html")

@app.route("/listarProdutosValidadeProxima", methods=['POST'])
def listarProdutosValidadeProxima():
    
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
    
@app.route("/consultarPontos", methods=['POST'])
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
            valor_total = pontos*1
            return render_template("mostrarPontos.html", bdtPontos=bdtPontos, valor_total=valor_total)
        else:
            flash('CARTÃO INEXISTENTE OU INATIVO','cartaoNaoExistente')

    conexao.close()
    return render_template("consultarPontos.html")

@app.route("/registarFatura")
def renderRegistarFatura():
    return render_template("registarFatura.html")

@app.route("/registarFatura", methods=['POST'])
def registarFatura():
    nif=request.form.get('nif')
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         
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

    sql1 = "SELECT id_fatura FROM t_fatura WHERE data= %s and nif=%s;"
    cursor.execute(sql1, (data_atual, nif,))
    id_fatura_raw = cursor.fetchone()
    id_fatura = id_fatura_raw[0]
    session['id_fatura']=id_fatura

    cursor.close()
    conexao.close()
    
    return redirect("/registarLinhaFatura")

@app.route("/registarLinhaFatura")
def renderRegistarLinhaFatura():
    return render_template("registarLinhaFatura.html")

@app.route("/registarLinhaFatura", methods=['GET', 'POST'])
def registarLinhaFatura():
    id_produto=request.form.get('id_produto')
    session['id_produto']=id_produto
    id_fatura=session['id_fatura']

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    cursor = conexao.cursor()
    sql = "SELECT descricao FROM t_produto WHERE id_produto = %s;"
    cursor.execute(sql, (id_produto,))
    descricao = cursor.fetchone()

    sql1 = "INSERT INTO t_linhaFat (id_produto, descricao, id_fatura) VALUES (%s, %s, %s);"
    val= (id_produto, descricao[0],id_fatura)
    cursor.execute(sql1, val)
    conexao.commit()

    sql2 = "SELECT * FROM t_linhaFat WHERE id_produto = %s and qtd is null LIMIT 1;"
    cursor.execute(sql2, (id_produto,))
    bdIdDescr = cursor.fetchall()
    id_linhaFatura= bdIdDescr[0][0]
    session['id_linhaFatura'] = id_linhaFatura

    cursor.close()

    conexao.close()
    
    return render_template("registarLinhaFatura2.html", bdIdDescr=bdIdDescr)

@app.route("/registarLinhaFatura2")
def renderRegistarLinhaFatura2():
    return render_template("registarLinhaFatura2.html")

@app.route("/registarLinhaFatura2", methods=['GET', 'POST'])
def registarLinhaFatura2():
    qtd=int(request.form.get('qtd'))
    id_produto=session['id_produto']
    id_linhaFat=session['id_linhaFatura']
    id_fatura=session['id_fatura']

    if qtd <= 0:
        flash('A QUANTIDADE DEVE SER MAIOR DO QUE ZERO','qtdMenorQzero')
        return redirect("/registarLinhaFatura2")

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    bdtLinhaFatura=[]
 
    if conexao.is_connected():
        cursor = conexao.cursor()

        sql1 = "SELECT valor_venda FROM t_produto WHERE id_produto = %s;"
        cursor.execute(sql1, (id_produto,))
        valor_unit_raw = cursor.fetchone()
        valor_unit = float(valor_unit_raw[0])
        
        valor_lf= qtd * valor_unit

        sql = "UPDATE t_linhaFat SET qtd = %s, valor_linhaFat=%s WHERE id_linhaFat = %s;"
        cursor.execute(sql, (qtd, valor_lf, id_linhaFat,))
        conexao.commit()

        sql2 = "SELECT * FROM t_linhaFat WHERE id_fatura=%s"
        cursor.execute(sql2,(id_fatura,))
        bdtLinhaFatura= cursor.fetchall()
        session['produtosDaFatura'] = bdtLinhaFatura

        cursor.close()
    
    conexao.close()
    
    return render_template("registarLinhaFatura.html", bdtLinhaFatura=bdtLinhaFatura)

@app.route("/finalizarFatura", methods=['GET','POST'])
def finalizarFatura():
    id_fatura=session['id_fatura']
                 
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )
 
    cursor = conexao.cursor()

    sql = "SELECT sum(qtd) from t_linhaFat where id_fatura=%s;"
    cursor.execute(sql, (id_fatura,))
    qtd_total_itens = cursor.fetchone()[0]
    session['qtdItens']=qtd_total_itens
    
    sql1 = "SELECT sum(valor_linhaFat) from t_linhaFat where id_fatura=%s;"
    cursor.execute(sql1, (id_fatura,))
    valor_total_itens = cursor.fetchone()[0]
    session['valorFatura']=valor_total_itens

    sql4 = "SELECT nif FROM t_fatura WHERE id_fatura = %s;"
    cursor.execute(sql4, (id_fatura,))
    nif_raw= cursor.fetchone()
    nif=nif_raw[0]
    session['nif']=nif

    sql3 = "SELECT * from t_cartao where nif=%s;"
    cursor.execute(sql3, (nif,))
    valorCartao = cursor.fetchone()[3]  

    sql2 = "UPDATE t_fatura SET valor_fatura = %s WHERE id_fatura = %s;"
    cursor.execute(sql2, (valor_total_itens, id_fatura,))
    conexao.commit()


    sql6 = "SELECT * from t_cartao where nif=%s;"
    cursor.execute(sql6, (nif,))
    valorAtual = cursor.fetchone()[3]
    

    cursor.close()
    conexao.close()
    
    return render_template("finalizarFatura.html", qtd_total_itens=qtd_total_itens, valor_total_itens=valor_total_itens, valorAtual=valorAtual)

@app.route("/utilizarValorCartao", methods=['GET','POST'])
def utilizarValorCartao():
    valorAutilizar=float(request.form.get('valorCartaoAutilizar'))
    valorFatura=float(session['valorFatura'])
    id_fatura=session['id_fatura']
    qtd_total_itens=session['qtdItens']
    nif=session['nif']

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

    sql1 = "UPDATE t_cartao SET valorCartao= valorCartao - %s WHERE nif = %s;"
    cursor.execute(sql1, (valorAutilizar, nif,))
    conexao.commit()

    sql2 = "SELECT valorCartao from t_cartao where nif=%s;"
    cursor.execute(sql2, (nif,))
    novoValorCartao = cursor.fetchone()[0]
    
    cursor.close()
    conexao.close()
    
    return render_template("finalizarFatura.html", valor_total_itens=novoValorFatura,qtd_total_itens=qtd_total_itens, valorAtual=novoValorCartao)

@app.route("/finalizarFatura2", methods=['GET','POST'])
def finalizarFatura2():
    valorFaturaFinal=session['valorFatura']
    nif=session['nif']

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='mercadona'
    )

    if valorFaturaFinal>10:

        valorCartao=int(valorFaturaFinal/10)

        cursor = conexao.cursor()
        sql = "UPDATE t_cartao SET valorCartao= valorCartao + %s WHERE nif = %s;"
        cursor.execute(sql, (valorCartao, nif,))
        conexao.commit()
        cursor.close()

    session.pop('id_fatura', None)
    session.pop('id_produto', None)
    session.pop('id_linhaFatura', None)
    session.pop('produtosDaFatura', None)
    session.pop('novoValorFatura', None)
    session.pop('valorFatura', None)
    session.pop('nif', None)
    session.pop('qtdItens', None)
    
    conexao.close()
    
    return redirect("/homepage")

#colocar o site no ar
if __name__=="__main__":
    app.run(debug=True)