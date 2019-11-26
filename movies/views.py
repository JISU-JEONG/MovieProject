from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Movie,Review, Score, Genre
from .forms import ReviewForm, ScoreForm
from accounts.models import User


flag = 0
movie_list_1 = []
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
        tmps.append(cmp_users[i][1])
    cmp_movies = []
    for movie in movies:
        if movie in user.rate_movies.all(): continue
        cmp_movies.append((rating(movie,user,tmps),movie))
    cmp_movies.sort(reverse=True)
    recommend = []
    for i in range(5):
        recommend.append(cmp_movies[i][1])
    return recommend
# Create your views here.
def index(request):
    movies = Movie.objects.all()
    user = request.user
    genres = Genre.objects.all()
    recommend = []
    global movie_list_1
    global flag
    if flag:
        movie_list = movie_list_1
    elif not flag:
        movie_list = [[] for _ in range(18)]
        for movie in movies:
            if movie.genres.all().filter(pk=28) and len(movie_list[0])<20:
                movie_list[0].append(movie)
            if movie.genres.all().filter(pk=12) and len(movie_list[1])<20:
                movie_list[1].append(movie)
            if movie.genres.all().filter(pk=16) and len(movie_list[2])<20:
                movie_list[2].append(movie)
            if movie.genres.all().filter(pk=35) and len(movie_list[3])<20:
                movie_list[3].append(movie)
            if movie.genres.all().filter(pk=80) and len(movie_list[4])<20:
                movie_list[4].append(movie)
            if movie.genres.all().filter(pk=99) and len(movie_list[5])<20:
                movie_list[5].append(movie)
            if movie.genres.all().filter(pk=18) and len(movie_list[6])<20:
                movie_list[6].append(movie)
            if movie.genres.all().filter(pk=10751) and len(movie_list[7])<20:
                movie_list[7].append(movie)
            if movie.genres.all().filter(pk=14) and len(movie_list[8])<20:
                movie_list[8].append(movie)
            if movie.genres.all().filter(pk=36) and len(movie_list[9])<20:
                movie_list[9].append(movie)
            if movie.genres.all().filter(pk=27) and len(movie_list[10])<20:
                movie_list[10].append(movie)
            if movie.genres.all().filter(pk=10402) and len(movie_list[11])<20:
                movie_list[11].append(movie)
            if movie.genres.all().filter(pk=9648) and len(movie_list[12])<20:
                movie_list[12].append(movie)
            if movie.genres.all().filter(pk=10749) and len(movie_list[13])<20:
                movie_list[13].append(movie)
            if movie.genres.all().filter(pk=878) and len(movie_list[14])<20:
                movie_list[14].append(movie)
            if movie.genres.all().filter(pk=53) and len(movie_list[15])<20:
                movie_list[15].append(movie)
            if movie.genres.all().filter(pk=10752) and len(movie_list[16])<20:
                movie_list[16].append(movie)
            if movie.genres.all().filter(pk=37) and len(movie_list[17])<20:
                movie_list[17].append(movie)
            flag = 1
            movie_list_1 = movie_list
    if request.user.is_authenticated and len(user.rate_movies.all())>10:
        recommend = solve(user)
    else:
        for movie in movies:
            if request.user.is_authenticated and movie in user.rate_movies.all(): continue
            S,cnt = 0,0
            for tmp in movie.rate_users.all():
                cnt+=1
                S+=Score.objects.filter(movie_id = movie.id, user_id = tmp.id)[0].score
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
        'recommend' : recommend,
        'genres' : genres,
        'actions' : movie_list[0],
        'advs' : movie_list[1],
        'anis' : movie_list[2],
        'comis' : movie_list[3],
        'guls' : movie_list[4],
        'docus' : movie_list[5],
        'dramas' : movie_list[6],
        'fams' : movie_list[7],
        'fans' : movie_list[8],
        'his' : movie_list[9],
        'afrs' : movie_list[10],
        'musics' : movie_list[11],
        'mis' : movie_list[12],
        'romans' : movie_list[13],
        'SFs' : movie_list[14],
        'thrils' : movie_list[15],
        'wars' : movie_list[16],
        'wests' : movie_list[17],
    }
    return render(request,"movies/index.html",context)

def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    review_form = ReviewForm()
    score_form = ScoreForm()
    reviews = Review.objects.filter(movie_id=movie_id)
    scores = Score.objects.filter(movie_id=movie_id)
    if request.user.is_authenticated:
        if request.user in movie.rate_users.all():
            score = scores.filter(user_id=request.user.id)[0].score
        else:
            score = 0
    else:
        score = 0
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
        'scores' : scores,
        'myscore' : score
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

def search(request):
    movies = Movie.objects.all()
    users = User.objects.all()
    genres = Genre.objects.all()
    movies_list = []
    users_list = []
    genres_list = []
    g_pk = 0
    search = request.GET.get("search")
    print(search)
    for genre in genres:
        if search in genre.name:
            g_pk = genre.pk
            break
    for movie in movies:
        if search in movie.title:
            movies_list.append(movie)
        if movie.genres.all().filter(pk=g_pk):
            genres_list.append(movie)
    for user in users:
        if search in user.username:
            users_list.append(user)
    context = {
        "movies" : movies_list,
        "users" : users_list,
        "genres" : genres_list 
    }
    print("들어왔당")
    return render(request, 'movies/search.html', context)