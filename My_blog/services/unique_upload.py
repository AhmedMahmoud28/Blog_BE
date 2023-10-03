from unique_upload import unique_upload


def file_upload(folder_name, instance, filename):
    return "%s/%s" % (folder_name, unique_upload(instance, filename))
