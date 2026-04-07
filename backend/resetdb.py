from pathlib import Path
import os
import shutil
import socket
import subprocess
import sys

from app import app


def resolve_sqlite_db_path(database_uri):
    sqlite_prefix = 'sqlite:///'
    if not database_uri.startswith(sqlite_prefix):
        return None

    sqlite_path = database_uri[len(sqlite_prefix):]
    if not sqlite_path or sqlite_path == ':memory:':
        return None

    if sqlite_path.startswith('/'):
        return Path(sqlite_path)

    return Path(app.instance_path) / sqlite_path


def remove_sqlite_files(database_path):
    for suffix in ('', '-shm', '-wal'):
        candidate = Path(f'{database_path}{suffix}')
        if candidate.exists():
            candidate.unlink()


def run_flask_command(*args):
    subprocess.run([sys.executable, '-m', 'flask', *args], check=True, cwd=Path(__file__).resolve().parent)


def backend_server_running():
    port = int(os.getenv('BACKEND_PORT', '3001'))
    hosts = ['127.0.0.1']

    configured_host = os.getenv('BACKEND_HOST')
    if configured_host and configured_host not in {'0.0.0.0', '::'}:
        hosts.insert(0, configured_host)

    for host in hosts:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            if sock.connect_ex((host, port)) == 0:
                return port

    return None


def main():
    active_port = backend_server_running()
    if active_port is not None:
        raise SystemExit(
            f'Backend server is running on port {active_port}. '
            'Stop it before running resetdb so the Flask reloader does not recreate tables during migration.'
        )

    database_uri = app.config['SQLALCHEMY_DATABASE_URI']
    database_path = resolve_sqlite_db_path(database_uri)
    if database_path is not None:
        remove_sqlite_files(database_path.resolve())

    shutil.rmtree(Path(__file__).resolve().parent / 'migrations', ignore_errors=True)

    run_flask_command('db', 'init')
    run_flask_command('db', 'migrate')
    run_flask_command('db', 'upgrade')

    print('resetdb complete')


if __name__ == '__main__':
    main()