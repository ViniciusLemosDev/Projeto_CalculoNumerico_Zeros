# ⚡ CalculusFlow

**CalculusFlow** é uma aplicação interativa desenvolvida em **Python + Streamlit** para **comparar métodos numéricos de cálculo de zeros de funções**.  
O projeto foi criado para fins **educacionais** na disciplina de **Cálculo Numérico**, permitindo explorar visualmente a eficiência dos métodos **Bissecção**, **Falsa Posição**, **Newton-Raphson** e **Secante**.

---

## 🧩 Funcionalidades

- Interface web simples e interativa feita com **Streamlit**  
- Escolha entre **três problemas práticos**:
  - Potencial magnético (função polinomial)
  - Concentração de bactérias
  - Deslocamento de estruturas mecânicas  
- Comparação entre os **quatro métodos iterativos clássicos**
- Exibição de resultados em formato de **tabela dinâmica (Pandas DataFrame)**
- Análise textual automática explicando a **velocidade, robustez e custo computacional** de cada método

---

## 🧠 Metodologia

O aplicativo compara os seguintes métodos:

| Método           | Tipo de Método      | Características Principais |
|------------------|--------------------|-----------------------------|
| **Bissecção**     | Intervalar         | Robusto e garantido, mas lento |
| **Falsa Posição** | Intervalar         | Melhor aproximação que a Bissecção |
| **Newton-Raphson**| Ponto Fixo (com derivada) | Extremamente rápido, depende da derivada |
| **Secante**       | Ponto Fixo (sem derivada) | Boa alternativa ao Newton-Raphson |

---

## 🚀 Como Executar o Projeto

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/ViniciusLemosDev/Projeto_CalculoNumerico_Zeros.git
cd Projeto_CalculoNumerico_Zeros
python -m venv venv
```

### 2️⃣ (Opcional) Crie e Ative um Ambiente Virtual

```bash
venv\Scripts\activate   # no Windows
source venv/bin/activate  # no Linux/Mac
```

### 3️⃣ Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Execute o Aplicativo

```bash
streamlit run app.py
```

Acesse no navegador: http://localhost:8501

### 📂 Estrutura do Projeto

```bash
📁 Projeto_CalculoNumerico_Zeros
├── app.py                # Interface principal do Streamlit
├── metodos_numericos.py  # Implementação dos métodos numéricos
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo
```

### 📊 Tecnologias Utilizadas

* Python 3.11+

* Streamlit → Interface web interativa

* Sympy → Manipulação simbólica e cálculo de derivadas

* Pandas → Organização e exibição dos resultados

* Tabulate → Formatação dos dados numéricos (para testes de terminal)

### 👨‍💻 Autores

Nome	Função
-------------------------------------------------------------------------------
Vinicius Lemos de Carvalho	Desenvolvimento do app Streamlit e integração geral
Eduardo Medeiros Magalhães	Implementação e testes dos métodos numéricos
Maksimo	Documentação, revisão e análise teórica dos métodos

### 📘 Licença

Este projeto foi desenvolvido apenas para fins educacionais.
Sinta-se livre para clonar, estudar e modificar o código para aprendizado.

### 🧩 Exemplo de Uso

1. Escolha um dos problemas no painel lateral.

2. Defina o intervalo [a, b] e os valores iniciais x₀, x₁.

3. Ajuste a tolerância e o número máximo de iterações.

4. Clique em "🚀 Comparar Métodos" para ver o desempenho de cada algoritmo.
