from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Source, Freqlist
from .forms import SourceForm
from django.shortcuts import redirect, get_object_or_404
from Translator.Frequency_list import TranslationandAlignment, Frequency_list


def post_new(request):
    if request.method == "POST":
        form = SourceForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
	    reassign = form.save(commit=False)
	    Returned_list = TranslationandAlignment(reassign.text)
            reassign.translation = Returned_list[0]
            reassign.alignment = Returned_list[1]
            reassign.save()
            return redirect('post_detail', pk=reassign.pk)
    else:
        form = SourceForm()
    return render(request, 'SourceTexts/post_edit.html', {'form': form})

def post_delete(request, pk):
    todelete = Source.objects.get(pk=pk)
    todelete.delete()
    posts = Source.objects.filter()
    return render(request, 'SourceTexts/post_list.html', {'posts': posts}) 

def post_list(request):
    posts = Source.objects.filter()
    return render(request, 'SourceTexts/post_list.html', {'posts': posts})

#Gotta fix the while loop
def frequency_list(request, pk):
    firstsourcetextinstance = Source.objects.get(pk=pk)
    FL = Freqlist.objects.filter(postpk=firstsourcetextinstance)
    if FL.count()>0:
        return render(request, 'SourceTexts/Freq_list.html', {'FL': FL})
    else:
        sourcetextinstance = Source.objects.get(pk=pk)
        Result = Frequency_list(sourcetextinstance.text, sourcetextinstance.translation, sourcetextinstance.alignment)
        print Result
        print Result * 5
        i = 0
        for x in Result:
            Duh = Result[i]
            print Duh
            B2 = Freqlist(postpk=sourcetextinstance, source_text_string=Duh[0], translation_text_string=Duh[1], frequency=Duh[2])
            B2.save()
	    i = i + 1
        return render(request, 'SourceTexts/Freq_list.html', {'FL': FL})

def post_edit(request, pk):
    post = get_object_or_404(Source, pk=pk)
    if request.method == "POST":
        form = SourceForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = SourceForm(instance=post)
    return render(request, 'SourceTexts/post_edit.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Source, pk=pk)
    return render(request, 'SourceTexts/post_detail.html', {'post': post})

