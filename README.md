<div align="center">

#### Redes sociais

[![linkedin](https://img.shields.io/badge/Linkedin-FFFFFF?style=flat&logo=linkedin&logoColor=blue)](https://www.linkedin.com/in/marcus-vinicius-de-miranda)
[![instagram](https://img.shields.io/badge/Instagram-FFFFFF?style=flat&logo=instagram&logoColor=orange)](https://www.instagram.com/marcusmiran/)

</div>

## Confitec - Teste Desenvolvedor Python

##### Primeiramente instalar as dependências:

```
pip install -r requirements.txt
```
<br>

##### Criar arquivo config.py de acordo com config.py.example

```python
# AWS
AWS_ACCESS_KEY_ID = 'your_access_key_aws'
AWS_SECRET_ACCESS_KEY = 'your_secret_key_aws'
REGION_NAME = 'default_region_name_aws'

# Genius
CLIENT_ID = 'client_id_for_genius_api' # not necessary
CLIENT_SECRET = 'client_secret_for_genius_api' # not necessary
CLIENT_ACCESS_TOKEN = 'client_access_token_for_genius_api'
```
<br>

##### Para iniciar a API, rodar no diretório do projeto o comando:

```
flask --app app run
```
<br>

##### Notas

O serviço Redis está configurado pra executar com as configurações padrões de instalação.

```python
import redis

# Using default config to create a connect
r = redis.Redis(host='localhost', port=6379, db=0)
```
<br>

##### Para executar os teste em 'tests/' basta executar o comando na pasta do projeto:

```
pytest tests
```
