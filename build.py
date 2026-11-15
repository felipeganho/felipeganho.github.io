"""Gera o index.html a partir dos arquivos em data/.

Uso: python build.py
Só biblioteca padrão. A página sai estática (funciona sem JavaScript e é indexável).
"""

import json
from html import escape
from pathlib import Path

RAIZ = Path(__file__).parent
DADOS = RAIZ / "data"
SITE = "https://felipeganho.github.io/"


def carregar(nome):
    return json.loads((DADOS / f"{nome}.json").read_text(encoding="utf-8"))


def e(texto):
    return escape(texto or "", quote=True)


def chips(itens):
    return "".join(f'<li class="chip">{e(i)}</li>' for i in itens)


def secao(ident, titulo, corpo):
    return f'<section id="{ident}" aria-labelledby="{ident}-t"><h2 id="{ident}-t">{titulo}</h2>{corpo}</section>'


def linha(periodo, titulo, sub, extra=""):
    return (
        '<article class="linha">'
        f'<p class="periodo">{e(periodo)}</p>'
        f'<div><h3>{e(titulo)}</h3><p class="sub">{e(sub)}</p>{extra}</div>'
        "</article>"
    )


def bloco_experiencia(itens):
    partes = []
    for x in itens:
        extra = ""
        if x.get("contexto"):
            extra += f'<p class="contexto">{e(x["contexto"])}</p>'
        if x.get("destaques"):
            extra += "<ul>" + "".join(f"<li>{e(d)}</li>" for d in x["destaques"]) + "</ul>"
        partes.append(linha(x["periodo"], x["cargo"], f'{x["empresa"]} · {x["local"]}', extra))
    return "".join(partes)


def bloco_projetos(itens):
    cartoes = []
    for p in itens:
        nome = e(p["nome"])
        if p.get("link"):
            nome = f'<a href="{e(p["link"])}">{nome}</a>'
        cartoes.append(
            '<article class="cartao">'
            f'<p class="tipo">{e(p["tipo"])}</p><h3>{nome}</h3>'
            f'<p>{e(p["descricao"])}</p><ul class="chips">{chips(p["stack"])}</ul>'
            "</article>"
        )
    return f'<div class="grade">{"".join(cartoes)}</div>'


def bloco_competencias(grupos):
    return '<dl class="comp">' + "".join(
        f'<div><dt>{e(g["grupo"])}</dt><dd><ul class="chips">{chips(g["itens"])}</ul></dd></div>' for g in grupos
    ) + "</dl>"


def bloco_formacao(itens, certs, idiomas):
    form = "".join(linha(f["periodo"], f["curso"], f["instituicao"]) for f in itens)
    cert = "".join(linha(c["ano"], c["nome"], c["emissor"]) for c in certs)
    idi = " · ".join(f'{e(i["idioma"])} ({e(i["nivel"])})' for i in idiomas)
    return (
        form
        + '<h3 class="subtitulo">Cursos e certificações</h3>'
        + cert
        + f'<h3 class="subtitulo">Idiomas</h3><p class="idiomas">{idi}</p>'
    )


def json_ld(perfil, formacao):
    dados = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": perfil["nome"],
        "jobTitle": "Tech Lead",
        "url": SITE,
        "image": perfil["foto"] if perfil["foto"].startswith("http") else SITE + perfil["foto"],
        "sameAs": [l["url"] for l in perfil["links"]],
        "alumniOf": [{"@type": "CollegeOrUniversity", "name": f["instituicao"]} for f in formacao[:3]],
        "knowsAbout": ["Go", "PHP", "Laravel", "Python", "TypeScript", "dbt", "Data Warehouse", "Docker", "Terraform", "RAG", "Agentes de IA"],
    }
    return json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")


def main():
    perfil = carregar("perfil")
    exp = carregar("experiencia")
    proj = carregar("projetos")
    comp = carregar("competencias")
    form = carregar("formacao")
    certs = carregar("certificacoes")
    idiomas = carregar("idiomas")

    secoes = [
        ("experiencia", "Experiência", bloco_experiencia(exp)),
        ("projetos", "Projetos", bloco_projetos(proj)),
        ("competencias", "Competências", bloco_competencias(comp)),
        ("formacao", "Formação", bloco_formacao(form, certs, idiomas)),
    ]
    nav = "".join(f'<a href="#{i}">{t}</a>' for i, t, _ in secoes)
    corpo = "".join(secao(i, t, c) for i, t, c in secoes)
    links = "".join(f'<a href="{e(l["url"])}" rel="me">{e(l["rotulo"])}</a>' for l in perfil["links"])
    descricao = f'{perfil["nome"]}: {perfil["cargo"]}. Back-end, dados e IA aplicada em fintech.'

    foto_abs = perfil["foto"] if perfil["foto"].startswith("http") else SITE + perfil["foto"]

    modelo = (RAIZ / "modelo.html").read_text(encoding="utf-8")
    html = (
        modelo.replace("{{foto_abs}}", e(foto_abs))
        .replace("{{titulo}}", e(f'{perfil["nome"]} · {perfil["cargo"]}'))
        .replace("{{descricao}}", e(descricao))
        .replace("{{foto}}", e(perfil["foto"]))
        .replace("{{nome}}", e(perfil["nome"]))
        .replace("{{cargo}}", e(perfil["cargo"]))
        .replace("{{local}}", e(perfil["local"]))
        .replace("{{links}}", links)
        .replace("{{resumo}}", e(perfil["resumo"]))
        .replace("{{nav}}", nav)
        .replace("{{secoes}}", corpo)
        .replace("{{jsonld}}", json_ld(perfil, form))
    )
    (RAIZ / "index.html").write_text(html, encoding="utf-8", newline="\n")
    print("index.html gerado")


if __name__ == "__main__":
    main()
