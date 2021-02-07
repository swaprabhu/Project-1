from django.shortcuts import render
import markdown2
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render, redirect
from . import util
import random 

class Edit(forms.Form):
    content_text = forms.CharField(widget=forms.Textarea(), label="")

class Post(forms.Form):
    title = forms.CharField(label= "Title", max_length=50)
    content_text = forms.CharField(widget=forms.Textarea(), label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request,title):
    page_in_md = util.get_entry(title)
    if page_in_md:
        page_in_html=(markdown2.markdown(page_in_md))
        return render(request,"encyclopedia/entry_page.html",{
        "page_in_html": page_in_html,
        "entry": title
        })
    else:
        return render(request,"encyclopedia/status.html",{
        "status":"No such page is found, You can add a Page "    
        })
    
def search(request):
    if request.method=="POST":
        search_query = request.POST.get('q','')
        page_in_md=util.list_entries()
        for i in range(len(page_in_md)):
            if [match for match in page_in_md if search_query.lower() == match.lower()]:
                page =  util.get_entry(search_query) 
                page_in_html=(markdown2.markdown(page))
                return render(request, "encyclopedia/entry_page.html" ,{
                    "page_in_html" : page_in_html,
                    "title" : search_query
                })
                
            elif [match for match in page_in_md if search_query.lower() in match.lower()]:
                matches= [match for match in page_in_md if search_query.lower() in match.lower()]   
                print(f'matches = ',matches)
                return render(request, "encyclopedia/searchPage.html", {
                    "matches": matches
                })  

            else:
                return render(request,"encyclopedia/status.html",{
                "status":"Your search is not found. You can create it."    
                })

def new_page(request):
    if request.method=="POST":
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content_text = form.cleaned_data["content_text"]
            entries = util.list_entries()
            if title in entries:
                return render(request,"encyclopedia/status.html",{"status":"Page with this Title is already exists, You cannot create this Page " })
            else:
                util.save_entry(title,content_text)
                return entry_page(request,title)
    else:
        return render(request,"encyclopedia/add_entry.html", {"form": Edit(), "post": Post()})

def edit_page(request, title):
    if request.method=="POST":
        content_text = request.POST.get('content')
        util.save_entry(title,content_text)
        return HttpResponseRedirect(reverse("wiki:entry",args=[title]))
    else:
        content = util.get_entry(title)
        return render(request,"encyclopedia/edit_page.html", {"title": title,
            "content": content})

def random_page(request):
    entries=util.list_entries()
    title1=random.choice(entries) 
    return entry_page(request,title1)