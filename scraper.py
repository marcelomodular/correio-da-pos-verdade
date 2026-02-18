import feedparser

# ── RSS Sources ──────────────────────────────────────────────────────────────
# Each entry: (rss_url, display_name)
# Sources without a working public RSS feed are omitted or use best-known URL.
SOURCES = [
    # ── Imprensa independente / investigativa ──
    ("https://apublica.org/feed/",                          "Agência Pública"),
    ("https://theintercept.com/brasil/feed/",               "Intercept Brasil"),
    ("https://ponte.org/feed/",                             "Ponte Jornalismo"),
    ("https://observatoriodaimprensa.com.br/feed/",         "Observatório da Imprensa"),

    # ── Imprensa de esquerda / progressista ──
    ("https://vermelho.org.br/feed/",                       "Vermelho"),
    ("https://operamundi.uol.com.br/feed/",                 "Opera Mundi"),
    ("https://jacobin.com.br/feed/",                        "Jacobin Brasil"),
    ("https://diplomatique.org.br/feed/",                   "Le Monde Diplomatique"),
    ("https://mst.org.br/feed/",                            "MST"),
    ("https://iclnoticias.com.br/feed/",                    "ICL Notícias"),
    ("https://revistaforum.com.br/feed/",                   "Revista Fórum"),
    ("https://jornalggn.com.br/feed/",                      "Jornal GGN"),
    ("https://cartacapital.com.br/feed/",                   "Carta Capital"),

    # ── Partidos / organizações ──
    ("https://fpabramo.org.br/feed/",                       "Fundação Perseu Abramo"),
    ("https://pcb.org.br/feed/",                            "PCB"),

    # ── Outros ──
    ("https://revistaopera.com.br/feed/",                   "Revista Opera"),
    ("https://jonesmanoel.com.br/feed/",                    "Jones Manoel"),
    ("https://subverta.com.br/feed/",                       "Subverta"),
    ("https://ominhocario.com.br/feed/",                    "O Minhocário"),
]


def get_rss_news(url, source_name, limit=5):
    """Fetch articles from a single RSS feed."""
    try:
        feed = feedparser.parse(url)
        noticias = []
        for entry in feed.entries[:limit]:
            noticias.append({
                'titulo':  entry.get('title', 'Sem título'),
                'link':    entry.get('link', '#'),
                'resumo':  entry.get('summary', ''),
                'fonte':   source_name,
                'data':    entry.get('published', ''),
            })
        return noticias
    except Exception as e:
        print(f"Erro ao buscar {source_name}: {e}")
        return []


def get_all_news(limit_per_source=5):
    """Aggregate news from all sources."""
    all_news = []
    for url, name in SOURCES:
        all_news.extend(get_rss_news(url, name, limit=limit_per_source))
    return all_news
