
## Sobre o projeto

O **Politicagem** é um agregador de notícias que reúne em uma única página os principais despachos de veículos independentes, investigativos, progressistas e de esquerda do Brasil e América Latina. A interface imita a estética dos jornais impressos da década de 1930 — tipografia serifada, colunas, capitulares e papel envelhecido — como contraponto irônico à era da desinformação.

As notícias são buscadas em tempo real via **RSS**, sem armazenamento em banco de dados. Cada visita apresenta uma notícia principal selecionada aleatoriamente, e todas as matérias são ordenadas cronologicamente por horário de publicação.

---

## Funcionalidades


- Tema escuro monocromático
- Seleção aleatória da notícia principal da capa
- Ordenação cronológica por horário de publicação
- Busca por palavra-chave em tempo real
- Agregação via RSS de +40 fontes
- Múltiplos parágrafos por artigo (mínimo 4)
- Modo terminal (sem servidor web)
- Visualização completa de artigos via scraping
- Layout responsivo com 4 colunas para desktop
- Correção de quebra de texto em colunas
- Popup de doação PIX configurado para 10 minutos

---

## Tecnologias

- **Python 3** + **Flask** — servidor web
- **feedparser** — leitura de feeds RSS
- **requests** — requisições HTTP
- **beautifulsoup4** — parsing HTML
- **python-dateutil** — manipulação de datas
- **readability-lxml** — extração de conteúdo de páginas web
- **lxml_html_clean** — compatibilidade com Python 3.13+
- **Jinja2** — templates HTML
- **Google Fonts** — UnifrakturMaguntia, IM Fell English, Playfair Display, Libre Baskerville
- **HTML/CSS** — design vintage responsivo com tema escuro monocromático

---

## Como rodar localmente

**Pré-requisitos:** Certifique-se de ter o Python 3 (versão 3.6 ou superior) e o pip instalados no seu sistema.

**Nota de compatibilidade:** O projeto foi testado e funciona com Python 3.13. As dependências foram atualizadas para garantir compatibilidade com versões mais recentes do Python.

### 1. Clone o repositório

```bash
git clone https://github.com/marcelomodular/politicagem
cd politicagem
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie o servidor

```bash
python app.py
```

Acesse **http://localhost:5000** no navegador.

### Modo terminal (sem servidor)

Para ver as notícias direto no terminal:

```bash
python main.py
```

---

## Versão desktop (Electron)

Também existe uma versão desktop em `electron-app/`.

```bash
cd electron-app
npm install
npm start
```

---

## Estrutura do projeto

```
politicagem/
├── app.py              # Servidor Flask com ordenação cronológica e seleção aleatória
├── scraper.py          # Lógica de scraping via RSS (+40 fontes)
├── main.py             # Modo terminal
├── requirements.txt    # Dependências Python
├── README.md           # Esta documentação
├── LICENSE             # Licença MIT
├── .gitignore          # Arquivos ignorados pelo Git
└── templates/
    ├── index.html      # Interface estilo jornal com 4 colunas
    └── visualizar.html  # Página para visualização completa de artigos
```

---

## Contribuindo

Quer adicionar uma nova fonte? Basta editar `scraper.py` e incluir a URL do feed RSS e o nome do veículo na lista `SOURCES`:

```python
SOURCES = [
    ...
    ("https://exemplo.com.br/feed/", "Nome do Veículo"),
]
```

---

## Licença

MIT — use, modifique e distribua livremente.

---

*"A imprensa é a vista da nação."* — Hipólito da Costa, fundador do Correio Braziliense (1808)



## Onboarding CLI

Para facilitar a primeira configuracao e criar atalho com icone do Politicagem:

```bash
python onboard_cli.py
```

Modo automatico (sem perguntas):

```bash
python onboard_cli.py --auto
```

O onboarding:
- explica a proposta do projeto (agregador RSS sem armazenamento local);
- instala dependencias Python e Electron;
- cria atalho na Area de Trabalho (Windows) usando o icone `electron-app/assets/politicagem-p.ico`.
