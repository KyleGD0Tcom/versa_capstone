from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        selected_department = request.POST['department']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.groups.filter(name=selected_department).exists():
                login(request, user)
                if selected_department == 'Admin':
                    return redirect('dashboard')
                elif selected_department == 'Delivery':
                    return redirect('delivery_dashboard')
                elif selected_department == 'Motorpool':
                    return redirect('motorpool_dashboard')
                elif selected_department == 'Sales':
                    return redirect('sales_dashboard')
                elif selected_department == 'Warehouse':
                    return redirect('warehouse_dashboard')
                elif selected_department == 'Aftersales':
                    return redirect('aftersales_dashboard')
            else:
                return render(request, 'accounts/login.html', {'error': 'User does not belong to the selected department'})
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')