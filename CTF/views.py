from django.shortcuts import get_object_or_404,render, redirect
from .forms import UserReigstration
from .models import Category, Challenge, Solve, Hint, HintUnlock, ChallengeFile, CustomeUser
from django.db.models import Sum, Max
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


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
    category = Category.objects.all()
    return render(request, 'challenges/category.html', {'challenges': challenges, 'category' : category})



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
def challenge_details(request, category_name, challenge_title):
    """Render the challenge detail page"""
    challenge = get_object_or_404(Challenge, title=challenge_title)
    category = get_object_or_404(Category, name=category_name)

    # Check if the user has solved this challenge
    solved = False
    if request.user.is_authenticated:
        solved = Solve.objects.filter(user=request.user, challenge=challenge).exists()
    
    # Get challenge files
    files = ChallengeFile.objects.filter(challenge=challenge)
    
    # Get unlocked hints for this user
    unlocked_hints = []
    locked_hints = []
    
    if request.user.is_authenticated:
        unlocked_hints = Hint.objects.filter(
            challenge=challenge,
            hintunlock__user=request.user
        )
        
        # Get locked hints (that the user hasn't unlocked yet)
        locked_hints = Hint.objects.filter(
            challenge=challenge
        ).exclude(
            id__in=[hint.id for hint in unlocked_hints]
        )
    else:
        # If user is not authenticated, all hints are locked
        locked_hints = Hint.objects.filter(challenge=challenge)
    
    # Get users who solved this challenge, sorted by newest first
    solvers = CustomeUser.objects.filter(
        solve__challenge=challenge
    ).annotate(
        solved_at= Max('solve__created_at')
    ).order_by('-solved_at')
    
    # Get total number of solves
    total_solves = challenge.solve_set.count()
    
    return render(request, 'challenges/challenge_details.html', {
        'category': category,
        'challenge': challenge,
        'solved': solved,
        'files': files,
        'unlocked_hints': unlocked_hints,
        'locked_hints': locked_hints,
        'solvers': solvers,
        'total_solves': total_solves,
    })


@login_required
@require_POST
def submit_flag(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    submitted_flag = request.POST.get('flag', '').strip()
    
    # Check if the user has already solved this challenge
    if Solve.objects.filter(user=request.user, challenge=challenge).exists():
        messages.warning(request, 'You have already solved this challenge!')
        return redirect('challenge_details', category_slug=challenge.category.slug, challenge_slug=challenge.title)
    
    # Check if the flag is correct
    if submitted_flag == challenge.flags:
        # Create a solve record
        Solve.objects.create(user=request.user, challenge=challenge)
        messages.success(request, 'Congratulations! You solved the challenge!')
    else:
        messages.error(request, 'Incorrect flag. Try again!')
    
    return redirect('challenge_details', category_slug=challenge.category.slug, challenge_slug=challenge.title)



@login_required
@require_POST
def unlock_hint(request, hint_id):
    hint = get_object_or_404(Hint, id=hint_id)
    challenge = hint.challenge
    
    # Check if the user has already unlocked this hint
    if HintUnlock.objects.filter(user=request.user, hint=hint).exists():
        messages.info(request, 'Hint already unlocked')
        return redirect('challenge_detail', category_slug=challenge.category.slug, challenge_slug=challenge.slug)
    
    # Check if the user has enough points to unlock the hint
    user_points = calculate_user_points(request.user)
    
    if user_points >= hint.cost:
        # Create a hint unlock record
        HintUnlock.objects.create(user=request.user, hint=hint)
        messages.success(request, f'Hint unlocked for {hint.cost} points')
    else:
        messages.error(request, f'Not enough points. You need {hint.cost} points to unlock this hint.')
    
    return redirect('challenge_details', category_slug=challenge.category.slug, challenge_slug=challenge.slug)


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

