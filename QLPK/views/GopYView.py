from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class GopYView(ModelView):
    can_edit = True
    can_view_details = True
    can_set_page_size = 50
    column_labels = dict(gop_y_id = "Mã góp ý", ten_nguoi_gui ="Tên người gửi",email_nguoi_gui ="Email người gửi", tieu_de ="Tiêu đề" )

    def is_accessible(self):
        return current_user.is_authenticated
