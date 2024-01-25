from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'user': 'root',
    'password': 'B1dCBBa-2Bf4d5Bhhfe6AGaf1E24hCFA',
    'host': 'roundhouse.proxy.rlwy.net',
    'port': 19533,
    'database': 'railway'
}

# Função para verificar e criar a tabela se não existir
def verificar_e_criar_tabela():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Verificar se a tabela já existe
    cursor.execute("SHOW TABLES LIKE 'maquina_parada'")
    tabela_existe = cursor.fetchone()

    if not tabela_existe:
        # Se a tabela não existe, criá-la
        cursor.execute("""
            CREATE TABLE maquina_parada (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome_operador VARCHAR(255),
                tipo_maquina VARCHAR(255),
                data_hora_parada DATETIME,
                data_hora_conserto DATETIME,
                nome_mecanico VARCHAR(255)
            )
        """)

    connection.close()

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    # Verificar e criar a tabela antes de processar a requisição
    verificar_e_criar_tabela()

    if request.method == 'POST':
        # Coletando dados do formulário
        nome_operador = request.form['nomeOperador']
        tipo_maquina = request.form['tipoMaquina']
        data_hora_parada = request.form['dataHoraParada']
        data_hora_conserto = request.form['dataHoraConserto']
        nome_mecanico = request.form['nomeMecanico']

        # Conectando ao banco de dados
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Inserindo dados na tabela 'maquina_parada'
        sql = "INSERT INTO maquina_parada (nome_operador, tipo_maquina, data_hora_parada, data_hora_conserto, nome_mecanico) VALUES (%s, %s, %s, %s, %s)"
        val = (nome_operador, tipo_maquina, data_hora_parada, data_hora_conserto, nome_mecanico)
        cursor.execute(sql, val)

        # Commit e fechamento da conexão
        connection.commit()
        connection.close()

    return render_template('futuristic_form.html')

if __name__ == '__main__':
    app.run(debug=True)
