from django.forms.widgets import ClearableFileInput

class BootstrapClearableFileInput(ClearableFileInput):
    template_name = 'users/widgets/bootstrap_clearable_file_input.html'
