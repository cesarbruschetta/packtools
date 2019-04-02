# coding: utf-8
from flask import g, Blueprint, render_template, current_app, request, url_for
import packtools
from forms import XMLUploadForm
from utils import analyze_xml

main = Blueprint("main", __name__)


@main.before_app_request
def add_context_settings():
    setattr(
        g,
        "SETTINGS_MAX_UPLOAD_SIZE",
        current_app.config.get("SETTINGS_MAX_UPLOAD_SIZE"),
    )
    setattr(g, "PACKTOOLS_VERSION", current_app.config.get("PACKTOOLS_VERSION"))


@main.route("/", methods=["GET", "POST"])
def packtools_home():

    form = XMLUploadForm()
    context = dict(form=form)
    if form.validate_on_submit():

        if form.add_scielo_br_rules.data:
            extra_sch = packtools.catalogs.SCHEMAS["scielo-br"]
        else:
            extra_sch = None

        results, exc = analyze_xml(form.file.data, extra_schematron=extra_sch)
        context["results"] = results
        context["xml_exception"] = getattr(exc, "message", getattr(exc, "msg", str(exc)))

    return render_template("validator/stylechecker.html", **context)


@main.route("/previews", methods=["GET", "POST"])
def packtools_preview_html():

    form = XMLUploadForm()
    context = dict(form=form)
    if form.validate_on_submit():

        previews = []
        try:
            for lang, html_output in packtools.HTMLGenerator.parse(
                form.file.data,
                valid_only=False,
                css=url_for("static", filename="css/htmlgenerator/scielo-article.css"),
                print_css=url_for(
                    "static", filename="css/htmlgenerator/scielo-bundle-print.cs"
                ),
                js=url_for("static", filename="js/htmlgenerator/scielo-article-min.js"),
            ):
                previews.append({"lang": lang, "html": html_output})
        except Exception as e:
            # print(e.message)
            # qualquer exeção aborta a pre-visualização mas continua com o resto
            previews = []

        context["previews"] = previews

    return render_template("validator/preview_html.html", **context)
