import sqlite3
import os

# adicionar consulta de fila, atualizacao para quem está em atendimento(status chamado) e quem finalizou, listar finalizados
class Connection:
    """
    Classe para gerenciar as conexões e realizar as operações com o banco de dados (sqlite)
    
    Argumentos:
        conexao(str): caminho para o banco de dados
    raises:
        FileNotFoundError: Caminho informado é invalido ou nao existe um baco sqlite no local
        
    """
    
    def __init__(self, conexao):
        """
        inicializa a conexão com o banco de dados sqlite

        argumentos:
            conexao(str): caminho para o banco de dados
        """
        
        # Verifica se o caminho existe
        if not os.path.exists(conexao):
            raise FileNotFoundError(f"Caminho invalido: não foi identificado um banco de dados sqlite em {conexao}")

        # cria a conexão
        self.conexao= sqlite3.connect(rf"{conexao}")
        # cria o cursor
        self.cursor = self.conexao.cursor()

    def fecha_conexao(self):
        """
        responsável por fechar a conexão com o banco
        """
        if self.conexao:
            # fecha a conexão
            print('fechando conexão')
            self.cursor.close()
            self.conexao.close()
    
    def consulta_senha(self):
        """
        consulta a ultima id no banco utilizando um sql buscando na tabela senhas (SELECT id FROM senhas ORDER BY id DESC LIMIT 1;)

        return:
            retorna um int referente a id identificada no banco de dados
        """
        try:
            # Executa o sql para consulta o id
            self.cursor.execute("SELECT id FROM senhas ORDER BY id DESC LIMIT 1;")
            # Salva o valor da consulta
            resultado = self.cursor.fetchone()
            ultimo_id = int(resultado[0]) if resultado else 0
            return ultimo_id
        except Exception as e:
            raise RuntimeError(f'Erro: {e} nao foi possivel realizar a consulta') from e

    def gera_senha(self, prioridade):
        """
        gera uma nova senha com base na ultima id identificada na tabela senha presente no banco de dados

        argumentos:
            prioridade(str, 'N' ou 'P'): define a prioridade de atenmento 'N' para normal e 'P' para preferecial

        raises:
            ValueError: retorna um erro caso o argumento para prioridade não seja 'P' ou 'N'

        return:
            retorna uma string com a senha gerada
        """

        # Verifica se o argumento para prioridade é valido
        if prioridade not in ("N", "P"):
            raise ValueError("O argumento deve ser 'N' para normal ou 'P' para prioridade.")

        # busca pela ultima senha
        ultimo_id = self.consulta_senha()
        # cria a nova senha (ultima id+1 e o tipo de prioridade)
        nova_senha = f"{prioridade}{int(ultimo_id)+ 1}"
        print(f'senha: {nova_senha}')

        # salva a senha criada
        self.salva_senha(prioridade)

        # retorna a senha
        return nova_senha

    def salva_senha(self, prioridade):
        """
        salva a nova senha no banco de dados sqlite (INSERT INTO senhas(prioridade, status) values ('{prioridade}', 'Aguardando');)

        argumentos:
            prioridade(str, 'N' ou 'P'): define a prioridade de atenmento 'N' para normal e 'P' para preferecial
        """
        
        if prioridade not in ("N", "P"):
            raise ValueError("O argumento deve ser 'N' para normal ou 'P' para prioridade.")
        
        try:
            self.cursor.execute(f"""
            INSERT INTO senhas(prioridade, status)
            values ('{prioridade}', 'Aguardando');
            """)
            # escreve a modificação
            self.conexao.commit()
        except Exception as e:
            raise RuntimeError(f'Erro: {e} nao foi possivel realizar a consulta') from e
        else:
            print("senha salva")
        finally:
            self.fecha_conexao()
    
    def altera_status_senha(self, id_senha):
        """
        funcao para alterar o status da senha na tabela ao finalizar o atendimento todas senhas sao salvas como 'finalizado'

        argumentos:
            id_senha(numerico): parte numerica da senha (desconsidere 'N' ou 'P'), utilizado para filtrar a linha na tabela

        """
        try:
            # comando sql para atualizar linha
            self.cursor.execute(f"""
                UPDATE senhas
                SET status = 'Finalizado',
                hora_fim = DATETIME('now', '-3 hours')
                WHERE id = {int(id_senha)}
                """)
            # escreve a modificação
            self.conexao.commit()
            print('Status atualizado com sucesso')
        except Exception as e:
            raise RuntimeError(f"Erro na atualização de status: erro -> {e}. \nNão foi possivel concluir o processo") from e
        finally:
            self.fecha_conexao()

    def consulta_ativos(self):
        """
        consulta a todos clientes ativo no banco utilizando um sql buscando na tabela senhas ("SELECT id, prioridade FROM senhas where status = 'Aguardando';")

        return:
            retorna uma lista com todos os clientes ativos
        """
        try:
            # Executa o sql para consulta
            self.cursor.execute("SELECT id, prioridade FROM senhas where status = 'Aguardando' order by id;")
            # Salva o valor da consulta
            resultado = self.cursor.fetchall()
            lista_senhas = []
            for senhas in resultado:
                lista_senhas.append(senhas[1] + str(senhas[0]))
            ultimo_id = resultado
            return lista_senhas
        except Exception as e:
            raise RuntimeError(f'Erro: {e} nao foi possivel realizar a consulta') from e
        finally:
            self.fecha_conexao()

    def chama_cliente(self):
        try:
            # Executa o sql para consulta
            self.cursor.execute("SELECT id, prioridade FROM senhas WHERE status = 'Atendimento' ORDER BY id LIMIT 1;")
            resultado = self.cursor.fetchone()
            if resultado == None:
                self.cursor.execute("SELECT id, prioridade FROM senhas WHERE status = 'Aguardando' ORDER BY id LIMIT 1;")
                # Salva o valor da consulta
                resultado = self.cursor.fetchone()
            senha_atual = (resultado[1] + str(resultado[0]))
            self.cursor.execute(f"UPDATE senhas SET status='Atendimento' WHERE id={resultado[0]}")
            self.conexao.commit()
            return senha_atual
        except Exception as e:
            raise RuntimeError(f'Erro: {e} nao foi possivel realizar a consulta') from e
        finally:
            self.fecha_conexao()
    
    def finaliza_atendimento(self, status):
        try:
            self.cursor.execute(f"UPDATE senhas SET status='{status}' WHERE status = 'Atendimento'")
            self.conexao.commit()
        except Exception as e:
            raise RuntimeError(f'Erro: {e} nao foi possivel realizar a consulta') from e
        finally:
            self.fecha_conexao()
