# Conecta Campus no PythonAnywhere

Esta pasta contém uma versão Flask/WSGI independente, preparada para o PythonAnywhere.

## 1. Enviar os arquivos

Envie o conteúdo desta pasta para:

```text
/home/SEU_USUARIO/conecta-campus
```

Você pode enviar o arquivo ZIP pela aba **Files** e descompactá-lo em um console Bash.

## 2. Criar o ambiente Python

Em um console Bash do PythonAnywhere:

```bash
mkvirtualenv --python=/usr/bin/python3.13 conecta-campus-venv
cd ~/conecta-campus
pip install -r requirements.txt
python manage_admin.py
```

O último comando solicitará o usuário e a senha do painel administrativo. A senha é armazenada apenas como hash.

## 3. Criar a aplicação web

Na aba **Web**:

1. escolha **Add a new web app**;
2. escolha **Manual configuration**;
3. selecione a mesma versão do Python usada no ambiente virtual;
4. no campo **Virtualenv**, informe `conecta-campus-venv`;
5. em **Source code** e **Working directory**, informe `/home/SEU_USUARIO/conecta-campus`.

## 4. Configurar o WSGI

Abra o arquivo WSGI indicado na aba Web, apague o conteúdo existente e cole o conteúdo de `pythonanywhere_wsgi.py`.

O arquivo usa `~/conecta-campus`, portanto não é necessário escrever o nome do usuário no código.

## 5. Configurar arquivos estáticos

Na seção **Static files** da aba Web, crie o mapeamento:

```text
URL:  /static/
Path: /home/SEU_USUARIO/conecta-campus/static
```

## 6. Publicar

Clique em **Reload** na aba Web e abra:

```text
https://SEU_USUARIO.pythonanywhere.com
```

O painel estará em `/admin`.

## Diagnóstico rápido

- `/health` deve responder `{"service":"conecta-campus","status":"ok"}`;
- erros de importação normalmente indicam caminho WSGI ou virtualenv incorretos;
- CSS ausente normalmente indica erro no mapeamento `/static/`;
- o banco SQLite é criado automaticamente em `instance/conecta_campus.db`.
