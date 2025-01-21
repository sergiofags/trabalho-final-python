from enum import Enum
from typing import List, Optional

class SalaStatus(Enum):
    ATIVA = 'Ativa'
    INATIVA = 'Inativa'

# Classes Principais
class Usuario:
    def __init__(self, nome: str, email: str, senha: str):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.salvas: List['Sala'] = []

    def __str__(self):
        return f'{self.nome} ({self.email})'

class Sala:
    def __init__(self, nome: str, descricao: str, foto: str, criador: Usuario):
        self.nome = nome
        self.descricao = descricao
        self.foto = foto
        self.criador = criador
        self.status = SalaStatus.ATIVA
        self.participantes: List[Usuario] = [criador]
        self.locais_embarque = []
        self.locais_desembarque = []

    def __str__(self):
        return f'Sala {self.nome} - Criada por {self.criador.nome}'

    def adicionar_embarque(self, usuario: Usuario, local: str):
        self.locais_embarque.append({"usuario": usuario.nome, "local": local})

    def adicionar_desembarque(self, usuario: Usuario, local: str):
        self.locais_desembarque.append({"usuario": usuario.nome, "local": local})

    def visualizar_locais(self):
        print('')
        print('='*30)
        print(f'\nLocais registrados na sala "{self.nome}":')
        print('='*30)
        print('')
        print("Embarques:")
        print('')
        if self.locais_embarque:
            for embarque in self.locais_embarque:
                print(f'Usuário: {embarque["usuario"]}, Local: {embarque["local"]}')
            print('')
        else:
            print('')
            print('='*30)
            print("Nenhum local de embarque registrado.")
            print('='*30)
            print('')
        print('='*30)
        print("\nDesembarques:")
        print('')
        if self.locais_desembarque:
            for desembarque in self.locais_desembarque:
                print(f'Usuário: {desembarque["usuario"]}, Local: {desembarque["local"]}')
            print('')
            print('='*30)
        else:
            print('')
            print('='*30)
            print("Nenhum local de desembarque registrado.")
            print('='*30)
            print('')

class Sistema:
    def __init__(self):
        self.usuarios: List[Usuario] = []
        self.salas: List[Sala] = []
        self.usuario_logado: Optional[Usuario] = None

    def cadastrar_usuario(self, nome: str, email: str, senha: str):
        usuario = Usuario(nome, email, senha)
        self.usuarios.append(usuario)
        print('')
        print('='*34)
        print(f'Usuário {usuario.nome} cadastrado com sucesso!')
        print('='*34)
        print('')
        

    def ver_usuarios(self):
        if not self.usuarios:
            print('')
            print('='*30)
            print("Nenhum usuário cadastrado.")
            print('='*30)
            print('')
        else:
            print('')
            print('='*30)
            print("Lista de usuários cadastrados:")
            print('='*30)
            print('')
            for i, usuario in enumerate(self.usuarios, start=1):
                print(f"{i}. Nome: {usuario.nome}, Email: {usuario.email}")
                print('') 
            print('='*30)
            print('')

    def login(self, email: str, senha: str):
        for usuario in self.usuarios:
            if usuario.email == email and usuario.senha == senha:
                self.usuario_logado = usuario
                print('')
                print('='*30)
                print(f'Bem-vindo(a), {usuario.nome}!')
                print('='*30)
                print('')
                return True
        print('')
        print('='*30)
        print('Credenciais inválidas!')
        print('='*30)
        print('')
        return False

    def criar_sala(self, nome: str, descricao: str, foto: str):
        if self.usuario_logado:
            sala = Sala(nome, descricao, foto, self.usuario_logado)
            self.salas.append(sala)
            self.usuario_logado.salvas.append(sala)
            print('')
            print('='*30)
            print(f'Sala "{nome}" criada com sucesso!')
            print('='*30)
            print('')
        else:
            print('')
            print('='*30)
            print('Você precisa estar logado para criar uma sala.')
            print('='*30)
            print('')

    def ver_salas(self):
        if self.usuario_logado:
            if not self.salas:
                print('')
                print('='*30)
                print("Nenhuma sala disponível.")
                print('='*30)
                print('')
                return None

            
            print('')
            print('='*30)
            print("\nLista de Salas:")
            print('='*30)
            print('')
            for i, sala in enumerate(self.salas, start=1):
                print(f"{i}. Nome: {sala.nome}, Criador: {sala.criador.nome}")
            print('')
            print('='*30)
            print('')
            return self.salas
        else:
            print('')
            print('='*30)
            print('Você precisa estar logado para visualizar as salas.')
            print('='*30)
            print('')

    def entrar_na_sala(self, nome_sala: str):
        for sala in self.salas:
            if sala.nome == nome_sala:
                sala.participantes.append(self.usuario_logado)
                print('')
                print('='*30)
                print(f'Você entrou na sala "{sala.nome}".')
                print('='*30)
                print('')
                return sala
            print('')
            print('='*30)
            print("Sala não encontrada.")
            print('='*30)
            print('')
        return None

    def convidar_para_sala(self, sala: Sala):
        print('')
        print('='*30)
        print(f"Link e código para convidar: {sala.nome}_CONVIDAR")
        print('='*30)
        print('')

    def sair_da_sala(self, sala: Sala):
        if sala and self.usuario_logado in sala.participantes:
            sala.participantes.remove(self.usuario_logado)  
            print('')
            print('='*30)
            print(f"Você saiu da sala '{sala.nome}'.")
            print('='*30)
            print('')
        else:
            print('')
            print('='*30)
            print("Você não está nesta sala.")
            print('='*30)
            print('')

    def deletar_sala(self, sala: Sala):
        if self.usuario_logado:
            self.salas.remove(sala)
            print('')
            print('='*30)
            print(f"Sala '{sala.nome}' deletada com sucesso!")
            print('='*30)
            print('')
        else:
            print('')
            print('='*30)
            print("Erro ao deletar a sala.")
            print('='*30)
            print('')

    def marcar_local_embarque(self, sala: Sala, local: str):
        if self.usuario_logado:
            sala.adicionar_embarque(self.usuario_logado, local)
            print('')
            print('='*30)
            print(f"Você marcou um local de embarque na sala '{sala.nome}'.")
            print('='*30)
            print('')
        else:
            print('')
            print('='*30)
            print("Você precisa estar logado para marcar um local de embarque.")
            print('='*30)
            print('')

    def marcar_local_desembarque(self, sala: Sala, local: str):
        if self.usuario_logado:
            sala.adicionar_desembarque(self.usuario_logado, local) 
            print('')
            print('='*30)
            print(f"Você marcou um local de desembarque na sala '{sala.nome}'.")
            print('='*30)
            print('')
        else:
            print('')
            print('='*30)
            print("Você precisa estar logado para marcar um local de desembarque.")
            print('='*30)
            print('')

    def visualizar_todos_locais(self):
        if self.salas:
            for sala in self.salas:
                sala.visualizar_locais()
        else: 
            print('')
            print('='*30)
            print("Nenhuma sala cadastrada.")
            print('='*30)
            print('')

