from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Movie,Review, Score
from .forms import ReviewForm, ScoreForm

# simil 함수 유저가 준 점수 평균
def simil(u1, u2):
    movies = movies.objects.all()
    S, S_u1, S_u2 =0,0,0
    for movie in movies:
        if u1 in movie.rate_users.all() and u2 in movie.rate_users.all():
            r1 = Score.objects.filter(movie_id = movie.id, user_id =u1.id)[0].score
            r2 = Score.objects.filter(movie_id = movie.id, user_id =u2.id)[0].score
            S += (r1-u1.rate)*(r2-u2.rate)
            S_u1 += (r1-u1.rate)**2
            S_u2 += (r2-u2.rate)**2
    try:
        return S/((S_u1**0.5)*(S_u2**0.5))
    except:
        return 0

# rating 함수
def rating(movie, user, cmp_users):
    S,abs_S = 0,0 
    for cmp_user in cmp_users:
        if cmp_user in movies.rate_user.all(): continue
        result = simil(user,cmp_user)
        r = Score.objects.filter(movie_id = movie.id, user_id = cmp_user.id)[0].score
        S += (result)*(r-cmp_user.rate)
        abs_S += abs(result)
    try:
        return user.rate + S/abs_S
    except:
        return user.rate

def solve(user):
    users = User.objects.all()
    movies = Movie.objects.all()
    tmps = []
    cmp_users = []
    for tmp in users:
        if user == tmp: continue
        cmp_users.append((simil(user, tmp), tmp))
    cmp_users.sort(reverse=True)
    for i in range(5):
        tmp.append(cmp_users[i][1])
    cmp_movies = []
    for movie in movies:
        if movie in user.rate_movies.all(): continue
        cmp_movies.append((rating(movie,user,tmp),movie))
    cmp_movies.sort(reverse=True)
    recommend = []
    for i in range(5):
        recommend.append(cmp_movies[i][1])
    return recommend

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    user = request.user 
    recommend = []
    if request.user.is_authenticated and len(user.rate_movies.all())>10:
        recommend = solve(user)
    else:
        for movie in movies:
            if request.user.is_authenticated and movie in user.rate_movies.all(): continue
            S,cnt = 0,0
            for tmp in movie.rate_users.all():
                cnt+=1
                S+=Score.objects.filter(movie_id = movie.id, user_id = request.user.id)[0].score
            try:
                recommend.append((S/cnt,movie))
            except:
                recommend.append((0,movie))
        recommend.sort(key=lambda x: x[0],reverse=True)
        reco = []
        for i in range(5):
            reco.append(recommend[i][1])
        recommend = reco
    context = {
        'movies' : movies,
        'recommend' : recommend
    }
    print(movies)
    print(recommend)
    return render(request,"movies/index.html",context)

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    review_form = ReviewForm()
    score_form = ScoreForm()
    reviews = Review.objects.filter(movie_id=movie_id)
    scores = Score.objects.filter(movie_id=movie_id)
    try:
        review_avg = sum(map(lambda x: x.score,reviews))/len(reviews)
    except:
        review_avg = 0
    # print(reviews)        
    # print(review_sum)
    context = {
        'movie' : movie,
        'review_form' : review_form,
        'review_avg' : review_avg,
        'score_form' : score_form,
        'scores' : scores
    }
    return render(request, "movies/detail.html", context)

@require_POST
def review_new(request,movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie,pk=movie_id)
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            form = review_form.save(commit=False)
            form.user = request.user
            form.movie = movie
            form.save()
            return redirect('movies:detail',movie_id)
        else:
            messages.info(request,'0~5사이의 값을 입력하세요')
            return redirect('movies:detail',movie_id)
    else:
        return redirect('accounts:login')
@require_POST
def review_delete(request, movie_id,review_id):
    review = get_object_or_404(Review,pk=review_id)
    review.delete()
    return redirect('movies:detail',movie_id)

@require_POST
def like(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user
    if user.is_authenticated:
        if user in movie.like_users.all():
            movie.like_users.remove(user)
        else:
            movie.like_users.add(user)
        return redirect('movies:detail',movie_id)
    else:
        return redirect('accounts:login') 

@require_POST
def score(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    user = request.user
    if user.is_authenticated:
        score_form = ScoreForm(request.POST)
        if score_form.is_valid():
            score = Score.objects.filter(movie_id = movie_id, user_id = request.user.id)
            score.delete()
            score_form = ScoreForm(request.POST)
            form = score_form.save(commit=False)
            form.user = request.user
            form.movie = movie
            form.save()
            S = 0
            cnt = 0
            for movie in user.rate_movies.all():
                cnt+=1
                S += Score.objects.filter(movie_id = movie.id, user_id = request.user.id)[0].score
            try:
                user.rate = S/cnt
            except:
                user.rate = 0
            user.save()
            return redirect('movies:detail',movie_id)
    else:
        return redirect('accounts:login') 