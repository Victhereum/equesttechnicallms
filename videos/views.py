from django.shortcuts import render, get_object_or_404
from django.views import generic

from blog.forms import CommentForm
from videos.models import Videos


class VideoList(generic.ListView):
    queryset = Videos.objects.all().order_by('-created_on')
    context_object_name = 'videos'
    template_name = 'videos/video_index.html'
    paginate_by = 3



def video_detail(request, slug):
    template_name = 'videos/video_post_detail.html'
    post = get_object_or_404(Videos, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
