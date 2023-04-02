from django.views import generic
from .models import ToDoList, ToDoItem
from django.urls import reverse, reverse_lazy

class ListListView(generic.ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

class ListItemView(generic.ListView):
    model = ToDoItem
    template_name = 'todo_app/todo_list.html'

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs['list_id'])

    def get_context_data(self):
        context = super().get_context_data()
        context['todo_list'] =ToDoList.objects.get(id=self.kwargs['list_id'])
        return context

class ListCreate(generic.CreateView):
    model = ToDoList
    fields = ['title']
    template_name = 'todo_app/todolist_form.html'

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context['title'] = "Add new list"
        return context

class ItemCreate(generic.CreateView):
    model = ToDoItem
    fields = [
        'todo_list',
        'title',
        'description',
        'due_date',
    ]
    template_name = 'todo_app/todoitem_form.html'

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        initial_data['todo_list'] = todo_list
        return initial_data

    def get_context_data(self):
        context = super(ItemCreate, self).get_context_data()
        todo_list = ToDoList.objects.get(id=self.kwargs['list_id'])
        context['todo_list'] = todo_list
        context['title'] = "Add new item"
        return context

    def get_success_url(self) -> str:
        return reverse('list', args=[self.object.todo_list_id])

class ItemUpdate(generic.UpdateView):
    model = ToDoItem
    template_name = 'todo_app/todoitem_form.html'
    fields = [
        'todo_list', 
        'title',
        'description',
        'due_date',
    ]

    def get_context_data(self):
        context = super(ItemUpdate, self).get_context_data()
        context['todo_list'] = self.object.todo_list
        context['title'] = 'Edit item'
        return context

    def get_success_url(self) -> str:
        return reverse('list', args=[self.object.todo_list_id])

class ListDelete(generic.DeleteView):
    model = ToDoList
    template_name = "todo_app/todolist_confirm_delete.html"
    success_url = reverse_lazy("index")

class ItemDelete(generic.DeleteView):
    model = ToDoItem
    template_name = "todo_app/todoitem_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context