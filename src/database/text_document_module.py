from src.database.database_module import DatabaseModule
import json
import os

class TextDocumentModule(DatabaseModule):
    def __init__(self, file_path):
        self.file_path = file_path

    def connect(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({"users": [], "teams": [], "schedules": []}, file)
        # checando se tem todas as chaves
        with open(self.file_path, 'r') as file:
            try:
                data = json.load(file)
                for entity in ["users", "teams", "schedules"]:
                    if entity not in data:
                        data[entity] = []
                self.save_data(data)
                
            except json.decoder.JSONDecodeError:
                print("\033[31m[ERRO]\033[0m Arquivo de banco de dados corrompido, resetando...")
                self.clear_data()
            
        print("\033[33m[INFO]\033[0m Conectado ao banco de dados de documentos de texto")
        return True
    
    def disconnect(self):
        print("\033[33m[INFO]\033[0m Desconectado do banco de dados de documentos de texto")

    def execute_query(self, query):
        data = self.fetch_data()
        
        if query['action'] == 'insert':
            entity = query['entity']
            data[entity].append(query['data'])
        elif query['action'] == 'delete':
            entity = query['entity']
            if entity in data:
                data[entity] = [item for item in data[entity] if not all(item[key] == value for key, value in query['criteria'].items())]
        elif query['action'] == 'update':
            entity = query['entity']
            if entity in data:
                for item in data[entity]:
                    if all(item[key] == value for key, value in query['criteria'].items()):
                        item.update(query['data'])
            
        self.save_data(data)

    def fetch_data(self, query=None):
        with open(self.file_path, 'r') as file:
            data = json.load(file)

        if query:
            entity = query['entity']
            if entity in data:
                return [item for item in data[entity] if all(item[key] == value for key, value in query['criteria'].items())]
            else:
                return []
        else:
            return data

    def save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def clear_data(self):
        with open(self.file_path, 'w') as file:
            json.dump({"users": [], "teams": [], "schedules": []}, file)

    def get_next_id(self, entity):
        data = self.fetch_data()
        if entity in data:
            return len(data[entity]) + 1
        else:
            return 1