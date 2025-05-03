from django.shortcuts import get_object_or_404,render, redirect
from .forms import UserReigstration
from .models import Category, Challenge, Solve, Hint, HintUnlock, ChallengeFile
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    
    return render(request, 'home.html')


def dashboardPage(request):

    return render(request, 'dashboard.html')


def loginPage(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                form = AuthenticationForm()
                return redirect('home')
            
    else :
        form = AuthenticationForm()

    Context = {'form' : form}
    return render(request, 'login.html', Context)


def logoutUser(request):
    logout(request)
    request.session.flush()
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = UserReigstration(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserReigstration()
   
    Context = {'form' : form}
    return render(request, 'signup.html', Context)


def about(request):

    return render(request, 'about.html')



@login_required(login_url='login')
def challenges(request):
    
    challenges = Challenge.objects.all()
    
    return render(request, 'challenges/category.html', {'challenges': challenges})



def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    challenges = Challenge.objects.filter(categorie=category)
    
    # Mark challenges as solved for the current user
    if request.user.is_authenticated:
        solved_challenges = Solve.objects.filter(
            user=request.user,
            challenge__in=challenges
        ).values_list('challenge_id', flat=True)
        
        for challenge in challenges:
            challenge.solved = challenge.id in solved_challenges
    else:
        for challenge in challenges:
            challenge.solved = False
    context = {'category': category,'challenges': challenges}

    return render(request, 'challenges/category.html', context=context)



@login_required(login_url='login')
def challenge_detail(request, challenge_id):
    """Get challenge details for the modal"""
    challenge = get_object_or_404(Challenge, id=challenge_id)
    
    # Check if the user has solved this challenge
    solved = Solve.objects.filter(user=request.user, challenge=challenge).exists()
    
    # Get challenge files
    files = []
    files_obj = ChallengeFile.objects.filter(challenge=challenge_id)
    for file in files_obj:
        files.append({
            'id': file.id,
            'name': file.name,
            'size': file.size,
            'url': file.file.url if file.file else None
        })
    
    # Get hints
    hints = []
    hints_obj = Hint.objects.filter(challenge=challenge_id)
    for hint in hints_obj:
        hint_data = {
            'id': hint.id,
            'cost': hint.cost,
            'unlocked': False,
            'description': None
        }
        
        # Check if hint is unlocked for this user
        unlocked = HintUnlock.objects.filter(user=request.user, hint=hint).exists()
        if unlocked:
            hint_data['unlocked'] = True
            hint_data['description'] = hint.description
        
        hints.append(hint_data)
    
    # Prepare response data
    data = {
        'id': challenge_id,
        'title': challenge.title,
        'description': challenge.description,
        'difficulty': challenge.difficulty,
        'points': challenge.point_val,
        'solves': challenge.solve_set(),
        'solved': solved,
        'files': files,
        'hints': hints
    }
    
    return JsonResponse(data)


@login_required(login_url='login')
@require_POST
def submit_flag(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    submitted_flag = request.POST.get('flag', '').strip()
    
    # Check if the user has already solved this challenge
    if Solve.objects.filter(user=request.user, challenge=challenge).exists():
        return JsonResponse({
            'success': False,
            'message': 'You have already solved this challenge!'
        })
    
    # Check if the flag is correct
    if submitted_flag == challenge.flags:
        # Create a solve record
        Solve.objects.create(user=request.user, challenge=challenge)
        
        return JsonResponse({
            'success': True,
            'message': 'Congratulations! You solved the challenge!'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Incorrect flag. Try again!'
        })



@login_required(login_url='url')
@require_POST
def unlock_hint(request, hint_id):
    hint = get_object_or_404(Hint, id=hint_id)  
    message = f'Hint unlocked for {hint.cost} points'

    # Check if the user has already unlocked this hint
    if HintUnlock.objects.filter(user=request.user, hint=hint).exists():
        message = 'Hint already unlocked'

    else:  
        HintUnlock.objects.create(user=request.user, hint=hint)
        
    return JsonResponse({
        'success': True,
        'message': message,
        'content': hint.description
    })


def calculate_user_points(user):
    """Calculate the total points earned by a user from solved challenges"""
    solved_challenges = Solve.objects.filter(user=user).values_list('challenge_id', flat=True)
    total_points = Challenge.objects.filter(id__in=solved_challenges).aggregate(
        total= Sum('points')
    )['total'] or 0
    
    # Subtract points spent on hints
    unlocked_hints = HintUnlock.objects.filter(user=user).values_list('hint_id', flat=True)
    spent_points = Hint.objects.filter(id__in=unlocked_hints).aggregate(
        total= Sum('cost')
    )['total'] or 0
    
    return total_points - spent_points


@login_required(login_url='login')
def leaderboard(request):
    return render(request, 'leaderboard.html')

