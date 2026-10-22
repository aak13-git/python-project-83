import os

import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.parser import get_data
from page_analyzer.repository import UrlRepository
from page_analyzer.url_validator import norm_url, validate_url

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template(
        'index.html',
    )


@app.route('/urls', methods=['POST'])
def urls_index():
    form_data = request.form.to_dict()
    url_address = form_data.get('url', '')
    errors = validate_url(url_address)

    if errors:
        flash('Некорректный URL', 'danger')
        return render_template(
            'index.html',
            messages=errors,
            url=form_data
        ), 422

    normalized_url = norm_url(url_address)
    repo = UrlRepository(DATABASE_URL)
    url_info = repo.find_url(normalized_url)

    if url_info is not None:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url', id=url_info.get('id')))

    id = repo.add_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url', id=id))


@app.route('/urls/<int:id>')
def get_url(id):
    repo = UrlRepository(DATABASE_URL)
    url_info = repo.find_url_by_id(id)

    if not url_info:
        abort(404)

    return render_template(
        'url.html',
        url_info=url_info,
    )


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    repo = UrlRepository(DATABASE_URL)
    url_info = repo.find_id(id)

    try:
        response = requests.get(url_info.get('name'), timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url', id=id))

    status = response.status_code
    data = get_data(response)
    data['status'] = status
    repo.add_url_check(data, url_info)
    flash('Страница успешно проверена', 'success')
    url_checks = repo.get_url_checks(id)
    return render_template(
        'url.html',
        url_info=url_info,
        url_checks=url_checks,
    )

@app.route('/urls', methods=['GET'])
def urls_list():
    repo = UrlRepository(DATABASE_URL)
    all_urls_checks = repo.get_all()
    return render_template(
      'urls.html',
      all_urls_checks=all_urls_checks,
    )


if __name__ == '__main__':
    app.run(debug=True)