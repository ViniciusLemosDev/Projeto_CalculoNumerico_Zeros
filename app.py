# app.py

import streamlit as st
import sympy as sp
import pandas as pd
from metodos_numericos import f_exemplo, f_bacterias, f_estrutura, comparar_metodos

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="CalculusFlow",
    page_icon="⚡",
    layout="wide"
)

# --- CABEÇALHO E INTRODUÇÃO ---
st.title("⚡ CalculusFlow")
st.subheader("Sua calculadora interativa para Zeros de Funções")
st.markdown("""
Bem-vindo ao **CalculusFlow**, o primeiro produto da nossa empresa fictícia de educação!

Esta ferramenta foi criada para o projeto de Cálculo Numérico e permite que você resolva equações
complexas e compare a eficiência de quatro métodos iterativos clássicos. Explore, aprenda e veja
o poder da matemática aplicada em ação!
""")
st.divider()

# --- BARRA LATERAL COM AS ENTRADAS DO USUÁRIO ---
with st.sidebar:
    st.header("⚙️ Painel de Controle")

    # Dicionário para mapear as escolhas do usuário às funções
    problemas_disponiveis = {
        "Exemplo: Potencial Magnético": f_exemplo,
        "Problema 1: Concentração de Bactérias": f_bacterias,
        "Problema 2: Deslocamento de Estruturas": f_estrutura
    }
    problema_selecionado = st.selectbox(
        "1. Escolha o problema a ser resolvido:",
        list(problemas_disponiveis.keys())
    )
    funcao_escolhida = problemas_disponiveis[problema_selecionado]

    st.subheader("2. Defina os Parâmetros")
    # Usando colunas para organizar os inputs
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("Início do Intervalo (a)", value=0.0, format="%.2f")
        x0 = st.number_input("Estimativa Inicial (x₀)", value=1.0, format="%.2f")

    with col2:
        b = st.number_input("Fim do Intervalo (b)", value=5.0, format="%.2f")
        x1 = st.number_input("Segunda Estimativa (x₁)", value=2.0, format="%.2f")

    st.subheader("3. Ajustes de Precisão")
    tol = st.number_input("Tolerância (ex: 1e-6)", value=1e-6, format="%e")
    max_iter = st.number_input("Máximo de Iterações", value=100, min_value=1, step=1)

    # Botão para executar o cálculo
    calcular = st.button("🚀 Comparar Métodos", use_container_width=True, type="primary")


# --- ÁREA PRINCIPAL PARA EXIBIR OS RESULTADOS ---
if calcular:
    st.header("📊 Resultados Comparativos")

    # Lógica para obter a derivada simbolicamente para Newton-Raphson
    df_simbolica = None
    if problema_selecionado == "Exemplo: Potencial Magnético":
        x = sp.symbols('x')
        df_simbolica = sp.lambdify(x, sp.diff(x**3 - 5*x**2 + 8*x - 4, x))
    elif problema_selecionado == "Problema 1: Concentração de Bactérias":
        t = sp.symbols('t')
        df_simbolica = sp.lambdify(t, sp.diff(80 * sp.exp(-2*t) + 20 * sp.exp(-0.1*t) - 10, t))
    elif problema_selecionado == "Problema 2: Deslocamento de Estruturas":
        t = sp.symbols('t')
        df_simbolica = sp.lambdify(t, sp.diff(10 * sp.exp(-0.5*t) * sp.cos(2*t) - 5, t))

    # Chama a função principal com todos os parâmetros
    with st.spinner('Calculando... os computadores estão a todo vapor!'):
        resultados = comparar_metodos(
            f=funcao_escolhida,
            df=df_simbolica,
            a=a, b=b,
            x0=x0, x1=x1,
            tol=tol,
            max_iter=max_iter
        )

    # Exibe os resultados em uma tabela bonita (DataFrame do Pandas)
    df_resultados = pd.DataFrame(resultados)
    st.dataframe(df_resultados, use_container_width=True)

    st.divider()

    # --- ANÁLISE EDUCACIONAL DOS RESULTADOS ---
    st.header("🧠 Análise dos Resultados")
    st.markdown("""
    A tabela acima mostra o desempenho de cada método. O que podemos aprender com isso?

    - **Velocidade de Convergência (Iterações):**
      - **Newton-Raphson** é geralmente o campeão em velocidade, convergindo com o menor número de iterações. Isso ocorre porque ele usa a informação da derivada (a inclinação da curva) para dar "saltos" mais inteligentes em direção à raiz.
      - A **Secante** é uma ótima alternativa quando a derivada é difícil de calcular, sendo quase tão rápida quanto Newton.
      - **Bissecção** e **Falsa Posição** são mais lentos e previsíveis, pois "prendem" a raiz em um intervalo que diminui a cada passo.

    - **Robustez (Confiança no Resultado):**
      - Os métodos de intervalo (**Bissecção** e **Falsa Posição**) são muito robustos. Se você fornecer um intervalo `[a, b]` onde a função muda de sinal, eles *garantem* que encontrarão uma raiz.
      - **Newton** e a **Secante** podem falhar (divergir) se a estimativa inicial for ruim ou se a função tiver um comportamento inadequado (como derivadas próximas de zero).

    - **Custo Computacional (Tempo):**
      - Embora o tempo de execução seja muito rápido para estas funções, em problemas de engenharia muito complexos, o custo de calcular a derivada para o método de Newton pode torná-lo mais "caro" que o método da Secante.

    **Conclusão:** Não existe um "método perfeito". A escolha depende do problema: se você precisa de garantia e robustez, use a Bissecção. Se precisa de velocidade máxima e pode calcular a derivada, Newton-Raphson é a escolha.
    """)

else:
    st.info("Ajuste os parâmetros na barra lateral à esquerda e clique em 'Comparar Métodos' para iniciar.")
