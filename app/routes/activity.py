from flask import Blueprint

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    GET: 取得目前所有的 Activity 並顯示於管理員總攬頁面。需檢查 Session 確認權限。
    """
    pass

@activity_bp.route('/activity/create', methods=['GET', 'POST'])
def create_activity():
    """
    GET: 顯示新建活動表單。
    POST: 接收表單位名稱與描述，將新活動寫回 DB 並重導向至列表或該活動頁面。
    """
    pass

@activity_bp.route('/activity/<int:id>', methods=['GET'])
def activity_detail(id):
    """
    GET: 回傳該活動的基本資訊與目前參與者列表，供管理員預覽名單並決定是否執行抽獎。
    若找不到活動回傳 404 錯誤。
    """
    pass

@activity_bp.route('/activity/<int:id>/participants', methods=['POST'])
def add_participants(id):
    """
    POST: 接收逗號分隔的名單字串或表單資料，批次或單純寫入 Participants 表格中。處理完重導向至活動詳細頁。
    """
    pass

@activity_bp.route('/activity/<int:activity_id>/participants/<int:participant_id>/delete', methods=['POST'])
def delete_participant(activity_id, participant_id):
    """
    POST: 給定參與者 ID，從資料庫中將其刪除以做防呆。處理完重導向至活動詳細頁。
    """
    pass

@activity_bp.route('/activity/<int:id>/draw', methods=['POST'])
def draw_prize(id):
    """
    POST: 重頭戲。接收獎項名稱與數量，從尚未中獎(is_winner=0)參與者候選名單中，
    運用 Python random 模組隨機抽取出指定數量的人。
    將資訊寫入 DrawResult，更新中獎參與者的狀態，成功後進入結果頁面。
    """
    pass

@activity_bp.route('/activity/<int:id>/results', methods=['GET'])
def activity_results(id):
    """
    GET: 查詢該活動所有的中獎結果名單 (DrawResult) 顯示在公佈欄上，不需要驗證管理員身分。
    """
    pass
