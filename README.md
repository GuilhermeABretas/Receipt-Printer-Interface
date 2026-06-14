# MarySmoke - Sistema de Recibos

Este é um sistema simples e moderno desenvolvido em Python com Tkinter para gerar e imprimir recibos em impressoras térmicas (58mm). O sistema foi feito sob medida para otimizar o fluxo de preenchimento e impressão rápida.

## 🚀 Como instalar e rodar (Primeira vez)

1. Faça o clone deste repositório ou baixe os arquivos para o seu computador:
   ```bash
   git clone https://github.com/GuilhermeABretas/Receipt-Printer-Interface.git
   ```

2. Você precisará ter o **Python** instalado na sua máquina. Se ainda não tiver, baixe e instale a versão mais recente em [python.org](https://www.python.org/).

3. Instale a biblioteca necessária abrindo o terminal (Prompt de Comando ou PowerShell) na pasta do projeto e rodando:
   ```bash
   pip install fpdf
   ```

## 🖥️ Como usar no dia a dia

Para facilitar o uso, preparamos um script que cria um atalho na sua Área de Trabalho. Assim, você não precisa ficar rodando comandos no terminal toda vez que quiser abrir o programa.

**Passos para criar o atalho:**
1. Abra a pasta do projeto (onde os arquivos foram baixados).
2. Dê um duplo clique no arquivo **`criar_atalho.bat`**.
3. O script vai rodar rapidamente e criar um atalho chamado **MarySmoke Recibos** na sua Área de Trabalho.
4. Agora é só abrir pelo atalho! A interface vai aparecer limpa, sem a janela preta do terminal no fundo.

**Nota sobre a Logo:** Certifique-se de que a imagem de logotipo do recibo (`logo.jpg` ou `logo.png`) está na mesma pasta do arquivo `interface.py`.

## 📦 Funcionalidades
- **Interface Minimalista e Plana (Flat Design):** Fundo cinza limpo, fontes padrão do sistema e espaçamento agradável.
- **Opções de Tabaco Predefinidas:** A lista suspensa do "Item" já conta com as opções rápidas de *Tabaco Trad.* e *Tabaco Mentol*, mas permite digitação livre.
- **Botões Inteligentes:** Opções de adicionar, remover itens que você se arrependeu, e limpar todo o pedido de um cliente com um clique.
- **Ajustes no PDF de 58mm:** A coluna de "Item" possui mais espaço para evitar quebra de linhas para produtos com nomes extensos.
