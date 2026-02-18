from flask import Flask, render_template, request
from scraper import get_all_news

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

    return render_template('index.html', noticias=noticias, busca=busca)


if __name__ == '__main__':
    app.run(debug=True)
