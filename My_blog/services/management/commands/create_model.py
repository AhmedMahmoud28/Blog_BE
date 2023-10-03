import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def create_model(self):
        with open(f"{self.project_path}/{self.app_name}/models.py", "a") as f:
            f.write(
                f"""
class {self.model_name}(models.Model):
    #relations

    #fields

    def __str__(self):
        return self.pk
"""
            )

    def register_admin(self):
        with open(f"{self.project_path}/{self.app_name}/admin.py", "a") as f:
            f.write(
                f"""
@admin.register(models.{self.model_name})
class {self.model_name}Admin(admin.ModelAdmin):
    "Admin View for {self.model_name}"

"""
            )

    def create_view(self):
        with open(f"{self.project_path}/{self.app_name}/views.py", "a") as f:
            f.write(
                f"""
class {self.model_name}ViewSet(viewsets.ModelViewSet):
    queryset = models.{self.model_name}.objects.all()
    serializer_class = serializers.{self.model_name}Serializer
    # filterset_class = filter.{self.model_name}Filter
    # search_fields = ['']
    # filterset_fields = ['']
"""
            )

    def create_serializer(self):
        with open(f"{self.project_path}/{self.app_name}/serializers.py", "a") as f:
            f.write(
                f"""
class {self.model_name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.{self.model_name}
        fields = '__all__'
"""
            )

    def add_view_path(self):
        target_text = "urlpatterns = ["
        new_text = f"router.register('{self.url_path}',views.{self.model_name}ViewSet)"
        file_path = f"{self.project_path}/{self.app_name}/urls.py"
        with open(file_path, "r") as f:
            lines = f.readlines()

        with open(file_path, "w") as f:
            for line in lines:
                if target_text in line:
                    f.write(new_text + "\n")
                f.write(line)

    def handle(self, *args, **options):
        self.project_path = os.path.join(os.getcwd(), "business_meal")

        self.app_name = input("Give me the app name ")
        self.model_name = input("Give me the model name ")
        is_admin_register = input(
            "Do you want to register this model in the admin [Y/n]"
        )
        is_create_view = input("Do you want to create view to this model [Y/n]")

        self.create_model()
        if is_admin_register not in ["N", "n", "no"]:
            self.register_admin()
        if is_create_view not in ["N", "n", "no"]:
            self.url_path = input("Give me url path ")

            self.create_view()
            self.create_serializer()
            self.add_view_path()
