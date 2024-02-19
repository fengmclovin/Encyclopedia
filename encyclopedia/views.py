from django.shortcuts import render

import markdown

from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })

    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def search(request):
    entry_search = request.POST.get('q')

    if entry_search:
        html_content = convert_md_to_html(entry_search)

        if html_content:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })

        else:
            allEntries = util.list_entries()
            reckon = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    reckon.append(entry)

            if reckon:
                return render(request, "encyclopedia/search.html", {
                    "reckon": reckon
                })

            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "No entries found for '{0}'".format(entry_search)
                })
            
    # Handle the case where entry_search is None or html_content is None
    return render(request, "encyclopedia/error.html", {
        "message": "Entry not found"
    })
