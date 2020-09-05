from django.shortcuts import render, redirect, HttpResponse
from .models import FlashCard
from .forms import FlashCardForm
import random
import csv
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# -------------------------------------------------------------------------------

# get number of cards in evey category
def get_counts(all_cards):
    counts = []
    count_alg = all_cards.filter(category='Algorithms').count()
    counts.append(count_alg)
    count_ds = all_cards.filter(category='Data-Structures').count()
    counts.append(count_ds)
    count_com = all_cards.filter(category='Complexity').count()
    counts.append(count_com)
    return counts

# get n popular/most liked cards
def get_popular_cards(all_cards, n):
    popular_cards = all_cards.order_by('likes')[:n]
    return popular_cards

# -------------------------------------------------------------------------------

# home - show all cards without pagination
# def home(request):
#     all_cards = FlashCard.objects.all()
#     cards = sorted(all_cards.order_by('front'), key=lambda x: random.random())
#     counts = get_counts(all_cards)
#     popular_cards = all_cards.order_by('-likes')[:3]
#     context = {'cards':cards, 'counts':counts, 'popular_cards':popular_cards }
#     return render(request, 'flashcards/home.html', context)

# home - show all cards with pagination
def home(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    #cards = sorted(all_cards.order_by('front'), key=lambda x: random.random())
    paginator = Paginator(all_cards, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]

    context = {'page_obj':page_obj, 'counts':counts, 'popular_cards':popular_cards }
    return render(request, 'flashcards/home.html', context)


# get flashcards by a specific category without pagination
# def get_cards_by_category(request, category):
#     all_cards = FlashCard.objects.all()
#     cards = all_cards.filter(category=category)
#     counts = get_counts(all_cards)
#     popular_cards = all_cards.order_by('-likes')[:3]
#     context = {'cards':cards, 'counts':counts, 'popular_cards':popular_cards }
#     return render(request, 'flashcards/home.html', context)


# get flashcards by a specific category with pagination
def get_cards_by_category(request, category):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    cards = all_cards.filter(category=category)
    paginator = Paginator(cards, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'page_obj':page_obj, 'counts':counts, 'popular_cards':popular_cards }
    return render(request, 'flashcards/home.html', context)

# add flashcard
@login_required
def add_card(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    if request.method == 'POST':
        form = FlashCardForm(request.POST)
        if form.is_valid():
            new_card = form.save(commit=False)
            new_card.creator = request.user
            new_card.save()
            messages.success(request, f'Flashcard added!')
            return redirect('home')
    else:
        form = FlashCardForm()

    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'form':form, 'counts':counts, 'popular_cards':popular_cards }
    return render(request, 'flashcards/add_card.html', context)


# edit card
@login_required
def edit_card(request, id):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    card = FlashCard.objects.get(id=id)
    if request.method == 'POST':
        form = FlashCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, f'Flashcard updated!')
            return redirect('home')
    else:
        form = FlashCardForm(instance=card)

    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'form':form, 'counts':counts, 'popular_cards':popular_cards }
    return render(request, 'flashcards/edit_card.html', context)


# search keywords - top 20 results
def search_keywords(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    cards = FlashCard.objects.filter(front__contains=request.GET.get('keywords'))[:20]
    paginator = Paginator(cards, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    counts = get_counts(all_cards)
    popular_cards = all_cards.order_by('-likes')[:3]
    context = {'page_obj': page_obj, 'counts':counts, 'popular_cards':popular_cards}
    return render(request, 'flashcards/home.html', context)


# learn with flashcards
def learn(request):
    if request.user.is_authenticated:
        all_cards = FlashCard.objects.filter(creator=request.user.id)
    else:
        all_cards = FlashCard.objects.all()
    cards = all_cards.filter(known=0)
    cards = sorted(cards.order_by('likes'), key=lambda x: random.random())
    context = {'card': cards[0]}
    return render(request, 'flashcards/learn.html', context)


# mark a card as known
@login_required
def mark_known(request, id):
    card = FlashCard.objects.get(id=id)
    card.known = 1
    card.save()
    return redirect('learn')


# liking a card
def mark_liked(request, id):
    card = FlashCard.objects.get(id=id)
    card.likes += 1
    card.save()
    return redirect('home')


# save and export cards as csv file
def dump_csv(request):
    cards = FlashCard.objects.all()
    response = HttpResponse (content_type='text/csv')
    writer = csv.writer(response)
    response['Content-Disposition'] = 'attachment; filename="flashcards.csv"'
    fieldnames = ['ID', 'Category', 'Front', 'Back', 'Creator', 'Likes', 'Known']
    writer.writerow(fieldnames)
    output = []
    for card in cards:
            output.append([card.id, card.category, card.front, card.back, card.creator, card.likes, card.known])
    writer.writerows(output)
    # with open('flashcards.csv', 'w', newline='') as file:
    #     fieldnames = ['ID', 'Category', 'Front', 'Back', 'Creator', 'Likes', 'Known']
    #     writer = csv.writer(file)
    #     writer.writerow(fieldnames)
    #     for card in cards:
    #         output.append([card.id, card.category, card.front, card.back, card.creator, card.likes, card.known])
    #     writer.writerows(output)
    return response



    