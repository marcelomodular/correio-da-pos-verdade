# 📰 Correio da Pós-Verdade

> Agregador de notícias da imprensa independente e progressista brasileira, com interface inspirada nos jornais do início do século XX.

![Interface do Correio da Pós-Verdade](docs/screenshot.png)

---

## Sobre o projeto

O **Correio da Pós-Verdade** é um agregador de notícias que reúne em uma única página os principais despachos de veículos independentes, investigativos e progressistas do Brasil. A interface imita a estética dos jornais impressos da década de 1930 — tipografia serifada, colunas, capitulares e papel envelhecido — como contraponto irônico à era da desinformação.

As notícias são buscadas em tempo real via **RSS**, sem armazenamento em banco de dados.

---

## Fontes monitoradas

| Categoria | Veículos |
|---|---|
| Imprensa investigativa | Agência Pública, Intercept Brasil, Ponte Jornalismo, Observatório da Imprensa |
| Imprensa progressista | Vermelho, Opera Mundi, Jacobin Brasil, Le Monde Diplomatique, MST, ICL Notícias, Revista Fórum, Jornal GGN, Carta Capital |
| Partidos / organizações | Fundação Perseu Abramo, PCB |
| Outros | Revista Opera, Jones Manoel, Subverta, O Minhocário |

---

## Funcionalidades

- 🗞️ Interface estilo jornal impresso dos anos 1930
- 🔎 Busca por palavra-chave em tempo real
- 📡 Agregação via RSS de 18+ fontes
- 🖥️ Modo terminal (sem servidor web)
- 📱 Layout responsivo para mobile

---

## Tecnologias

- **Python 3** + **Flask** — servidor web
- **feedparser** — leitura de feeds RSS
- **Jinja2** — templates HTML
- **Google Fonts** — UnifrakturMaguntia, IM Fell English, Playfair Display, Libre Baskerville

---

## Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/marcelomodular/correio-da-pos-verdade
cd correio-da-pos-verdade
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

## Estrutura do projeto

```
correio-da-pos-verdade/
├── app.py              # Servidor Flask (rota principal)
├── scraper.py          # Lógica de scraping via RSS
├── main.py             # Modo terminal
├── requirements.txt    # Dependências Python
└── templates/
    └── index.html      # Interface estilo jornal
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

