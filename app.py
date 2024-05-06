from flask import Flask, render_template, request,redirect
from pymongo import MongoClient
from werkzeug.security import check_password_hash
import os
app = Flask(__name__)


# class MyApp:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.setup_routes()
#         self.setup_db()
#
#     def setup_routes(self):
#         @self.app.route('/')
#         def index():
#             return render_template('login.html')
#
#         @self.app.route('/login', methods=['POST'])
#         def login():
#             email = request.form.get('email')
#             password = request.form.get('password')
#
#             # Verificar se o usuário existe no banco de dados
#             user_data = self.collection.find_one({'email': email})
#             if user_data:
#                 # Verificar se a senha fornecida corresponde à senha armazenada no banco de dados
#                 if check_password_hash(user_data['password'], password):
#                     return render_template('server.html')
#                 else:
#                     return "Senha incorreta. Por favor, tente novamente."
#             else:
#                 return "Usuário não encontrado. Por favor, registre-se primeiro."
#
#         @self.app.route('/signup')
#         def signup():
#             return render_template('signup.html')
#
#         @self.app.route('/register', methods=['POST'])
#         def register():
#             try:
#                 name = request.form['name']
#                 phone = request.form['phone']
#                 email = request.form['email']
#                 password = request.form['password']
#
#                 # Inserir dados do cliente no MongoDB Atlas
#                 cliente_data = {
#                     'name': name,
#                     'phone': phone,
#                     'email': email,
#                     'password': password
#                 }
#                 self.collection.insert_one(cliente_data)
#
#                 return "Cadastro realizado com sucesso!"
#             except Exception as e:
#                 return str(e)
#
#     def setup_db(self):
#         try:
#             self.cluster = MongoClient("mongodb+srv://tempotemporesto:uSkg5lY0Z1L442EY@test.ty5rffy.mongodb.net/test?retryWrites=true&w=majority")
#             self.db = self.cluster["python"]
#             self.collection = self.db["test"]
#             print("Conexão com o banco de dados estabelecida com sucesso!")
#         except Exception as e:
#             print(f"Erro ao conectar-se ao banco de dados: {e}")
#
#





try:
    # Conectar-se ao cluster MongoDB Atlas
    #cluster = MongoClient("mongodb+srv://tempotemporesto:uSkg5lY0Z1L442EY@test.ty5rffy.mongodb.net")
    cluster = MongoClient("mongodb+srv://tempotemporesto:uSkg5lY0Z1L442EY@test.ty5rffy.mongodb.net/test?retryWrites=true&w=majority")
    # Acessar o banco de dados e a coleção
    db = cluster["python"]
    collection = db["test"]
    print("Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar-se ao banco de dados: {e}")

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():

    #email = request.form.get('email')
    #password = request.form.get('password')

    # Verificar se o usuário existe no banco de dados
    #user_data = collection.find_one({'email': email})

    #user_dato = collection.find_one({'password': password})
    #if user_data:
        # Verificar se a senha fornecida corresponde à senha armazenada no banco de dados
        #if check_password_hash(user_dato['password'], password):
            return render_template('server.html')
            #return "Senha incorreta. Por favor, tente novamente."
            # return render_template('sever.html')
        #else:
            # render_template('signup.html')
            # return "Login realizado com sucesso!"
        #    return render_template('server.html')
    #else:
    #    return "Usuário não encontrado. Por favor, registre-se primeiro."




    #  username = request.form.get('email')
    #  password = request.form.get('password')
    #
    # #  Verificar se o usuário existe no banco de dados
    #  user_data = collection.find_one({'email': username})
    # #
    #  user_dato = collection.find_one({'password': password})
    #  if user_data:
    #
    #      # Verificar se a senha fornecida corresponde à senha armazenada no banco de dados
    #      if check_password_hash(user_data['password'], password):
    #          return "Senha incorreta. Por favor, tente novamente."
    #          #return render_template('sever.html')
    #      else:
    #          #render_template('signup.html')
    #          #return "Login realizado com sucesso!"
    #             return render_template('server.html')
    #     else:
    #             return "Usuário não encontrado. Por favor, registre-se primeiro."
    # #
    # # #Lógica de autenticação
    # #return "Login realizado com sucesso!"


@app.route('/signup')
def signup():
    return render_template('signup.html')

# @app.route('/index')
# def index():
#      return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        # Inserir dados do cliente no MongoDB Atlas
        cliente_data = {
            'name': name,
            'phone': phone,
            'email': email,
            'password': password
        }
        collection.insert_one(cliente_data)

        return "Cadastro realizado com sucesso!"
    except Exception as e:
        return str(e)



@app.route('/server')
def server():
     #name1 = request.form.get('name')
     return render_template('server.html')


@app.route('/fotos')
def fotos():
    def upload_profile_picture():
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            # Salve o arquivo onde desejar
            file.save('caminho/para/salvar/imagem.jpg')
            return 'Imagem de perfil atualizada com sucesso!'
        else:
            return 'Erro ao carregar a imagem.'
    return render_template('fotos.html')

@app.route('/Contatos')
def Contatos():
     return render_template('Contatos.html')



if __name__ == '__main__':
    app.run(debug=True)