# 🏥 Fila Saúde

Protótipo de **Fila Inteligente** para Postos de Saúde

---

## 📌 Descrição

Este projeto é um protótipo de sistema de **fila inteligente** para postos de saúde, desenvolvido em **Python** com banco de dados **MySQL**.

Funcionalidades principais:

* ➕ **Adicionar pacientes** com prioridade
* 📋 **Visualizar fila** ordenada por prioridade e hora de chegada
* 🔔 **Chamar próximo paciente**
* ✅ **Finalizar atendimentos**
* 🗂️ **Registrar histórico** de atendimentos
* 🖥️ **Interface gráfica** para interação mais intuitiva (Tkinter)

---

## 🛠️ Tecnologias

* **Python 3.x**
* **MySQL**
* Biblioteca: [`mysql-connector-python`](https://pypi.org/project/mysql-connector-python/)
* Biblioteca: **Tkinter** (interface gráfica)

---

## 🚀 Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/mateussxz/fila_saude
cd fila_saude
```

### 2. Instale as dependências

```bash
pip install mysql-connector-python
```

### 3. Configure a senha do MySQL

Defina a variável de ambiente **DB_PASSWORD**:

* **Windows PowerShell**

```powershell
$env:DB_PASSWORD="sua_senha"
```

* **Linux/Mac**

```bash
export DB_PASSWORD="sua_senha"
```

### 4. Execute o protótipo

* **Menu interativo (terminal):**

```bash
python app.py
```
* **Interface gráfica (Tkinter):**

```bash
python interface_fila_saude.py
```

## 🖥️ Interface Gráfica

A interface gráfica permite:

* Visualiza a fila em tempo real
* Adicionar pacientes via diálogo
* Chamar e finalizar atendimentos com botões
* Atualizar dinamicamente a lista de pacientes

💡 A interface utiliza o mesmo banco de dados e mantém as funcionalides do protótipo original.

---

## 🗄️ Estrutura do Banco de Dados

Tabela: **`pacientes`**

| Coluna       | Tipo     | Descrição                                      |
| ------------ | -------- | ---------------------------------------------- |
| `id`         | INT (AI) | Identificador único (auto incremento)          |
| `nome`       | VARCHAR  | Nome do paciente                               |
| `idade`      | INT      | Idade do paciente                              |
| `prioridade` | INT      | Menor valor = maior prioridade                 |
| `status`     | VARCHAR  | Ex.: `aguardando`, `atendimento`, `finalizado` |
| `chegada`    | DATETIME | Data e hora de chegada                         |

---

## ⚠️ Observações

* 🔑 A senha do banco **não está no código** → configurada via variável de ambiente.
* 💻 Projeto pronto para uso **local** ou como **demonstração de portfólio**.
* 🖥️ A iterface gráfica é opcional, mas recomendada para uma melhor experiência.
