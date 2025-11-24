#!/usr/bin/env python3
"""
Script para gerar instaladores com a branch correta
Lê o arquivo .env e atualiza install.ps1, install.sh e instalacao.md
"""

import os
import re

def carregar_env():
    """Carrega variáveis do arquivo .env"""
    env_path = '.env'
    if not os.path.exists(env_path):
        env_path = '.env.example'
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if linha and not linha.startswith('#') and '=' in linha:
                chave, valor = linha.split('=', 1)
                if chave == 'CORAL_BRANCH':
                    return valor.strip()
    
    return 'main'  # padrão

def atualizar_install_ps1(branch):
    """Atualiza install.ps1 com a branch correta"""
    caminho = 'install.ps1'
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Substitui a branch nos comentários e URLs
    conteudo = re.sub(
        r'Coral_project/(main|dev)/install\.ps1',
        f'Coral_project/{branch}/install.ps1',
        conteudo
    )
    conteudo = re.sub(
        r'refs/heads/(main|dev)\.zip',
        f'refs/heads/{branch}.zip',
        conteudo
    )
    conteudo = re.sub(
        r'Coral_project-(main|dev)',
        f'Coral_project-{branch}',
        conteudo
    )
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"✓ {caminho} atualizado para branch '{branch}'")

def atualizar_install_sh(branch):
    """Atualiza install.sh com a branch correta"""
    caminho = 'install.sh'
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Substitui a branch nos comentários e URLs
    conteudo = re.sub(
        r'Coral_project/(main|dev)/install\.sh',
        f'Coral_project/{branch}/install.sh',
        conteudo
    )
    conteudo = re.sub(
        r'refs/heads/(main|dev)\.zip',
        f'refs/heads/{branch}.zip',
        conteudo
    )
    conteudo = re.sub(
        r'Coral_project-(main|dev)',
        f'Coral_project-{branch}',
        conteudo
    )
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"✓ {caminho} atualizado para branch '{branch}'")

def atualizar_instalacao_md(branch):
    """Atualiza docs/guias/instalacao.md com a branch correta"""
    caminho = 'docs/guias/instalacao.md'
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Substitui todas as referências à branch
    conteudo = re.sub(
        r'Coral_project/(main|dev)/(install|uninstall)\.(ps1|sh)',
        lambda m: f'Coral_project/{branch}/{m.group(2)}.{m.group(3)}',
        conteudo
    )
    
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"✓ {caminho} atualizado para branch '{branch}'")

def main():
    print("=== Gerador de Instaladores ===\n")
    
    branch = carregar_env()
    print(f"Branch configurada: {branch}\n")
    
    atualizar_install_ps1(branch)
    atualizar_install_sh(branch)
    atualizar_instalacao_md(branch)
    
    print(f"\n✓ Todos os instaladores atualizados para a branch '{branch}'")
    print(f"\nPara mudar a branch, edite o arquivo .env e execute este script novamente.")

if __name__ == '__main__':
    main()
