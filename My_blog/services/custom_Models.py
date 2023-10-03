from rest_framework.utils import model_meta


class CustomModel:
    def update(self, *args, **kwargs):
        info = model_meta.get_field_info(self)
        m2m_fields = []
        for attr, value in kwargs.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(self, attr, value)

        self.save()

        for attr, value in m2m_fields:
            field = getattr(self, attr)
            field.set(value)

        return self
