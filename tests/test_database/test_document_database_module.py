import unittest
import os
from src.database.text_document_module import TextDocumentModule

class TestTextDocumentModule(unittest.TestCase):
    def setUp(self):
        # Configurações para os testes
        self.file_path = "test_data.json"
        self.db_module = TextDocumentModule(self.file_path)

    def tearDown(self):
        # Limpar o arquivo de dados após o teste
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_fetch_data_empty(self):
        # Testa buscar dados de um arquivo vazio
        result = self.db_module.fetch_data({})
        self.assertEqual(result, [])

    def test_save_and_fetch_data(self):
        # Testa salvar e buscar dados
        initial_data = [{"name": "John", "age": 25}, {"name": "Alice", "age": 30}]
        
        # Salva dados iniciais
        self.db_module.save_data(initial_data)

        # Busca dados
        result = self.db_module.fetch_data({"name": "John"})

        # Verifica se os dados foram recuperados corretamente
        self.assertEqual(result, [{"name": "John", "age": 25}])

    def test_clear_data(self):
        # Testa limpar todos os dados
        initial_data = [{"name": "John", "age": 25}, {"name": "Alice", "age": 30}]
        
        # Salva dados iniciais
        self.db_module.save_data(initial_data)

        # Limpa dados
        self.db_module.clear_data()

        # Verifica se os dados foram removidos
        result = self.db_module.fetch_data({})
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
