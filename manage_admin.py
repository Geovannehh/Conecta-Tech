"""Cria ou atualiza o acesso administrativo do Conecta Campus."""

from getpass import getpass

from werkzeug.security import generate_password_hash

from flask_app import app, get_db, init_db


def main() -> None:
    username = input("Usuário administrativo: ").strip()
    if len(username) < 3:
        raise SystemExit("O usuário precisa ter ao menos 3 caracteres.")
    password = getpass("Senha: ")
    confirmation = getpass("Repita a senha: ")
    if password != confirmation:
        raise SystemExit("As senhas não coincidem.")
    if len(password) < 10:
        raise SystemExit("Use uma senha com pelo menos 10 caracteres.")

    with app.app_context():
        init_db()
        db = get_db()
        db.execute(
            """
            INSERT INTO admins (username, password_hash)
            VALUES (?, ?)
            ON CONFLICT(username) DO UPDATE SET password_hash = excluded.password_hash
            """,
            (username, generate_password_hash(password)),
        )
        db.commit()
    print("Administrador criado/atualizado com sucesso.")


if __name__ == "__main__":
    main()
