from django.shortcuts import get_object_or_404,render, redirect
from .forms import UserRegistration, UserLogin, CustomUserProfileForm
from .models import Category, Challenge, Solve, Hint, HintUnlock, ChallengeFile, CustomeUser
from django.db.models import Sum, Max
from django.contrib.auth import  login, logout

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse

from .prevent_brf import brute_force_protect


def home(request):
    context = {}
    return render(request, 'home.html', context)


def about(request):
    context = {}
    return render(request, 'about.html', context)




@login_required
def user_dashboard(request):

    user = request.user

    if request.method == 'POST':
        p_form = CustomUserProfileForm(request.POST, request.FILES, instance=user)
        if p_form.is_valid():
            p_form.save()
            return redirect('profile')

    else:
        p_form = CustomUserProfileForm(instance=user)

    if request.user.profile_image:
        profile_image = request.user.profile_image.url
    else:
        profile_image = None
    
    users_ranked = CustomeUser.objects.filter(points__gt=0).order_by('-points')
    user_rank = None
    for i, ranked_user in enumerate(users_ranked):
        if ranked_user.id == user.id:
            user_rank = i + 1
            break
    
    total_users_with_points = users_ranked.count()
    percentile = None
    
    if user_rank and total_users_with_points > 0:
        percentile = 100 - (user_rank / total_users_with_points * 100)
    
    #  Initialisation : 
    top_users = []
    rank = 1
    prev_points = None
    
    for i, top_user in enumerate(users_ranked[:5]): # for only the first 5 player 
        if prev_points is not None and top_user.points == prev_points:
            pass # Case when tow user have the same points
        else:
            rank = i + 1
        top_users.append({
            'rank': rank,
            'username': top_user.username,
            'points': top_user.points,
            'is_current_user': top_user.id == user.id
        })  
        prev_points = top_user.points
    
    context = {
        'user': user,
        'profile_image': profile_image,
        'user_rank': user_rank,
        'percentile': percentile,
        'total_users': CustomeUser.objects.count(),
        'top_users': top_users,
        'account_age_days': (user.date_joined.now().date() - user.date_joined.date()).days,
        'p_form' : p_form,
    }
    
    return render(request, 'profile.html', context)



def settings(request):
    user = request.user
    if request.method == 'POST':
        us_name = request.POST.get('username')
        email = request.POST.get('email')
        display_name = request.POST.get('display_name')
        bio = request.POST.get('bio')
        has_error = False

        if us_name and us_name != user.username:
            if CustomeUser.objects.filter(username=us_name).exclude(pk=user.pk).exists():
                messages.error(request, "This username is already taken.")
                has_error = True
            else:
                user.username = us_name

        if email and email != user.email:
            if CustomeUser.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, "This email is already taken.")
                has_error = True
            else:
                user.email = email

        if not has_error:
            if display_name:
                user.name = display_name
            if bio:
                user.bio = bio
            user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('settings')

    return render(request, 'settings.html')


def loginPage(request):
    if request.method == 'POST':
        form = UserLogin(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            form = UserLogin()
            url = reverse('home') + '#more-challenge'
            return redirect(url)
        else:
            messages.error(request, 'Invalide username or password.')
    else:
        form = UserLogin()

    Context = {'form' : form}
    return render(request, 'login.html', Context)


def logoutUser(request):
    logout(request)
    request.session.flush()
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            url = reverse('home') + '#more-challenge'
            return redirect(url)
        else:
            print(form.errors)
    else:
        form = UserRegistration()
   
    Context = {'form' : form}
    return render(request, 'signup.html', Context)




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
    challenge = get_object_or_404(Challenge, title=challenge_title)
    category = get_object_or_404(Category, name=category_name)
    solved = False
    if request.user.is_authenticated:
        solved = Solve.objects.filter(user=request.user, challenge=challenge).exists()

    files = ChallengeFile.objects.filter(challenge=challenge)

    unlocked_hints = []
    locked_hints = []
    
    if request.user.is_authenticated:
        unlocked_hints = Hint.objects.filter(
            challenge=challenge,
            hintunlock__user=request.user
        )

        locked_hints = Hint.objects.filter(
            challenge=challenge
        ).exclude(
            id__in=[hint.id for hint in unlocked_hints]
        )
    else:
        locked_hints = Hint.objects.filter(challenge=challenge)

    solvers = CustomeUser.objects.filter(
        solve__challenge=challenge
    ).annotate(
        solved_at=Max('solve__solved_at')  
    ).order_by('-solved_at')

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




@brute_force_protect # flag-cheking 
@require_POST
def submit_flag(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    submitted_flag = request.POST.get('flag', '').strip()
    category = Category.objects.get(id = challenge.categorie_id)

    if Solve.objects.filter(user=request.user, challenge=challenge).exists():
        messages.warning(request, 'You have already solved this challenge!')

    if submitted_flag == challenge.flags:
        request.user.points += challenge.point_val
        request.user.save()
        Solve.objects.create(user=request.user, challenge=challenge)
        messages.success(request, 'Congratulations! You solved the challenge!')
        
    
    response = redirect(reverse('challenge_details', args=[category.name, challenge.title]))
    messages.error(request, 'Incorrect flag. Try again!')
    request.session['flag_failed'] = True
    return response
    

    

@login_required
@require_POST
def unlock_hint(request, hint_id, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    hint = get_object_or_404(Hint, id=hint_id) 
    category = Category.objects.get(id = challenge.categorie_id)
    
    if HintUnlock.objects.filter(user=request.user, hint=hint).exists():
        messages.info(request, 'Hint already unlocked')
    
    HintUnlock.objects.create(user=request.user, hint=hint)
    messages.success(request, f'Hint unlocked')
        
    return redirect('challenge_details', category.name, challenge.title)
    


@login_required(login_url='login')
def leaderboard(request):
    users = CustomeUser.objects.filter(
        points__gt=0 
    ).order_by(
        '-points'  
    )
    ranked_users = []
    rank = 1
    prev_points = None
    
    for i, user in enumerate(users):
        if prev_points is not None and user.points == prev_points:
            pass
        else:
            rank = i + 1   
        ranked_users.append({
            'rank': rank,
            'username': user.username,
            'points': user.points,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined
        })
        
        prev_points = user.points
    
    return render(request, 'leaderboard.html', {
        'ranked_users': ranked_users
    })

