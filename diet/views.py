from typing import final
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from diet.forms import UserBMIForm

from .models import Menu, UserBMI
# Create your views here.

import secrets
import collections
import random
import os

Menu_namedTuple = collections.namedtuple(
    'Menu_namedTuple', ['nama', 'protein', 'lemak', 'karbo', 'kalori'])
menu_laukHewani = []
menu_laukNabati = []
menu_sayur = []
menu_nasi = []


def generate_menuSatuHari():
    menu_satuHari = []
    genome_nasi = secrets.choice(menu_nasi)
    genome_hewani = secrets.choice(menu_laukHewani)
    genome_nabati = secrets.choice(menu_laukNabati)
    genome_sayur = secrets.choice(menu_sayur)
    menu_satuHari.insert(0, genome_nasi)
    menu_satuHari.insert(1, genome_hewani)
    menu_satuHari.insert(2, genome_nabati)
    menu_satuHari.insert(3, genome_sayur)
    return menu_satuHari


def generate_genome(size: int):
    genome = []
    for i in range(0, size):
        for j in range(0, 3):
            menu_satuHari = []
            genome_nasi = secrets.choice(menu_nasi)
            genome_hewani = secrets.choice(menu_laukHewani)
            genome_nabati = secrets.choice(menu_laukNabati)
            genome_sayur = secrets.choice(menu_sayur)
            menu_satuHari.insert(0, genome_nasi)
            menu_satuHari.insert(1, genome_hewani)
            menu_satuHari.insert(2, genome_nabati)
            menu_satuHari.insert(3, genome_sayur)
        genome.insert(j, menu_satuHari)
    return genome


def generate_population(size: int):
    population = []
    for i in range(size):
        population.insert(i, generate_genome(21))  # 21 = 7 hari * 3 kali makan
    return population


def generate_fitness(limit_kalori: int, population: list):
    fitness = []
    idx = 0
    for genome in population:
        fitness_pct = 0
        kalori = 0
        for hari in (genome):
            for i in hari:
                kalori += i.kalori
        fitness_pct = (kalori/limit_kalori) * 100
        if (kalori > limit_kalori):
            fitness.insert(idx, 0)
        else:
            fitness.insert(idx, fitness_pct)
        idx += 1
    return fitness


def selection(fitness: list):
    fitness_clone = fitness[:]
    parent1 = max(fitness_clone, key=float)
    parent1_index = fitness.index(parent1)
    fitness_clone.pop(parent1_index)
    parent2 = max(fitness_clone, key=float)
    parent2_index = fitness.index(parent2)
    return [parent1_index, parent2_index]


def crossover(parent1: list, parent2: list):
    child1 = parent1[:]
    child2 = parent2[:]
    crossover_point = round(len(child1)/2)
    child1[0:crossover_point] = parent2[0:crossover_point]
    child2[0:crossover_point] = parent1[0:crossover_point]
    return [child1, child2]


def mutation(child: list, mutation_rate: int):
    mutant = child[:]
    for i in range(len(mutant)):
        if(random.uniform(0, 1) <= mutation_rate):
            mutant[i] = generate_menuSatuHari()
    return mutant


def regeneration(population: list, fitness: list, mutant1: list, mutant2: list):
    min_selection1 = min(fitness, key=float)
    min_selection1_index = fitness.index(min_selection1)
    fitness.pop(min_selection1_index)
    population.pop(min_selection1_index)
    min_selection2 = min(fitness, key=float)
    min_selection2_index = fitness.index(min_selection2)
    fitness.pop(min_selection2_index)
    population.pop(min_selection2_index)
    population.append(mutant1)
    population.append(mutant2)
    return population


