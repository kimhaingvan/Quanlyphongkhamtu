from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from werkzeug.utils import redirect


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated
