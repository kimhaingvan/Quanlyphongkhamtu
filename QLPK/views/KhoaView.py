from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class KhoaView(ModelView):
    can_edit = True
    column_display_pk = True
    can_view_details = True
    can_set_page_size = 50
    column_labels = dict(khoa_id="Mã khoa", ten_khoa="Tên khoa", mieu_ta="Miêu tả")

    column_exclude_list = ['detele_at', 'create_at', ]
    def is_accessible(self):
        return current_user.is_authenticated
