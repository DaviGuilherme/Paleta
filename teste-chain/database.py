import pymysql.cursors

class Database:
    def __init__(self):
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='paletaTeste123',
                password='paletaTeste123',
                database='paleta',
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def ler_perguntas(self, categoria):
        if self.connection:
            cursor = self.connection.cursor()
            sql = f"SELECT `pergunta` FROM `pergunta` INNER JOIN `questionario` ON `fk_pergunta` = `id_pergunta` INNER JOIN `categoria` ON `fk_categoria` = `id_categoria` AND LOWER(`nome`) LIKE LOWER('{categoria}')"
            cursor.execute(sql)
            result = cursor.fetchall()

            lista_perguntas = []
            for pergunta in result:
                lista_perguntas.append(pergunta['pergunta'])

            cursor.close()
            return lista_perguntas

    def recuperar_pedido(self, id_pedido):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                sql = f"SELECT `pergunta`, `resposta` FROM `pergunta` INNER JOIN `questionario` ON `fk_pergunta` = `id_pergunta` INNER JOIN `categoria` ON `fk_categoria` = `id_categoria` INNER JOIN `resposta` ON `id_questionario` = `fk_questionario` INNER JOIN `pedido` ON `id_pedido` = `fk_pedido` WHERE `id_pedido` = {id_pedido}"
                cursor.execute(sql)
                result = cursor.fetchall()

                cursor.close()
                return result
            except Exception as e:
                print(e)

    def salvar_respostas(self, dados):
        id_pedido = 0
        preco = 30.00
        if dados['resolucao'] == '1000x1000':
            preco = 25.00

        if self.connection:
            cursor = self.connection.cursor()
            try:
                command = f"INSERT INTO `pedido` (`titulo`, `resolucao`, `prazo`, `preco`, `data_inicio`, `data_fim`, `status`, `imagem`, `fk_categoria`, `fk_designer`, `fk_contratante`) VALUES ('{dados['titulo']}', '{dados['resolucao']}', '{dados['prazo']}', {preco}, NOW(), NOW(), 'Aguardando aprovação', NULL, (SELECT id_categoria FROM categoria WHERE nome LIKE '{dados['categoria']}'), {dados['idDesigner']}, {dados['idContratante']})"
                cursor.execute(command)
                self.connection.commit()
                id_pedido = cursor.lastrowid

                for cor in dados['cor']:
                    command = f"INSERT INTO `cor` (`cor`, `fk_pedido`) VALUES ('{cor}', {id_pedido})"
                    cursor.execute(command)
                    self.connection.commit()

                chaves_padrao = ['titulo', 'resolucao', 'prazo', 'categoria', 'idDesigner', 'idContratante', 'cor']
                dados_respostas = {chave: dados[chave] for chave in dados if chave not in chaves_padrao}

                for pergunta in dados_respostas.keys():
                    command = f"INSERT INTO `resposta` (`resposta`, `fk_pedido`, `fk_questionario`) VALUES ('{dados_respostas[pergunta]}', {id_pedido}, (SELECT id_questionario FROM questionario INNER JOIN pergunta ON fk_pergunta = id_pergunta WHERE pergunta = '{pergunta}' AND fk_categoria = (SELECT id_categoria FROM categoria WHERE nome LIKE '{dados['categoria']}')))"
                    cursor.execute(command)
                    self.connection.commit()
            except Exception as e:
                print(f"Erro ao salvar respostas: {e}")
            finally:
                cursor.close()

        return id_pedido