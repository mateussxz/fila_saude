# Fila Saúde - Protótipo de Fila Inteligente para Postos de Saúde

## Descrição
Protótipo de sistema de **fila inteligente** para postos de saúde, desenvolvido em **Python** com banco de dados **MySQL**.
Permite:
- Adicionar pacientes com prioridade
- Visualizar fila ordenada por prioridade e hora de chegada
- Chamar próximo paciente
- Finalizar atendimentos
- Registrar histórico de atendimentos

--- 

## Tecnologias 
- Python 3.x
- MySQL
- Biblioteca `mysql-connector-python`

---

## Como usar

1. **Clone o repositório**
```bash
git clone https://github.com/mateussxz/fila_saude
cd fila_saude
```
2. Instale a biblioteca
```bash
pip install mysql-connector-python
```
3. Defina a variável de ambiente com a senha do MySQL
. Windows PowerShell:
```powershell
$env:DB_PASSWORD="sua_senha"
```
. Linux/Mac:
```bash
export DB_PASSWORD="sua_senha"
```
4. Rode o script
```bash
python app.py
```
5. Siga o meu interativo para gerenciar a fila.

Estrutura do banco
Tabela "pacientes" com colunas:
. id (INT, auto incremento)
. nome (VARCHAR)
. idade (INT)
. prioridade (INT, menor valor = maior prioridade)
. status (VARCHAR, exemplos: "aguardando", "atendimento", "finalizado")
. chegada (DATETIME)

Observações
. Senha do banco não está no código; usa variável de ambiente
. Projeto pronto para uso local ou demonstração de portfólio.
