from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from users.models import Studente, Docente, Profile
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from home.models import TesiCreata, Attivita_progettuale_creata, Richiesta_tesi_bozza, Richiesta_prova_finale_bozza
from itertools import chain
from django.core.mail import send_mail
from django.conf import settings



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data.get('username')
            indice = user.find('.')
            if indice != -1:
                matricola = form.cleaned_data.get('matricola')

                if matricola.isnumeric():
                    sd = Studente()
                else:
                    sd = Docente()

                div = user.split('.')
                sd.nome = div[0]
                sd.cognome = div[1]
                sd.matricola = matricola
                sd.mail = form.cleaned_data.get('email')

                form.save()
                all_utenti = User.objects.all()
                for utente in all_utenti:
                    u = utente.username.split('.')
                    if u[0] == sd.nome and u[1] == sd.cognome and utente.email == sd.mail :
                        sd.user = utente

                sd.save()
                messages.success(request, f'Account created for {user}!')

                return redirect('profile')
            else:
                messages.error(request, f'Errore! Username deve essere nome.cognome!!!')
                return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    all_docenti = Docente.objects.all()
    all_studenti = Studente.objects.all()

    all_richiesta_tesi = all_richiesta_pfinale =all_tesi= all_attivita  ={}
    nome = request.user.username.split('.')
    for s in all_studenti:
        if s.nome == nome[0] and s.cognome == nome[1] and s.mail == request.user.email:
            all_richiesta_tesi = Richiesta_tesi_bozza.objects.filter(autore=s).order_by('-date_posted')
            all_richiesta_pfinale = Richiesta_prova_finale_bozza.objects.filter(autore=s).order_by('-date_posted')
    context_richieste = {
        'all_richiesta_tesi': all_richiesta_tesi,
        'all_richiesta_pfinale': all_richiesta_pfinale,
    }

    for doc in all_docenti:
        if doc.nome == nome[0] and doc.cognome == nome[1] and doc.mail == request.user.email:
            all_tesi = TesiCreata.objects.filter(author=doc).order_by('-date_posted')
            all_attivita = Attivita_progettuale_creata.objects.filter(author=doc).order_by('-date_posted')
            tot = list(chain(all_tesi, all_attivita))
        context = {
            'all_tesi': all_tesi,
            'all_attivita': all_attivita,
        }
        if doc.mail == request.user.email:
            return render(request, 'users/profile_doc.html', context)

    for stud in all_studenti:
        if stud.mail == request.user.email:
            return render(request, 'users/profile_stud.html', context_richieste)
