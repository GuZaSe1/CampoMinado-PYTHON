import random

# Função para criar o tabuleiro com minas
def criar_tabuleiro(linhas, colunas, num_minas):
    tabuleiro = [[' ' for _ in range(colunas)] for _ in range(linhas)]
    minas = set()

    while len(minas) < num_minas:
        linha = random.randint(0, linhas - 1)
        coluna = random.randint(0, colunas - 1)
        minas.add((linha, coluna))

    for linha, coluna in minas:
        tabuleiro[linha][coluna] = 'M'

    return tabuleiro, minas

# Função para mostrar o tabuleiro ao jogador
def mostrar_tabuleiro(tabuleiro, revelado, bandeiras):
    linhas = len(tabuleiro)
    colunas = len(tabuleiro[0])

    print("\n   " + " ".join([str(i) for i in range(colunas)]))
    for i in range(linhas):
        linha_mostrar = []
        for j in range(colunas):
            if (i, j) in bandeiras:
                linha_mostrar.append('F')
            elif revelado[i][j]:
                linha_mostrar.append(tabuleiro[i][j])
            else:
                linha_mostrar.append('_')
        print(f"{i:2} " + " ".join(linha_mostrar))
    print()

# Contar minas adjacentes a uma célula
def contar_minas_adjacentes(tabuleiro, linha, coluna):
    linhas = len(tabuleiro)
    colunas = len(tabuleiro[0])
    contador = 0
    for l in range(max(0, linha - 1), min(linhas, linha + 2)):
        for c in range(max(0, coluna - 1), min(colunas, coluna + 2)):
            if tabuleiro[l][c] == 'M':
                contador += 1
    return contador

# Revelar uma célula e expandir se for vazia
def revelar(tabuleiro, revelado, linha, coluna):
    if revelado[linha][coluna]:
        return
    revelado[linha][coluna] = True
    if tabuleiro[linha][coluna] == ' ':
        contagem = contar_minas_adjacentes(tabuleiro, linha, coluna)
        tabuleiro[linha][coluna] = str(contagem) if contagem > 0 else ' '
        if contagem == 0:
            for l in range(max(0, linha - 1), min(len(tabuleiro), linha + 2)):
                for c in range(max(0, coluna - 1), min(len(tabuleiro[0]), coluna + 2)):
                    if (l, c) != (linha, coluna):
                        revelar(tabuleiro, revelado, l, c)

# Verifica se o jogador venceu
def venceu(tabuleiro, revelado):
    for i in range(len(tabuleiro)):
        for j in range(len(tabuleiro[0])):
            if tabuleiro[i][j] != 'M' and not revelado[i][j]:
                return False
    return True

# Função principal do jogo
def jogar():
    print("=== CAMPO MINADO ===")
    colunas = int(input("Digite o número de colunas (X): "))
    linhas = int(input("Digite o número de linhas (Y): "))
    num_minas = int(input("Digite o número de minas (N): "))

    tabuleiro, minas = criar_tabuleiro(linhas, colunas, num_minas)
    revelado = [[False for _ in range(colunas)] for _ in range(linhas)]
    bandeiras = set()

    while True:
        mostrar_tabuleiro(tabuleiro, revelado, bandeiras)

        acao = input("Digite sua ação (r para revelar, f para marcar/desmarcar bandeira): ").lower()
        try:
            linha = int(input("Linha: "))
            coluna = int(input("Coluna: "))
        except ValueError:
            print("Coordenadas inválidas. Tente novamente.")
            continue

        if not (0 <= linha < linhas and 0 <= coluna < colunas):
            print("Coordenadas fora do tabuleiro. Tente novamente.")
            continue

        if acao == 'f':
            if (linha, coluna) in bandeiras:
                bandeiras.remove((linha, coluna))
            else:
                bandeiras.add((linha, coluna))
        elif acao == 'r':
            if (linha, coluna) in bandeiras:
                print("Você marcou essa célula com uma bandeira. Remova-a antes de revelar.")
                continue
            if (linha, coluna) in minas:
                mostrar_tabuleiro(tabuleiro, [[True] * colunas for _ in range(linhas)], bandeiras)
                print("💥 BOOM! Você pisou em uma mina. Fim de jogo!")
                break
            revelar(tabuleiro, revelado, linha, coluna)
            if venceu(tabuleiro, revelado):
                mostrar_tabuleiro(tabuleiro, revelado, bandeiras)
                print("🎉 Parabéns! Você venceu o jogo!")
                break
        else:
            print("Ação inválida. Use 'r' para revelar ou 'f' para bandeira.")

# Inicia o jogo
if __name__ == "__main__":
    jogar()
