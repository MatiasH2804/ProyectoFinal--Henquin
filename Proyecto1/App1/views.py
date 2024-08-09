from django.shortcuts import render, redirect
from .models import Ingreso, Gasto, Avatar
from .forms import IngresoForm, GastoForm, AvatarForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
import csv

@login_required
def registrar_ingreso(request):
    if request.method == 'POST':
        form = IngresoForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)
            ingreso.user = request.user
            ingreso.save()
            return redirect('resumen_financiero')
    else:
        form = IngresoForm()
    return render(request, 'App1/registrar_ingreso.html', {'form': form})

@login_required
def registrar_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.user = request.user
            gasto.save()
            return redirect('resumen_financiero')
    else:
        form = GastoForm()
    return render(request, 'App1/registrar_gasto.html', {'form': form})

@login_required
def resumen_financiero(request):
    ingresos = Ingreso.objects.filter(user=request.user)
    gastos = Gasto.objects.filter(user=request.user)
    saldo_restante = sum(ingreso.cantidad for ingreso in ingresos) - sum(gasto.cantidad for gasto in gastos)
    total_ingresos = sum(ingreso.cantidad for ingreso in ingresos)
    total_gastos = sum(gasto.cantidad for gasto in gastos)
    
    for ingreso in ingresos:
        ingreso.fecha = ingreso.fecha.strftime('%d/%m/%Y')
    
    for gasto in gastos:
        gasto.fecha = gasto.fecha.strftime('%d/%m/%Y')
    
    return render(request, 'App1/resumen_financiero.html', {
        'ingresos': ingresos,
        'gastos': gastos,
        'saldo_restante': saldo_restante,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos
    })

@login_required
def download_data(request):
    ingresos = Ingreso.objects.filter(user=request.user)
    gastos = Gasto.objects.filter(user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="finanzas.csv"'

    writer = csv.writer(response)
    writer.writerow(['Fecha','|     |', 'Monto','|     |', 'Categoria','|     |', 'Medio de Pago'])

    for ingreso in ingresos:
        writer.writerow([ingreso.fecha.strftime('%d/%m/%Y'),'|     |', ingreso.cantidad,'|     |', ingreso.categoria])
    
    for gasto in gastos:
        writer.writerow([gasto.fecha.strftime('%d/%m/%Y'),'|     |', gasto.cantidad,'|     |', gasto.categoria,'|     |', gasto.medio_pago])

    return response

@login_required
def reset_data(request):
    if request.method == 'POST':
        if request.user.check_password(request.POST['password']):
            Ingreso.objects.filter(user=request.user).delete()
            Gasto.objects.filter(user=request.user).delete()
            return redirect('resumen_financiero')
    return redirect('resumen_financiero')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'App1/register.html', {'form': form})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user.avatar)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = AvatarForm(instance=request.user.avatar)
    return render(request, 'App1/editar_perfil.html', {'form': form})

def inicio(request):
    return render(request, 'App1/index.html')

def about(request):
    return render(request, 'App1/about.html')
