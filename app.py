import mysql.connector
from datetime import datetime
import os

# ---------------- Conexão com o MySQL ----------------


def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=os.getenv("DB_PASSWORD"),
            database="fila_saude"
        )
        print("Conexão bem-sucedida ao banco de dados!")
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar: {erro}")
        return None

# ---------------- Funções da fila ----------------


def mostrar_fila(conexao):
    cursor = conexao.cursor()
    query = """
    SELECT id, nome, idade, prioridade, status, chegada
    FROM pacientes
    WHERE status = 'aguardando'
    ORDER BY prioridade ASC, chegada ASC;
    """
    cursor.execute(query)
    pacientes = cursor.fetchall()

    print("\n-- Fila de Pacientes ---")
    if pacientes:
        for p in pacientes:
            print(
                f"ID: {p[0]}, Nome: {p[1]}, Idade: {p[2]}, Prioridade:{p[3]}, Status:{p[4]}, Chegada:{p[5]}")
    else:
        print("Fila vazia!")
        cursor.close()


def adicionar_paciente(conexao, nome, idade, prioridade):
    cursor = conexao.cursor()
    chegada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
    INSERT INTO pacientes (nome, idade, prioridade, status, chegada)
    VALUES (%s, %s, %s, 'aguardando', %s);
    """
    cursor.execute(query, (nome, idade, prioridade, chegada))
    conexao.commit()
    print(f"Paciente {nome} adicionado à fila.")
    cursor.close()


def chamar_proximo(conexao):
    cursor = conexao.cursor()
    # pega o próximo paciente aguardando, ordenado por prioridade e chegada
    query = """
    SELECT id, nome FROM pacientes
    WHERE status = 'aguardando'
    ORDER BY prioridade ASC, chegada ASC
    LIMIT 1;
    """

    cursor.execute(query)
    paciente = cursor.fetchone()
    if paciente:
        paciente_id, nome = paciente
        # atualiza status em atendimento
        update = "UPDATE pacientes SET status = 'atendimento' WHERE id = %s;"
        cursor.execute(update, (paciente_id,))
        conexao.commit()
        print(
            f"Chamando paciente ID {paciente_id}, Nome: {nome} para atendimento.")
    else:
        print("Nenhum paciente aguardando na fila.")
    cursor.close()


def finalizar_atendimento(conexao, paciente_id):
    cursor = conexao.cursor()
    update = "UPDATE pacientes SET status = 'finalizado' WHERE id = %s;"
    cursor.execute(update, (paciente_id,))
    conexao.commit()
    print(f"Atendimento do paciente ID {paciente_id} finalizado.")
    cursor.close()

# ---------------- Menu interativo ----------------


def menu():
    conexao = conectar_banco()
    if not conexao:
        return

    while True:
        print("\n--- Menu Fila Saúde ---")
        print("1. Mostrar fila")
        print("2. Adicionar paciente")
        print("3. Chamar próximo paciente")
        print("4. Finalizar atendimento")
        print("5. Sair")
        escolha = input("Escolha uma opção:")

        if escolha == "1":
            mostrar_fila(conexao)
        elif escolha == "2":
            nome = input("Nome do paciente:")
            idade = int(input("Idade do paciente:"))
            prioridade = int(input("Prioridade (1 = maior prioridade): "))
            adicionar_paciente(conexao, nome, idade, prioridade)
        elif escolha == "3":
            chamar_proximo(conexao)
        elif escolha == "4":
            paciente_id = int(input("ID do paciente a finalizar:"))
            finalizar_atendimento(conexao, paciente_id)
        elif escolha == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

    conexao.close()


# ---------------- Execução ----------------
if __name__ == "__main__":
    menu()
