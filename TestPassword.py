import bcrypt

senha = "senha123"  # A senha que você quer criptografar
hash_gerado = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
print(hash_gerado.decode('utf-8'))  # Imprime o hash gerado
