from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class HoaDonView(ModelView):
    can_edit = True
    column_display_pk = True
    can_view_details = True
    can_set_page_size = 50
    column_labels = dict(hoa_don_id="Mã hóa đơn", benh_nhan="Mã bệnh nhân", phieu_kham_benh_id="Mã phiếu khám bênh", tien_kham="Tiền khám", ngay_thanh_toan="Ngày thanh toán", tong_tien="Tổng tiền", ds_chi_tiet_hoa_don="Các chi tiết hóa đơn")

    column_exclude_list = ['detele_at', 'create_at', ]
    def is_accessible(self):
        return current_user.is_authenticated