def menu(sistema):
    while True:
        print(('='*10),"Menu do Sistema: ",('='*10))
        print('')
        print("1. Cadastrar Usuário")
        print("2. Ver Usuários")
        print("3. Login")
        print("4. Criar Sala")
        print("5. Ver Salas")
        print('')
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            print('')
            print('='*30)
            print("-> Cadastrar Usuário")
            print('='*30)
            print('')
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            sistema.cadastrar_usuario(nome, email, senha)

        elif escolha == '2':
            print('')
            print('='*30)
            print("-> Ver Usuários")
            print('='*30)
            print('')
            sistema.ver_usuarios()

        elif escolha == '3':
            print('')
            print('='*30)
            print("-> Login")
            print('='*30)
            print('')
            email = input("Email: ")
            senha = input("Senha: ")
            sistema.login(email, senha)

        elif escolha == '4':
            print('')
            print('='*30)
            print("-> Criar sala")
            print('='*30)
            print('')
            if sistema.usuario_logado:
                nome = input("Nome da sala: ")
                descricao = input("Descrição: ")
                foto = input("Foto (link): ")
                sistema.criar_sala(nome, descricao, foto)
            else: 
                print('')
                print('='*30)
                print('Você precisa estar logado para criar uma sala.')
                print('='*30)
                print('')

        elif escolha == '5':
            print('')
            print('='*30)
            print("-> Ver salas")
            print('='*30)
            print('')
            salas = sistema.ver_salas()
            if salas:
                print("\n1. Entrar na Sala")
                print("0. Sair")
                print('')
                sub_escolha = input("Escolha uma opção: ")
                print('')

                if sub_escolha == '1':
                    print('')
                    nome_sala = input("Digite o nome da sala: ")
                    print('')
                    sala = sistema.entrar_na_sala(nome_sala)
                    if sala:
                        while True:
                            print('')
                            print("1. Convidar para Sala")
                            print("2. Sair da Sala")
                            print("3. Deletar Sala")
                            print("4. Marcar Local de Embarque")
                            print("5. Marcar Local de Desembarque")
                            print("6. Mostrar Locais")
                            print("0. Sair")
                            print('')
                            sub_sub_escolha = input("Escolha uma opção: ")

                            if sub_sub_escolha == '1':
                                sistema.convidar_para_sala(sala)
                            elif sub_sub_escolha == '2':
                                sistema.sair_da_sala(sala)
                                break
                            elif sub_sub_escolha == '3':
                                sistema.deletar_sala(sala)
                                break
                            elif sub_sub_escolha == '4':
                                print('')
                                local = input("Digite o local de embarque: ")
                                print('')
                                sistema.marcar_local_embarque(sala, local)
                            elif sub_sub_escolha == '5':
                                print('')
                                local = input("Digite o local de desembarque: ")
                                print('')
                                sistema.marcar_local_desembarque(sala, local)
                            elif sub_sub_escolha == '6':
                                sistema.visualizar_todos_locais()
                            elif sub_sub_escolha == '0':
                                break
                            else:
                                print("Opção inválida!")
                elif sub_escolha == '0':
                    continue

        else:
            print('')
            print('='*30)
            print("Opção inválida!")
            print('='*30)
            print('')

if __name__ == "__main__":
    sistema = Sistema()
    menu(sistema)
