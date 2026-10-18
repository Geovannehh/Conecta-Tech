# Conecta Campus Tech — iniciar localmente

1. Extraia o ZIP.
2. Instale Python 3.10 ou mais recente.
3. No terminal, entre na pasta conecta-campus e execute:

   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   .venv\Scripts\python.exe flask_app.py

4. Abra http://127.0.0.1:5000 no navegador.

Em macOS/Linux, substitua .venv\Scripts\python.exe por .venv/bin/python.

O banco e a chave local serão criados na primeira execução. Para criar
um administrador, execute manage_admin.py com o mesmo Python do ambiente.

Esta versão inclui a paleta escura e a correção dos fundos brancos.
O progresso das missões permanece no navegador de cada pessoa; não está
incluído no ZIP. Veja docs/TRANSFORMACAO-TECH.md para recursos e limites.
O README.md apresenta as telas e instruções completas. O guia de publicação
no PythonAnywhere está em docs/PYTHONANYWHERE.md.
