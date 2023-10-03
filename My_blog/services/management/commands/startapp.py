import os

from django.core.management.base import CommandError
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    def add_app_to_installed_apps(self, app_name, dict, project_name):
        settings_location = f"{dict}/settings/base.py"
        old_settings = open(settings_location, "r")
        old_settings = old_settings.readlines()
        new_settings = open(settings_location, "w")
        for line in old_settings:
            if line == "LOCAL_APPS = [\n":
                line = line + f"    '{project_name}.{app_name}',\n"
            new_settings.write(line)

    def add_app_urls_to_main_urls(self, app_name, dict, project_name):
        urls_location = f"{dict}/urls.py"
        old_urls = open(urls_location, "r")
        old_urls = old_urls.readlines()
        new_urls = open(urls_location, "w")
        for line in old_urls:
            if line == '    path("admin/", admin.site.urls),\n':
                line = (
                    line
                    + f'    path("api/", include("{project_name}.{app_name}.urls")),\n'
                )
            new_urls.write(line)

    help = (
        "Creates a Django app directory structure for the given app name in "
        "the current directory or optionally in the given directory."
    )
    missing_args_message = "You must provide an application name."

    def handle(self, **options):
        options["template"] = os.path.join(os.getcwd(), "app_template")
        app_name = options.pop("name")
        target = options.pop("directory")
        if target is None:
            project_name = "My_blog"
            project_dict = os.path.join(os.getcwd(), project_name)
            top_dir = os.path.join(os.getcwd(), project_name, app_name)
            try:
                os.makedirs(top_dir)
            except FileExistsError:
                raise CommandError("'%s' already exists" % top_dir)
            except OSError as e:
                raise CommandError(e)
            self.add_app_to_installed_apps(app_name, project_dict, project_name)
            self.add_app_urls_to_main_urls(app_name, project_dict, project_name)
        super().handle("app", app_name, top_dir, **options)
