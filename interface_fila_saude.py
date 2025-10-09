import os
import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": os.getenv("DB_PASSWORD"),
    "database": "fila_saude"
}

# ---------------- Banco ----------------


def conectar_banco():
    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        return conexao
    except mysql.connector.Error as e:
        messagebox.showerror(
            "Erro de conexão", f"Não foi possível conectar ao banco de dados:\n{e}")
        return None

# ---------------- Operações ----------------


def buscar_fila(conexao):
    cursor = conexao.cursor()
    query = """
    SELECT id, nome, idade, prioridade, status, chegada
    FROM pacientes
    WHERE status = 'aguardando'
    ORDER BY prioridade ASC, chegada ASC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


def inserir_paciente(conexao, nome, idade, prioridade,
                     tipo_atendimento=None):
    cursor = conexao.cursor()
    chegada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = """
    INSERT INTO pacientes (nome, idade, prioridade, status, chegada)
    VALUES (%s, %s, %s, 'aguardando', %s);
    """
    cursor.execute(query, (nome, idade, prioridade, chegada))
    conexao.commit()
    cursor.close()


def pegar_proximo(conexao):
    cursor = conexao.cursor()
    query = """
    SELECT id, nome FROM pacientes
    WHERE status = 'aguardando'
    ORDER BY prioridade ASC, chegada ASC
    LIMIT 1;
    """
    cursor.execute(query)
    paciente = cursor.fetchone()
    cursor.close()
    return paciente  # (id, nome) or None


def set_status(conexao, paciente_id, novo_status):
    cursor = conexao.cursor()
    update = "UPDATE pacientes SET status = %s WHERE id = %s;"
    cursor.execute(update, (novo_status, paciente_id))
    conexao.commit()
    cursor.close()

# ---------------- UI ----------------


class FilaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fila Inteligente - Postos de Saúde")
        self.geometry("800x450")
        self.resizable(True, True)

        self.conexao = conectar_banco()
        if not self.conexao:
            # encerra app se não conseguir conenctar
            self.destroy()
            return

        self._criar_widgets()
        self.atualizar_fila()

    def _criar_widgets(self):
        # Frame superior: botões
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=8)

        btn_add = tk.Button(top_frame, text="Adicionar Paciente",
                            command=self.ui_adicionar)
        btn_add.pack(side="left", padx=4)

        btn_chamar = tk.Button(top_frame, text="Chamar Próximo",
                               command=self.ui_chamar_proximo)
        btn_chamar.pack(side="left", padx=4)

        btn_finalizar = tk.Button(top_frame, text="Finalizar Atendimento (por ID)",
                                  command=self.ui_finalizar_por_id)
        btn_finalizar.pack(side="left", padx=4)

        btn_refresh = tk.Button(top_frame, text="Atualizar",
                                command=self.atualizar_fila)
        btn_refresh.pack(side="left", padx=4)

        # Frame central: Treeview da fila
        cols = ("id", "nome", "idade", "prioridade", "status", "chegada")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            # ajuste de largura inicial
            if c == "nome":
                self.tree.column(c, width=260)
            elif c == "chegada":
                self.tree.column(c, width=150)
            else:
                self.tree.column(c, width=90, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        # Double-click na linha abre opções (ex: finalizar)
        self.tree.bind("<Double-1>", self.on_double_click)

        # Status bar
        self.status_var = tk.StringVar(value="Conectado ao banco de dados.")
        status_bar = tk.Label(self, textvariable=self.status_var, anchor="w")
        status_bar.pack(fill="x", side="bottom")

    def atualizar_fila(self):
        if not self.conexao or not self.conexao.is_connected():
            self.conexao = conectar_banco()
            if not self.conexao:
                return

        rows = buscar_fila(self.conexao)
        # limpar tree
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            self.tree.insert("", "end", values=r)
        self.status_var.set(
            f"{len(rows)} pacientes aguardando. Última atualização: {datetime.now().strftime('%H:%M:%S')}")

    def ui_adicionar(self):
        # Simples diálogo para pedir dados
        nome = simpledialog.askstring("Nome", "Nome do paciente:", parent=self)
        if not nome:
            return
        try:
            idade = simpledialog.askinteger(
                "Idade", "Idade do paciente:", parent=self, minvalue=0, maxvalue=150)
            if idade is None:
                return
        except Exception:
            messagebox.showerror("Erro", "Entrada inválida.")
            return

        # Prioridade: 1 = maior prioridade
        try:
            prioridade = simpledialog.askinteger(
                "Prioridade", "Prioridade (1 = maior prioridade):", parent=self, minvalue=1, maxvalue=100)
            if prioridade is None:
                return
        except Exception:
            messagebox.showerror("Entrada inválida.")
            return

        try:
            inserir_paciente(self.conexao, nome.strip(),
                             int(idade), int(prioridade))
            messagebox.showinfo("Sucesso", f"Paciente {nome} adicionado.")
            self.atualizar_fila()
        except Exception as e:
            messagebox.showinfo("Erro", f"Erro ao inserir paciente: \n{e}")

    def ui_chamar_proximo(self):
        try:
            paciente = pegar_proximo(self.conexao)
            if not paciente:
                messagebox.showinfo(
                    "Fila vazia", "Nenhum paciente aguardando.")
                return

            pid, nome = paciente
            confirm = messagebox.askyesno(
                "Confirmar chamada", f"Chamar paciente ID {pid} - {nome} para atendimento?")
            if not confirm:
                return

            set_status(self.conexao, pid, "atendimento")
            messagebox.showinfo(
                "Chamando", f"Paciente {nome} (ID {pid}) chamado para atendimento.")
            self.atualizar_fila()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao chamar próximo:\n{e}")

    def ui_finalizar_por_id(self):
        try:
            paciente_id = simpledialog.askinteger(
                "Finalizar atendimento", "ID do paciente a finalizar:", parent=self, minvalue=1)
            if not paciente_id:
                return
            confirm = messagebox.askyesno(
                "Confirmar", f"Finalizar atendimento ID {paciente_id}?")
            if not confirm:
                return
            set_status(self.conexao, paciente_id, "finalizado")
            messagebox.showinfo(
                "Concluído", f"Atendimento do paciente ID {paciente_id} finalizado.")
            self.atualizar_fila()
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao finalizar atendimento:\n{e}")

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        values = self.tree.item(item, "values")
        pid = values[0]
        nome = values[1]
        # oferecer opções rápidas
        action = messagebox.askquestion(
            "Opção", f"O que deseja para ID {pid} - {nome}?\nSim = Chamar para atendimento / Não = Cancelar")
        if action == "yes":
            try:
                set_status(self.conexao, pid, "atendimento")
                messagebox.showinfo(
                    "Chamado", f"Paciente {nome} (ID {pid}) foi movido para atendimemto.;")
                self.atualizar_fila()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar status:\n{e}")

    def on_closing(self):
        if messagebox.askokcancel("Sair", "Deseja sair?"):
            try:
                if self.conexao and self.conexao.is_connected():
                    self.conexao.close()
            finally:
                self.destroy()


if __name__ == "__main__":
    app = FilaApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
