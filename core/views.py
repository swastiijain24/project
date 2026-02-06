from django.db.models import Count, Q
import random
from django.contrib import messages
from django.shortcuts import redirect, render
from core.models import Follow, LikePost, Post, Tag, User, Profile
from django.contrib import auth
from django.contrib.auth.decorators import login_required

@login_required(login_url='signin')
def home(request):
    userprofile=Profile.objects.get(user_id=request.user.pk)

    #custom feed by interest
    followed_user_ids = Follow.objects.filter(username=userprofile).values_list('followperson__user_id', flat=True)

    liked_posts_ids = list(LikePost.objects.filter(username=request.user.username).order_by('-liked_at').values_list('post_id', flat=True)[:50])
    liked_posts = Post.objects.filter(id__in=liked_posts_ids)
    #since there is a many to many rel btw tags and posts, post model has a tags field and related name is posts to tag model will refer as posts so filter all the (post, tag) where the post is in liked post and store unique ones means for each post, tag the post will be seen if it is there in liked posts if yes that tag corresponding to it is taken and stored uniquely
    interested_tags = Tag.objects.filter(posts__in=liked_posts).distinct()
    #removing users own posts and posts the user has already liked 
    user_recommendation_feed =  Post.objects.filter(
        profile_id__user_id__in=followed_user_ids
    ).exclude(
        profile_id=request.user.id
    ).exclude(
        id__in=liked_posts_ids
    ).annotate(
        tag_match_score=Count(
            'tags',
            filter=Q(tags__in=interested_tags),
            distinct=True
        )
    ).order_by('-tag_match_score','-created_at')

    suggested_users = Profile.objects.exclude(user_id__in=followed_user_ids).exclude(user_id=request.user.id)

    suggested_users = list(suggested_users)
    random.shuffle(suggested_users)

    context = {
        'userprofile':userprofile,
        'user_recommendation_feed':user_recommendation_feed,
        'final_sugg_list':suggested_users
    }

    return render(request, 'index.html', context)

def signUp(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
            return redirect('signup')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'username taken')
            return redirect('signup')
        elif password1!=password2:
            messages.info(request, 'passwords donot match')
            return redirect('signup')
        else:
            user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password1)
            user.save()

            newuser = User.objects.get(email=email)
            new_profile = Profile.objects.create(user_id=newuser)
            new_profile.save()

            return redirect('index')
    else:
        return render(request, 'signup.html')


def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logOut(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request, pk):
    profile = Profile.objects.get(user_id=pk)
    if request.method == 'POST':

        if request.FILES.get('profileimg'):
            profile.profileimg = request.FILES.get('profileimg')

        if request.FILES.get('bgimg'):
            profile.bgimg = request.FILES.get('bgimg')

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        bio = request.POST.get('bio')
        location = request.POST.get('location')
        workingat = request.POST.get('workingat')
        education = request.POST.get('education')

        user = profile.user_id
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        profile.bio = bio
        profile.location = location
        profile.workingat = workingat
        profile.education = education
        profile.save()
    return render(request, 'settings.html', {'profile':profile})

@login_required(login_url='signin')
def upload(request, pk):
    profile = Profile.objects.get(user_id=pk)
    if request.method == 'POST':
        if request.FILES.get('postimage'):
            image = request.FILES.get('postimage')
            caption = request.POST.get('caption')
            selected_tag_ids = request.POST.getlist('tags')
            post = Post.objects.create(profile_id=profile, image=image, caption=caption)
            post.tags.set(selected_tag_ids)
            post.save()
            return redirect('profile', pk=request.user.id)
    else:
        tags = Tag.objects.all()
        return render(request, 'upload.html', {'tags':tags})

@login_required(login_url='signin')
def profile(request, pk):
    user_obj = Profile.objects.get(user_id=request.user.id)
    profile = Profile.objects.get(user_id=pk)
    profile_posts = Post.objects.filter(profile_id=profile)
    profile_posts_count = profile_posts.count()

    is_following = Follow.objects.filter(username=user_obj , followperson=profile).exists()

    context={
        'profile':profile,
        'profile_posts':profile_posts,
        'profile_posts_count':profile_posts_count,
        'is_following': is_following
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def likepost(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
    else :
        like_filter.delete()
        post.no_of_likes -= 1
        post.save()
    return redirect('/')

@login_required(login_url='signin')
def follow(request):
    user_id=request.user.id
    followperson_id=int(request.GET.get('followperson_id'))

    user_obj = Profile.objects.get(user_id=user_id)
    followperson_obj= Profile.objects.get(user_id=followperson_id)

    follow_obj=Follow.objects.filter(username=user_obj, followperson=followperson_obj).first()

    if follow_obj == None:
        new_follow_obj = Follow.objects.create(username=user_obj, followperson=followperson_obj)
        user_obj.following_count += 1
        followperson_obj.follower_count += 1
        user_obj.save()
        followperson_obj.save()
    else:
        follow_obj.delete()
        user_obj.following_count -= 1
        followperson_obj.follower_count -= 1
        user_obj.save()
        followperson_obj.save()
    return redirect('profile', pk=followperson_id)