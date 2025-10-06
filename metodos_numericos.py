# =============================================
# SIMULADOR DE MÉTODOS ITERATIVOS PARA RAÍZES
# Bissecção | Falsa Posição | Newton-Raphson | Secante
# Autor: (adicione o nome da sua equipe)
# Disciplina: Cálculo Numérico — UNIVASF
# =============================================

import math           # Biblioteca matemática padrão (funções exp, cos, etc.)
import time           # Para medir o tempo de execução de cada método
import sympy as sp     # Biblioteca simbólica para derivar funções (usada no Newton-Raphson)
from tabulate import tabulate  # Biblioteca para formatar tabelas no terminal

# -------------------------------------------------------
# DEFINIÇÃO DAS FUNÇÕES DE TESTE
# -------------------------------------------------------

def f_exemplo(x):
    """
    Função do exemplo fornecido no enunciado:
    f(x) = x³ - 5x² + 8x - 4
    Representa o potencial magnético citado no texto.
    """
    return x**3 - 5*x**2 + 8*x - 4


def f_bacterias(t):
    """
    Problema 1: Concentração de bactérias.
    C = 80e^(-2t) + 20e^(-0.1t)
    Queremos encontrar t tal que C = 10.
    Logo: f(t) = 80e^(-2t) + 20e^(-0.1t) - 10 = 0
    """
    return 80 * math.exp(-2*t) + 20 * math.exp(-0.1*t) - 10


def f_estrutura(t):
    """
    Problema 2: Deslocamento da estrutura.
    y(t) = 10e^(-0.5t)cos(2t)
    Queremos quando y(t) = 5, ou seja:
    f(t) = 10e^(-0.5t)cos(2t) - 5 = 0
    """
    return 10 * math.exp(-0.5*t) * math.cos(2*t) - 5


# -------------------------------------------------------
# IMPLEMENTAÇÃO DOS MÉTODOS ITERATIVOS
# -------------------------------------------------------

def bisseccao(f, a, b, tol=1e-6, max_iter=1000):
    """
    Método da Bissecção:
    Divide o intervalo [a,b] pela metade até encontrar a raiz.
    Requer que f(a) e f(b) tenham sinais opostos.
    """
    inicio = time.perf_counter()  # Inicia a contagem de tempo
    fa, fb = f(a), f(b)

    # Verifica se há mudança de sinal no intervalo
    if fa * fb > 0:
        raise ValueError("A função deve ter sinais opostos em a e b.")

    # Loop principal de iterações
    for i in range(1, max_iter + 1):
        c = (a + b) / 2          # Ponto médio
        fc = f(c)
        # Critério de parada: erro menor que a tolerância
        if abs(fc) < tol or (b - a) / 2 < tol:
            fim = time.perf_counter()
            return c, i, fim - inicio, abs(fc)
        # Atualiza o intervalo conforme o sinal
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc

    fim = time.perf_counter()
    return c, max_iter, fim - inicio, abs(fc)


def falsa_posicao(f, a, b, tol=1e-6, max_iter=1000):
    """
    Método da Falsa Posição (Regula Falsi):
    Usa interpolação linear entre f(a) e f(b).
    Também requer sinais opostos no intervalo.
    """
    inicio = time.perf_counter()
    fa, fb = f(a), f(b)

    if fa * fb > 0:
        raise ValueError("A função deve ter sinais opostos em a e b.")

    for i in range(1, max_iter + 1):
        # Fórmula da Falsa Posição
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        # Verifica se atingiu a precisão desejada
        if abs(fc) < tol:
            fim = time.perf_counter()
            return c, i, fim - inicio, abs(fc)
        # Atualiza o intervalo
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc

    fim = time.perf_counter()
    return c, max_iter, fim - inicio, abs(fc)


def newton_raphson(f, df, x0, tol=1e-6, max_iter=1000):
    """
    Método de Newton-Raphson:
    Usa a derivada da função para obter aproximações sucessivas.
    f'(x) é fornecida como função separada.
    """
    inicio = time.perf_counter()
    x = x0

    for i in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            raise ZeroDivisionError("Derivada nula! Método não pode continuar.")
        x1 = x - fx / dfx   # Fórmula principal
        if abs(fx) < tol:
            fim = time.perf_counter()
            return x1, i, fim - inicio, abs(fx)
        x = x1

    fim = time.perf_counter()
    return x, max_iter, fim - inicio, abs(f(x))


def secante(f, x0, x1, tol=1e-6, max_iter=1000):
    """
    Método da Secante:
    Parecido com o Newton-Raphson, mas não usa derivada.
    Calcula uma derivada aproximada com dois pontos consecutivos.
    """
    inicio = time.perf_counter()

    for i in range(1, max_iter + 1):
        f0, f1 = f(x0), f(x1)
        if (f1 - f0) == 0:
            raise ZeroDivisionError("Divisão por zero na secante.")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        if abs(f(x2)) < tol:
            fim = time.perf_counter()
            return x2, i, fim - inicio, abs(f(x2))
        # Atualiza os pontos
        x0, x1 = x1, x2

    fim = time.perf_counter()
    return x2, max_iter, fim - inicio, abs(f(x2))


# -------------------------------------------------------
# FUNÇÃO DE COMPARAÇÃO ENTRE OS MÉTODOS
# -------------------------------------------------------

def comparar_metodos(f, df=None, a=None, b=None, x0=None, x1=None, tol=1e-6):
    """
    Executa todos os métodos disponíveis e mostra um comparativo.
    Coleta: raiz, número de iterações, tempo e erro final.
    """
    resultados = []

    # Tenta rodar o método da bissecção
    try:
        raiz, it, tempo, erro = bisseccao(f, a, b, tol)
        resultados.append(["Bissecção", raiz, it, tempo*1000, erro])
    except Exception as e:
        resultados.append(["Bissecção", str(e), "-", "-", "-"])

    # Tenta rodar o método da Falsa Posição
    try:
        raiz, it, tempo, erro = falsa_posicao(f, a, b, tol)
        resultados.append(["Falsa Posição", raiz, it, tempo*1000, erro])
    except Exception as e:
        resultados.append(["Falsa Posição", str(e), "-", "-", "-"])

    # Tenta rodar o método de Newton-Raphson (se houver derivada)
    if df is not None and x0 is not None:
        try:
            raiz, it, tempo, erro = newton_raphson(f, df, x0, tol)
            resultados.append(["Newton-Raphson", raiz, it, tempo*1000, erro])
        except Exception as e:
            resultados.append(["Newton-Raphson", str(e), "-", "-", "-"])
    else:
        resultados.append(["Newton-Raphson", "sem derivada", "-", "-", "-"])

    # Tenta rodar o método da Secante (se houver x0 e x1)
    if x0 is not None and x1 is not None:
        try:
            raiz, it, tempo, erro = secante(f, x0, x1, tol)
            resultados.append(["Secante", raiz, it, tempo*1000, erro])
        except Exception as e:
            resultados.append(["Secante", str(e), "-", "-", "-"])
    else:
        resultados.append(["Secante", "sem x0/x1", "-", "-", "-"])

    # Exibe a tabela final
    print(tabulate(resultados, headers=["Método", "Raiz", "Iterações", "Tempo (ms)", "|f(raiz)|"], tablefmt="fancy_grid"))


# -------------------------------------------------------
# PROGRAMA PRINCIPAL (TESTES)
# -------------------------------------------------------
if __name__ == "__main__":
    # ====== EXEMPLO 1 ======
    print("\n===== EXEMPLO: f(x) = x³ – 5x² + 8x – 4 =====")

    # Derivada simbólica da função usando SymPy
    x = sp.symbols('x')
    df_exemplo = sp.lambdify(x, sp.diff(x**3 - 5*x**2 + 8*x - 4, x))

    # Chama o comparador para todos os métodos
    comparar_metodos(f_exemplo, df_exemplo, a=0, b=5, x0=2.5, x1=3)

    # ====== PROBLEMA 1 ======
    print("\n===== PROBLEMA 1: Concentração de Bactérias =====")
    comparar_metodos(f_bacterias, a=0, b=10, x0=1, x1=2)

    # ====== PROBLEMA 2 ======
    print("\n===== PROBLEMA 2: Deslocamento da Estrutura =====")
    comparar_metodos(f_estrutura, a=0, b=5, x0=1, x1=2)
