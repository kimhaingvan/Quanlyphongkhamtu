from flask_admin import BaseView, expose
from flask_login import current_user

from QLPK import dao


class RegisterView(BaseView):
    @expose("/")
    def index(self):
        cac_chuc_vu = dao.LayTatCaChucVu()
        print(cac_chuc_vu)
        return self.render("admin/register.html", cac_chuc_vu = cac_chuc_vu)

    def is_accessible(self):
        return not current_user.is_authenticated
