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

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>APP JOAO</title>
        <style>
            body {
                background-color: #000;
                color: #FFA500;
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }

            .container {
                max-width: 400px;
                width: 100%;
                margin: auto;
                padding: 20px;
                box-sizing: border-box;
                text-align: center;
                border: 2px solid #FFF; /* Adicionando a borda branca */
                border-radius: 10px; /* Bordas arredondadas */
            }

            label {
                display: block;
                margin-bottom: 10px;
                text-align: left;
            }

            select, input {
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                border: 2px solid #FFA500;
                border-radius: 5px;
                background-color: #333;
                color: #FFA500;
                box-sizing: border-box;
            }

            button {
                width: 100%;
                padding: 10px;
                background-color: #FFA500;
                color: #000;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }

            .success-message {
                color: #00FF00;
                margin-top: 10px;
                display: inline-block; /* Para que o botão fique ao lado da mensagem */
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>APP JOAO MANUTENÇÃO 1.0V</h1>
            <form id="futuristic-form" method="post" onsubmit="enviarFormulario(event)">
                <label for="nomeOperador">Nome do Operador:</label>
                <select id="nomeOperador" name="nomeOperador">
                    <option value="Bruno">Bruno</option>
                    <option value="João">João</option>
                    <option value="Tiago">Tiago</option>
                </select>

                <label for="tipoMaquina">Tipo de Máquina:</label>
                <select id="tipoMaquina" name="tipoMaquina">
                    <option value="martelo">Martelo</option>
                    <option value="tesoura">Tesoura</option>
                    <option value="facao">Facão</option>
                </select>

                <label for="dataHoraParada">Data e Hora da Parada:</label>
                <input type="datetime-local" id="dataHoraParada" name="dataHoraParada" required>

                <label for="dataHoraConserto">Data e Hora do Conserto:</label>
                <input type="datetime-local" id="dataHoraConserto" name="dataHoraConserto" required>

                <label for="nomeMecanico">Nome do Mecânico:</label>
                <select id="nomeMecanico" name="nomeMecanico">
                    <option value="Tião">Tião</option>
                    <option value="Duda">Duda</option>
                </select>

                <button type="submit">Enviar</button>
                <p class="success-message" id="success-message"></p>
            </form>
        </div>

        <script>
            // Definir campos como vazios quando a página é carregada
            window.onload = function () {
                document.getElementById('nomeOperador').value = '';
                document.getElementById('tipoMaquina').value = '';
                document.getElementById('dataHoraParada').value = '';
                document.getElementById('dataHoraConserto').value = '';
                document.getElementById('nomeMecanico').value = '';
            };

            function enviarFormulario(event) {
                event.preventDefault(); // Evita o comportamento padrão do formulário

                // Lógica para enviar o formulário (pode ser ajustada conforme necessário)

                // Limpar os campos
                document.getElementById('nomeOperador').value = '';
                document.getElementById('tipoMaquina').value = '';
                document.getElementById('dataHoraParada').value = '';
                document.getElementById('dataHoraConserto').value = '';
                document.getElementById('nomeMecanico').value = '';

                // Exibir mensagem de sucesso
                var successMessage = document.getElementById('success-message');
                successMessage.innerText = 'Informações enviadas com sucesso!';

                // Esconder a mensagem após 5 segundos
                setTimeout(function () {
                    successMessage.innerText = '';
                }, 5000);
            }
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True)
