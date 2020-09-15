from flask_admin import BaseView, expose
from flask_login import current_user


class ThongKeView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/thongke.html")

    def is_accessible(self):
        return current_user.is_authenticated and current_user.chuc_vu_id == 2
