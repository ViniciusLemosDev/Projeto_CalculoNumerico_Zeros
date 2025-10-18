# metodos_numericos.py

import math
import time
import sympy as sp
from tabulate import tabulate

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
    inicio = time.perf_counter()
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("A função deve ter sinais opostos em a e b.")
    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = f(c)
        if abs(fc) < tol or (b - a) / 2 < tol:
            fim = time.perf_counter()
            return c, i, fim - inicio, abs(fc)
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    fim = time.perf_counter()
    return c, max_iter, fim - inicio, abs(fc)


def falsa_posicao(f, a, b, tol=1e-6, max_iter=1000):
    inicio = time.perf_counter()
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("A função deve ter sinais opostos em a e b.")
    for i in range(1, max_iter + 1):
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        if abs(fc) < tol:
            fim = time.perf_counter()
            return c, i, fim - inicio, abs(fc)
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    fim = time.perf_counter()
    return c, max_iter, fim - inicio, abs(fc)


def newton_raphson(f, df, x0, tol=1e-6, max_iter=1000):
    inicio = time.perf_counter()
    x = x0
    for i in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            raise ZeroDivisionError("Derivada nula! Método não pode continuar.")
        x1 = x - fx / dfx
        if abs(fx) < tol:
            fim = time.perf_counter()
            return x1, i, fim - inicio, abs(fx)
        x = x1
    fim = time.perf_counter()
    return x, max_iter, fim - inicio, abs(f(x))


def secante(f, x0, x1, tol=1e-6, max_iter=1000):
    inicio = time.perf_counter()
    for i in range(1, max_iter + 1):
        f0, f1 = f(x0), f(x1)
        if (f1 - f0) == 0:
            raise ZeroDivisionError("Divisão por zero na secante.")
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        if abs(f(x2)) < tol:
            fim = time.perf_counter()
            return x2, i, fim - inicio, abs(f(x2))
        x0, x1 = x1, x2
    fim = time.perf_counter()
    return x2, max_iter, fim - inicio, abs(f(x2))

# -------------------------------------------------------
# FUNÇÃO DE COMPARAÇÃO MODIFICADA
# -------------------------------------------------------

def comparar_metodos(f, df=None, a=None, b=None, x0=None, x1=None, tol=1e-6, max_iter=1000):
    """
    Executa os métodos e RETORNA uma lista de dicionários com os resultados.
    """
    resultados = []
    headers = ["Método", "Raiz", "Iterações", "Tempo (ms)", "|f(raiz)|"]

    # Dicionário para armazenar os dados de cada método
    def formatar_resultado(metodo, raiz, it, tempo, erro):
        return {
            "Método": metodo,
            "Raiz": f"{raiz:.8f}",
            "Iterações": it,
            "Tempo (ms)": f"{tempo*1000:.4f}",
            "|f(raiz)|": f"{erro:.2e}"
        }

    # Bissecção
    try:
        raiz, it, tempo, erro = bisseccao(f, a, b, tol, max_iter)
        resultados.append(formatar_resultado("Bissecção", raiz, it, tempo, erro))
    except Exception as e:
        resultados.append({"Método": "Bissecção", "Raiz": str(e), "Iterações": "-", "Tempo (ms)": "-", "|f(raiz)|": "-"})

    # Falsa Posição
    try:
        raiz, it, tempo, erro = falsa_posicao(f, a, b, tol, max_iter)
        resultados.append(formatar_resultado("Falsa Posição", raiz, it, tempo, erro))
    except Exception as e:
        resultados.append({"Método": "Falsa Posição", "Raiz": str(e), "Iterações": "-", "Tempo (ms)": "-", "|f(raiz)|": "-"})

    # Newton-Raphson
    if df is not None and x0 is not None:
        try:
            raiz, it, tempo, erro = newton_raphson(f, df, x0, tol, max_iter)
            resultados.append(formatar_resultado("Newton-Raphson", raiz, it, tempo, erro))
        except Exception as e:
            resultados.append({"Método": "Newton-Raphson", "Raiz": str(e), "Iterações": "-", "Tempo (ms)": "-", "|f(raiz)|": "-"})
    else:
        resultados.append({"Método": "Newton-Raphson", "Raiz": "Não aplicável", "Iterações": "-", "Tempo (ms)": "-", "|f(raiz)|": "-"})

    # Secante
    if x0 is not None and x1 is not None:
        try:
            raiz, it, tempo, erro = secante(f, x0, x1, tol, max_iter)
            resultados.append(formatar_resultado("Secante", raiz, it, tempo, erro))
        except Exception as e:
            resultados.append({"Método": "Secante", "Raiz": str(e), "Iterações": "-", "Tempo (ms)": "-", "|f(raiz)|": "-"})
    else:
        resultados.append({"Método": "Secante", "Raiz": "Não aplicável", "Iterações": "-", "Tempo (ms)": "-", "|f(raiz)|": "-"})

    return resultados
