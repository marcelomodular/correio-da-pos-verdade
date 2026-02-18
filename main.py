"""
Agregador de Notícias - Modo Terminal
Execute este arquivo para ver as notícias diretamente no terminal,
sem precisar iniciar o servidor web.
"""

from scraper import get_all_news

def main():
    print("\n" + "="*60)
    print("       📰  AGREGADOR DE NOTÍCIAS BRASILEIRAS")
    print("="*60 + "\n")

    noticias = get_all_news()

    if not noticias:
        print("Nenhuma notícia encontrada. Verifique sua conexão com a internet.")
        return

    fonte_atual = None
    for i, noticia in enumerate(noticias, 1):
        if noticia['fonte'] != fonte_atual:
            fonte_atual = noticia['fonte']
            print(f"\n── {fonte_atual} ──────────────────────────")

        print(f"\n[{i}] {noticia['titulo']}")
        print(f"    🔗 {noticia['link']}")
        if noticia.get('data'):
            print(f"    📅 {noticia['data']}")

    print("\n" + "="*60)
    print(f"Total: {len(noticias)} notícias agregadas.")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
