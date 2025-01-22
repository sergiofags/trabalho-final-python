from enum import Enum
from typing import List, Optional
from datetime import datetime

class Usuario:
    id_counter = 0
    
    def __init__(self, nome: str, email: str, senha: str, dataNasc: datetime, numeroTelefone: str, foto: str):
        self.id = Usuario.id_counter
        Usuario.id_counter += 1
        self.nome = nome
        self.email = email
        self.senha = senha
        self.dataNasc = dataNasc
        self.numeroTelefone = numeroTelefone
        self.foto = foto
        self.salvas: List['Sala'] = []

    def __str__(self):
        return f'{self.nome} ({self.email}) ({self.id})'

    def cadastrar_usuario(self, nome: str, email: str, senha: str) -> 'Usuario':
        return Usuario(nome, email, senha, datetime.now(), 0, "")

    @classmethod
    def login(cls, email: str, senha: str, usuarios: List['Usuario']) -> Optional['Usuario']:
        for usuario in usuarios:
            if usuario.email == email and usuario.senha == senha:
                return usuario
        return None

    def entrar_na_sala(self, sala: 'Sala') -> None:
        if any(usuario.id == self.id for usuario in sala.participantes):
            return
        else:
            sala.adicionar_participante(self)
            print(f"Você entrou na sala '{sala.nome}'.")

class Sala:
    id_counter = 0
    salas: List['Sala'] = []  # Lista de salas disponíveis no sistema (agora um atributo de classe)

    def __init__(self, nome: str, descricao: str, foto: str, horarioCorte: str, criador: Usuario):
        self.id = Sala.id_counter
        Sala.id_counter += 1
        self.nome = nome
        self.descricao = descricao
        self.foto = foto
        self.criador = criador
        self.horarioCorte = horarioCorte
        self.participantes: List[Usuario] = [criador]
        self.locais_embarque = []
        self.locais_desembarque = []

    def __str__(self):
        return f'Sala {self.nome} ({self.id}) - Criada por {self.criador.nome} ({self.criador.id})'

    def adicionar_participante(self, usuario: Usuario):
        self.participantes.append(usuario)

    def remover_participante(self, usuario: Usuario):
        if usuario in self.participantes:
            self.participantes.remove(usuario)

    def adicionar_embarque(self, usuario: Usuario, local: str):
        self.locais_embarque.append({"id": usuario.id, "usuario": usuario.nome, "local": local})

    def adicionar_desembarque(self, usuario: Usuario, local: str):
        self.locais_desembarque.append({"id": usuario.id, "usuario": usuario.nome, "local": local})

    def visualizar_locais(self):
        print(f'\nLocais registrados na sala "{self.nome}":')
        print("Embarques:")
        if self.locais_embarque:
            for embarque in self.locais_embarque:
                print(f'Usuário: {embarque["usuario"]}, Local: {embarque["local"]}')
        else:
            print("Nenhum local de embarque registrado.")
        
        print("\nDesembarques:")
        if self.locais_desembarque:
            for desembarque in self.locais_desembarque:
                print(f'Usuário: {desembarque["usuario"]}, Local: {desembarque["local"]}')
        else:
            print("Nenhum local de desembarque registrado.")

    def ver_participantes(self):
        for participante in self.participantes:
            print(participante)

    @staticmethod
    def criar_sala(nome: str, descricao: str, foto: str, horarioCorte: str, usuario_logado: Usuario) -> 'Sala':
        sala = Sala(nome, descricao, foto, horarioCorte, usuario_logado)  # Passando usuario_logado como criador
        Sala.salas.append(sala)  # Adicionando a sala à lista de salas
        usuario_logado.salvas.append(sala)
        return sala
    
    @staticmethod
    def ver_salas(usuario_logado: Optional[Usuario]) -> None:
        if usuario_logado:
            if not Sala.salas:  # Acessando o atributo de classe diretamente
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
            for i, sala in enumerate(Sala.salas, start=1):
                print(f"{i}. Id: {sala.id} Nome: {sala.nome} Horario de Corte: {sala.horarioCorte}, Criador: {sala.criador.nome}")
            print('')
            print('='*30)
            print('')
            return Sala.salas
        else:
            print('')
            print('='*30)
            print('Você precisa estar logado para visualizar as salas.')
            print('='*30)
            print('')
        
    def convidar_para_sala(self):
        print('')
        print('='*30)
        print(f"Link e código para convidar: {self.nome}_CONVIDAR")
        print('='*30)
        print('')
    

