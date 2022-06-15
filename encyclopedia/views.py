from django.shortcuts import  render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse 
from markdown2 import Markdown
import re
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


''' 
    This function shows an extisting entry or an error if we get a None, rendering entry.html or error.html:
''' 
def entry (request, title):
    mdown = Markdown()
    entry_list = util.list_entries()
    if title in entry_list:
        entry_page = util.get_entry(title)
        return render(request, "encyclopedia/entry.html",{
            "entry": mdown.convert(entry_page),
            "entry_title": title
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "entry_title": title
        })


''' 
    This function checks if there is an entry with exactly the same letters we typed and then shows it directly.
    The loop checks if the value we type is part of a specific title.
    Also avoid possible confusions between upper and lowercase.
    Then, the value is appended to the list substring.
'''    
def search(request):
    entry_list = util.list_entries()
    if request.method == 'POST':
        substring = []
        query = request.POST
        query = query['q']
        for page in entry_list:
            if re.search(query.lower(), page.lower()):
                substring.append(page)
            if query.lower() == page.lower():
                return redirect(entry, title=page)
        if len(query) == 0:
            return render(request, "encyclopedia/error.html",{
            'error': f'You have not entered any search.'
        })
        return render(request, "encyclopedia/search.html", {
            "entries": substring 
        })


''' 
    This function allows to enter new entries to our encyclopedia.
    It appends the new entry to an empty list and then redirects to the index page. 
    If we write nothing or the new entry already exists, we will get an error message.
''' 
def new_entry(request):
    entry_list = util.list_entries()
    lower_list = []
    for entry in entry_list:
        lower_list.append(entry.lower())
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if len(title) == 0:
            return render(request, "encyclopedia/error.html",{
            'error': f'You have not entered any new page.'
        })
        if title.lower() not in lower_list:
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "encyclopedia/new_entry.html", {
            "existing": True,
            "entry": title
        })
    return render(request, "encyclopedia/new_entry.html",{
        "existing": False
    })


''' 
    This function allows to edit an entry getting its already existing text. 
    When Submit is clicked, it saves the edited entry and go back to that specific entry page.
''' 
def edit(request, title):
    content = util.get_entry(title)
    if request.method == 'POST':
        content = request.POST.get('new')
        util.save_entry(title, content)  
        return redirect(entry, title = title)     
    return render(request, "encyclopedia/edit.html", {
        "content": content,
        "entry_title": title
    })


''' 
    This function selects a random entry.
''' 
def random_entry(request):
    entries = util.list_entries()
    choice = random.choice(entries)
    content = util.get_entry(choice)
    mdown = Markdown()
    return render(request, "encyclopedia/entry.html",{
            "entry": mdown.convert(content),
            "entry_title": choice
        })