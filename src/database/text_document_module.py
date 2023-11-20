from src.database.database_module import DatabaseModule
import json
import os

class TextDocumentModule(DatabaseModule):
    def __init__(self, file_path):
        self.file_path = file_path
        # printando em laranja para ter destaque no terminal
        print("\033[33m[INFO]\033[0m Usando módulo de documentos de texto")

        # Criar arquivo se não existir
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump([], file)

    def connect(self):
        # Não é necessário implementar para documentos de texto
        return True

    def disconnect(self):
        # Não é necessário implementar para documentos de texto
        return True

    def execute_query(self, query):
        data = self.fetch_data(None)
        
        if query['action'] == 'insert':
            data.append(query['data'])
        elif query['action'] == 'delete':
            data = [item for item in data if item['username'] != query['username']]
        self.save_data(data)

    def fetch_data(self, query):
        # Lógica para buscar dados de documentos de texto
        with open(self.file_path, 'r') as file:
            data = json.load(file)

        # Aplicar filtro se houver uma consulta
        if query:
            data = [item for item in data if all(item[key] == value for key, value in query.items())]

        return data

    def save_data(self, data):
        data = [dict(t) for t in {tuple(d.items()) for d in data}]
        print(data)
        # Lógica para salvar dados em documentos de texto
        with open(self.file_path, 'w') as file:
            json.dump(data, file)
        

    def clear_data(self):
        # Lógica para limpar todos os dados em documentos de texto
        with open(self.file_path, 'w') as file:
            json.dump([], file)            

