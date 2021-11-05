from flask_admin.contrib.sqla import ModelView
from flask_admin import expose

class ChatBotModelView(ModelView):
    def create_view(self):
        return super().create_view()


    def edit_view(self):
        return super().edit_view()