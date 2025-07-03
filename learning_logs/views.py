from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm

# Create your views here.
def index(request):
    """The home page for learning_log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    # Filter topics to only show those created by the logged-in user
    context = {'topics' : topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    # Ensure the topic belongs to the logged-in user
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('date_added')
    context = {'topic' : topic, 'entries' : entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user  # Set the owner to the logged-in user
            new_topic.save()
            # Redirect to the topics page after saving the new topic
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)
    # Ensure the topic belongs to the logged-in user
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # No data submitted; create a blank form
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic  # Associate the entry with the topic
            new_entry.save()
            # Redirect to the topic page after saving the new entry
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Ensure the topic belongs to the logged-in user
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry data
        form = TopicForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            # Redirect to the topic page after saving the edited entry
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'form': form, 'topic': topic}
    return render(request, 'learning_logs/edit_entry.html', context)
