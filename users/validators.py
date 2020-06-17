
def validate_file_extension(value):
    from django.core.exceptions import ValidationError
    import os

    #ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    path = os.path.splitext(value.name)[0].split('/')[0]  # [0] returns path+filename
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename

    valid_extensions = ['.pdf']
    if path == 'documents' :
        raise ValidationError('Please select a file.')
        
    elif not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file type.')


def user_directory_path(instance, filename):
    dir_name = str(instance.id)
    return '/'.join(['documents', dir_name, filename])

def directory_path_for_ref_letter(instance, filename):
    dir_name = str(instance.user.id)
    return '/'.join(['documents', dir_name, filename])

    