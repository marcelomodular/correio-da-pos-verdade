from flask import Flask, render_template, request, jsonify
from scraper import get_all_news
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    busca = request.args.get('busca', '').strip().lower()
    noticias = get_all_news()

    if busca:
        noticias = [
            n for n in noticias
            if busca in n['titulo'].lower() or busca in n['resumo'].lower()
        ]

    # Ordenar todas as notícias por data de publicação (mais recentes primeiro)
    def parse_date(noticia):
        if noticia.get('data'):
            try:
                # Tentar diferentes formatos de data
                formatos = [
                    '%a, %d %b %Y %H:%M:%S %Z',  # RFC 2822
                    '%Y-%m-%dT%H:%M:%S%z',       # ISO 8601
                    '%Y-%m-%d %H:%M:%S',         # YYYY-MM-DD HH:MM:SS
                    '%d/%m/%Y %H:%M',            # DD/MM/YYYY HH:MM
                    '%d/%m/%Y',                  # DD/MM/YYYY
                    '%Y-%m-%d',                  # YYYY-MM-DD
                ]
                for formato in formatos:
                    try:
                        return datetime.strptime(noticia['data'], formato)
                    except ValueError:
                        continue
                # Se nenhum formato funcionar, usar timestamp atual
                return datetime.now()
            except:
                return datetime.now()
        return datetime.now()

    # Filtrar notícias que têm data válida e ordenar por data
    noticias_com_data = [n for n in noticias if n.get('data')]
    noticias_sem_data = [n for n in noticias if not n.get('data')]

    # Ordenar notícias com data (mais recentes primeiro)
    noticias_com_data.sort(key=parse_date, reverse=True)

    # Combinar: notícias com data ordenadas + notícias sem data
    noticias = noticias_com_data + noticias_sem_data

    # Selecionar aleatoriamente a notícia principal (headline)
    if len(noticias) > 0:
        # Escolher aleatoriamente uma notícia para ser o headline
        headline_index = random.randint(0, len(noticias) - 1)
        headline = noticias[headline_index]

        # Remover o headline da lista e colocar no início
        noticias.pop(headline_index)
        noticias.insert(0, headline)

    return render_template('index.html', noticias=noticias, busca=busca)


@app.route('/visualizar')
def visualizar_noticia():
    from urllib.parse import unquote_plus
    
    url = request.args.get('url', '')
    titulo = request.args.get('titulo', '')
    fonte = request.args.get('fonte', '')
    
    # Decodificar parâmetros
    if url:
        url = unquote_plus(url)
    if titulo:
        titulo = unquote_plus(titulo)
    if fonte:
        fonte = unquote_plus(fonte)
    
    if not url:
        return jsonify({'error': 'URL não fornecida'}), 400
    
    return render_template('visualizar.html', url=url, titulo=titulo, fonte=fonte)


@app.route('/extrair_conteudo')
def extrair_conteudo():
    from urllib.parse import unquote_plus
    
    url = request.args.get('url', '')
    
    # Decodificar URL
    if url:
        url = unquote_plus(url)
    
    print(f"DEBUG: Extraindo conteúdo da URL: {url}")
    
    if not url:
        return jsonify({'error': 'URL não fornecida'}), 400
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remover elementos indesejados
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'menu', 'advertisement', 'sidebar', '.sidebar', '.related', '.comments']):
            element.decompose()
        
        # Estratégia 1: Procurar por elementos article que contenham h1
        articles_with_h1 = []
        for article in soup.find_all('article'):
            if article.find('h1') or article.find('h2'):
                articles_with_h1.append(article)
        
        if articles_with_h1:
            # Pegar o artigo com mais texto
            content = max(articles_with_h1, key=lambda x: len(x.get_text()))
            print(f"DEBUG: Encontrado article com h1/h2")
        
        else:
            # Estratégia 2: Procurar por elementos com classes de conteúdo
            content_selectors = [
                '.post-content',
                '.entry-content', 
                '.article-content',
                '.content-main',
                '.post-body',
                '.entry-body',
                '.article-body',
                'main .content',
                '.single-content',
                '.post-inner',
                '.entry',
                '[role="article"]',
                'main'
            ]
            
            content = None
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    # Pegar o elemento com mais texto (provavelmente o conteúdo principal)
                    content = max(elements, key=lambda x: len(x.get_text()))
                    print(f"DEBUG: Encontrado conteúdo com seletor: {selector}")
                    break
        
        if not content:
            # Estratégia 3: Procurar por divs com muita texto
            all_divs = soup.find_all('div')
            text_divs = [div for div in all_divs if len(div.get_text()) > 200]
            if text_divs:
                content = max(text_divs, key=lambda x: len(x.get_text()))
                print(f"DEBUG: Usando div com mais texto como fallback")
        
        if not content:
            # Fallback final para o body
            content = soup.find('body')
            print(f"DEBUG: Usando body como último fallback")
        
        if content:
            # Limpar o conteúdo
            text_content = content.get_text(separator='\n', strip=True)
            
            # Remover linhas em branco excessivas
            lines = [line.strip() for line in text_content.split('\n') if line.strip()]
            text_content = '\n'.join(lines)
            
            # Limitar tamanho para não sobrecarregar
            text_content = text_content[:5000] + '...' if len(text_content) > 5000 else text_content
            
            # Validar se o conteúdo faz sentido (não é muito curto)
            if len(text_content.strip()) < 50:
                return jsonify({'error': 'Conteúdo muito curto ou inválido'}), 404
            
            # Obter o título da página
            page_title = soup.title.string if soup.title else 'Título não encontrado'
            
            # Verificar se há h1 ou h2 no conteúdo para validar
            content_h1 = content.find('h1')
            content_h2 = content.find('h2')
            
            print(f"DEBUG: Título da página: {page_title}")
            print(f"DEBUG: H1 no conteúdo: {content_h1.get_text() if content_h1 else 'Nenhum'}")
            print(f"DEBUG: H2 no conteúdo: {content_h2.get_text() if content_h2 else 'Nenhum'}")
            print(f"DEBUG: Primeiros 200 chars do conteúdo: {text_content[:200]}...")
            
            return jsonify({
                'conteudo': text_content,
                'titulo': page_title,
                'h1': content_h1.get_text() if content_h1 else None,
                'h2': content_h2.get_text() if content_h2 else None,
                'sucesso': True
            })
        else:
            return jsonify({'error': 'Conteúdo não encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Erro ao extrair conteúdo: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