def homepage(request):
    if request.user.is_authenticated:
        UserBMIData = UserBMI.objects.all().filter(user=request.user)

        for menu in Menu.objects.all().filter(jenis="Lauk Hewani"):
            menu_laukHewani.append(Menu_namedTuple(menu.nama, menu.protein,
                                                   menu.lemak, menu.karbo, menu.kalori))
        for menu in Menu.objects.all().filter(jenis="Lauk Nabati"):
            menu_laukNabati.append(Menu_namedTuple(menu.nama, menu.protein,
                                                   menu.lemak, menu.karbo, menu.kalori))
        for menu in Menu.objects.all().filter(jenis="Sayur"):
            menu_sayur.append(Menu_namedTuple(menu.nama, menu.protein,
                                              menu.lemak, menu.karbo, menu.kalori))
        for menu in Menu.objects.all().filter(jenis="Nasi"):
            menu_nasi.append(Menu_namedTuple(menu.nama, menu.protein,
                                             menu.lemak, menu.karbo, menu.kalori))

        mutation_rate = 0.05
        isLooping = True
        if len(UserBMIData) != 0:
            for user_info in UserBMIData:
                bmr = user_info.bmr
                limit_kalori = round(bmr * 7)
            final_menu = []
            population = generate_population(30)
            fitness = generate_fitness(limit_kalori, population)

            generation = 0
            while(isLooping):
                parents = selection(fitness)
                parent1 = population[parents[0]]
                parent2 = population[parents[1]]

                [child1, child2] = crossover(parent1, parent2)

                mutant1 = mutation(child1, mutation_rate)
                mutant2 = mutation(child2, mutation_rate)

                population = regeneration(
                    population, fitness, mutant1, mutant2)
                fitness = generate_fitness(limit_kalori, population)

                # os.system('cls' if os.name == 'nt' else 'clear')
                print(f"Best Fitness: {max(fitness)}")

                generation += 1
                if(generation == 1000 or max(fitness) == 100):
                    isLooping = False
                    kalori_sementara = 0
                    population_index = fitness.index(max(fitness))
                    for i in population[population_index]:
                        final_menu.append(i)
                        for j in i:
                            kalori_sementara += j.kalori
                            # print(kalori_sementara)
                print(f"Best solution found at {generation} generations!")
                print(f"=========================")

            final_menu_senin = final_menu[0:3]
            final_menu_selasa = final_menu[3:6]
            final_menu_rabu = final_menu[6:9]
            final_menu_kamis = final_menu[9:12]
            final_menu_jumat = final_menu[12:15]
            final_menu_sabtu = final_menu[15:18]
            final_menu_minggu = final_menu[18:21]

            return render(request=request,
                          template_name="diet/diet.html",
                          context={"users": UserBMIData,
                                   "menu_senin": final_menu_senin,
                                   "menu_selasa": final_menu_selasa,
                                   "menu_rabu": final_menu_rabu,
                                   "menu_kamis": final_menu_kamis,
                                   "menu_jumat": final_menu_jumat,
                                   "menu_sabtu": final_menu_sabtu,
                                   "menu_minggu": final_menu_minggu, })
        else:
            return render(request=request,
                          template_name="diet/diet.html")
    else:
        return redirect("diet:login")

# Temporary testing


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user)
            return redirect("diet:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

    form = UserCreationForm
    return render(request,
                  "diet/register.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.success(request, "Logged out sucessfully")
    return redirect("diet:login")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are logged in as {username}")
                return redirect("diet:homepage")
            else:
                messages.error(request, f"Invalid username or password")
        else:
            messages.error(request, f"Invalid username or password")

    form = AuthenticationForm()
    return render(request,
                  "diet/login.html",
                  context={"form": form})


def data(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = UserBMIForm(initial={'user': request.user})
            return render(request=request,
                          template_name="diet/data.html",
                          context={"form": form})
        else:
            form = UserBMIForm(
                initial={'user': request.user}, data=request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                tinggi_badan = form.cleaned_data.get('tinggi_badan')
                berat_badan = form.cleaned_data.get('berat_badan')
                jenis_kelamin = form.cleaned_data.get('jenis_kelamin')
                tingkat_aktivitas = form.cleaned_data.get('tingkat_aktivitas')
                usia = form.cleaned_data.get('umur')


                if ((tinggi_badan <= 0) or (berat_badan <= 0) or (usia <= 0) or (tinggi_badan > 272) or (berat_badan > 635) or (usia > 122)):
                    messages.error(request, f"Please reinput your data correctly")
                    return render(request,
                        "diet/data.html",
                        context={"form": form})


                bmi = berat_badan / ((tinggi_badan/100) * (tinggi_badan/100))

                if(jenis_kelamin == 'Laki-laki'):
                    bmr = 66 + (13.7 * berat_badan) + \
                        (5 * tinggi_badan) - (6.8 * usia)
                else:
                    bmr = 655 + (9.6 * berat_badan) + \
                        (1.8 * tinggi_badan) - (4.7 * usia)

                if(tingkat_aktivitas == "Sedantary"):
                    bmr = bmr * 1.2
                elif(tingkat_aktivitas == "Exercise 1-3"):
                    bmr = bmr * 1.375
                elif(tingkat_aktivitas == "Exercise 4-5"):
                    bmr = bmr * 1.55
                elif(tingkat_aktivitas == "Daily"):
                    bmr = bmr * 1.725
                elif(tingkat_aktivitas == "Intense"):
                    bmr = bmr * 1.9

                if (bmr <= 0 or bmi <= 0):
                    messages.error(request, f"Please reinput your data correctly")
                    return render(request,
                        "diet/data.html",
                        context={"form": form})
                

                obj.bmi = bmi
                obj.bmr = bmr

                obj, created = UserBMI.objects.update_or_create(
                    user=request.user,
                    defaults={'user': request.user, 'umur': usia, 'tinggi_badan': tinggi_badan,
                              'berat_badan': berat_badan, 'jenis_kelamin': jenis_kelamin, 'bmi': bmi,
                              'bmr': bmr}
                )
                # form.save()
                return redirect("diet:homepage")
    else:
        return redirect("diet:login")

# TO DO: Detect if bmi/bmr data exist, if yes update, if no create
#  TO DO: Restrict pages