def menu():
    usuarios: List[Usuario] = []
    usuario_logado: Optional[Usuario] = None

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
            data_nasc = input("Data de Nascimento (formato: dd/mm/yyyy): ")
            numero_telefone = input("Número de Telefone: ")
            foto = input("Foto (link): ")
            
            data_nasc = datetime.strptime(data_nasc, "%d/%m/%Y")

            usuario = Usuario(nome, email, senha, data_nasc, numero_telefone, foto)
            usuarios.append(usuario)
            
            print('')
            print('='*34)
            print(f'Usuário {usuario.nome} cadastrado com sucesso!')
            print('='*34)
            print('')

        elif escolha == '2':
            print('')
            print('='*30)
            print("-> Ver Usuários")
            print('='*30)
            print('')
            if not usuarios:
                print("Nenhum usuário cadastrado.")
            else:
                for i, usuario in enumerate(usuarios, start=1):
                    print(f"{i}. Id: {usuario.id} Nome: {usuario.nome}, Email: {usuario.email}")
            print('='*30)
            print('')

        elif escolha == '3':
            print('')
            print('='*30)
            print("-> Login")
            print('='*30)
            print('')
            email = input("Email: ")
            senha = input("Senha: ")
            usuario_logado = Usuario.login(email, senha, usuarios)
            if usuario_logado:
                print(f'Bem-vindo(a), {usuario_logado.nome}!')
            else:
                print('Credenciais inválidas!')
            print('='*30)

        elif escolha == '4':
            print('')
            print('='*30)
            print("-> Criar Sala")
            print('='*30)
            print('')
            if usuario_logado:
                nome = input("Nome da sala: ")
                descricao = input("Descrição: ")
                foto = input("Foto (link): ")
                horarioCorte = input("Horário de corte (Formato: 00:00): ")
                
                sala = Sala.criar_sala(nome, descricao, foto, horarioCorte, usuario_logado)
                print(f'Sala "{nome}" criada com sucesso!')
            else:
                print('Você precisa estar logado para criar uma sala.')
            print('='*30)

        elif escolha == '5':
            print('')
            print('='*30)
            print("-> Ver salas")
            print('='*30)
            print('')
            salas = Sala.ver_salas(usuario_logado)
            if salas:
                print("\n1. Entrar na Sala")
                print("0. Sair")
                print('')
                sub_escolha = input("Escolha uma opção: ")

                if sub_escolha == '1':
                    print('')
                    nome_sala = input("Digite o nome da sala: ")
                    print('')
                    sala_encontrada = next((sala for sala in salas if sala.nome == nome_sala), None)
                    if sala_encontrada:
                        usuario_logado.entrar_na_sala(sala_encontrada)
                        print(f'Você entrou na sala "{sala_encontrada.nome}".')
                        while True:
                            print('')
                            print("1. Convidar para Sala")
                            print("2. Sair da Sala")
                            print("3. Deletar Sala")
                            print("4. Marcar Local de Embarque")
                            print("5. Marcar Local de Desembarque")
                            print("6. Mostrar Locais")
                            print("7. Mostrar Participantes")
                            print("0. Sair")
                            print('')
                            sub_sub_escolha = input("Escolha uma opção: ")

                            if sub_sub_escolha == '1':
                                sala_encontrada.convidar_para_sala()
                            elif sub_sub_escolha == '2':
                                sala_encontrada.remover_participante(usuario_logado)
                                break
                            elif sub_sub_escolha == '3':
                                salas.remove(sala_encontrada)
                                break
                            elif sub_sub_escolha == '4':
                                local = input("Digite o local de embarque: ")
                                sala_encontrada.adicionar_embarque(usuario_logado, local)
                            elif sub_sub_escolha == '5':
                                local = input("Digite o local de desembarque: ")
                                sala_encontrada.adicionar_desembarque(usuario_logado, local)
                            elif sub_sub_escolha == '6':
                                sala_encontrada.visualizar_locais()
                            elif sub_sub_escolha == '7':
                                sala_encontrada.ver_participantes()
                            elif sub_sub_escolha == '0':
                                break
                            else:
                                print("Opção inválida!")
                    else:
                        print("Sala não encontrada.")
                elif sub_escolha == '0':
                    continue
            else:
                print("Nenhuma sala disponível.")
            print('='*30)

        else:
            print('')
            print('='*30)
            print("Opção inválida!")
            print('='*30)
            print('')

if __name__ == "__main__":
    menu()
