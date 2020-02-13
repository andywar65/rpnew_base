from django.forms.widgets import ClearableFileInput

class SmallClearableFileInput(ClearableFileInput):
    template_name = 'users/widgets/bootstrap_clearable_file_input.html'
