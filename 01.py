# pesquisa por usuário
# pesquisa por status
# pesquisa por prioridade
#
# chamados urgentes (criticos e abertos)
# abrir chamando (cadastrar novo chamado)
# resolver chamado (mudar status do chamado para progresso)
# fechar chamado (mudar status do chamado para fechado)
import sqlite3

def conexao_banco():
  conexao = sqlite3.connect('chamados.db')
  cursor = conexao.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS chamados (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      titulo TEXT,
      prioridade TEXT,
      status TEXT,
      usuario TEXT
    )
  ''')
  conexao.commit()
  return conexao

def escolha():
  while True:
    print ('1 - Pesquisa por Usuario')
    print ('2 - Pesquisa por status')
    print ('3 - Pesquisa por prioridade')
    print ('4 - Modificar Chamados')
    print ('5 - Adicionar chamado')

    opcoes = input ('Escolha: ')

    if opcoes == '1':
      user()

    if opcoes == '2':
      status()

    if opcoes == '3':
      prioritarios()

    if opcoes == '4':
      mod()

    if opcoes == '5':
      add()

def user():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    usuario = input('Digite o nome do usuário: ')
    cursor.execute('SELECT * FROM chamados WHERE usuario = ?', (usuario,))
    resultados = cursor.fetchall()
    if resultados:
        for chamado in resultados:
            print(chamado)
    else:
        print('Nenhum chamado encontrado para o usuário:', usuario)

    return escolha()

def status():
    conexao = conexao_banco()
    cursor = conexao.cursor()

    status = input('Digite o status do chamado (Aberto, Em progresso, Fechado): ')
    cursor.execute('SELECT * FROM chamados WHERE status = ?', (status,))
    resultados = cursor.fetchall()
    if resultados:
        for chamado in resultados:
            print(chamado)
    else:
        print('Nenhum chamado encontrado com o status:', status)

def add():
  while True:
    adicionar = input('Deseja adicionar um chamado? ').lower()
    if adicionar == 'nao':
      return escolha()

    elif adicionar == 'sim':
      titulo = input('Digite o título do chamado: ')
      prioridade = input('Digite a prioridade do chamado (Baixa, Média, Alta, Crítica): ')
      status = input('Digite o status do chamado (Aberto, Em progresso, Fechado): ')
      usuario = input('Digite o nome do usuário: ')

      conexao = conexao_banco()
      cursor = conexao.cursor()
      sql = '''
      INSERT INTO chamados (titulo, prioridade, status, usuario)
      VALUES (?, ?, ?, ?)'''

      cursor.execute(sql, (titulo, prioridade, status, usuario))
      conexao.commit()

def prioritarios():
  while True:
    print ('1- Chamados de Baixa prioridade')
    print ('2 - Média')
    print ('3 - Alta')
    print ('4 - Críticos')
    print ('5 - Todos')
    print ('0 - Voltar')

    conexao = conexao_banco()
    cursor = conexao.cursor()
    prioridade = input('Escolha a prioridade: ')

    sql = 'SELECT * FROM chamados WHERE prioridade LIKE ?'
    cursor.execute(sql, (f'%{prioridade}%',))
    resultados = cursor.fetchall()
    
    if resultados:
        for chamado in resultados:
            print(chamado)
    else:
        print('Nenhum chamado encontrado com a prioridade:', prioridade)
    
    return escolha()

def mod():
  conexao = conexao_banco()
  cursor = conexao.cursor()
  id_chamado = input('Digite o ID do chamado que deseja modificar: ')
  cursor.execute('SELECT * FROM chamados WHERE id = ?', (id_chamado,))
  resultado = cursor.fetchone()
  if resultado:
      print('Chamado encontrado:', resultado)
      novo_status = input('Digite o novo status do chamado (Aberto, Em progresso, Fechado): ')
      cursor.execute('UPDATE chamados SET status = ? WHERE id = ?', (novo_status, id_chamado))
      conexao.commit()
      print('Status do chamado atualizado com sucesso.')
  else:
      print('Nenhum chamado encontrado com o ID:', id_chamado)

menu = escolha()