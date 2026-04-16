import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.activity import Activity
from app.models.participant import Participant
from app.models.draw_result import DrawResult

activity_bp = Blueprint('activity', __name__)

# 判斷是否登入的輔助函式
def is_logged_in():
    return 'admin_id' in session

@activity_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """管理員總覽頁面"""
    if not is_logged_in():
        flash('請先登入', 'warning')
        return redirect(url_for('auth.login'))
        
    activities = Activity.get_all()
    return render_template('activity/dashboard.html', activities=activities)

@activity_bp.route('/activity/create', methods=['GET', 'POST'])
def create_activity():
    """建立新活動"""
    if not is_logged_in():
        flash('請先登入', 'warning')
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        
        if not name:
            flash('請輸入活動名稱', 'danger')
            return redirect(url_for('activity.create_activity'))
            
        activity_id = Activity.create(name, description)
        if activity_id:
            flash('活動建立成功！', 'success')
            return redirect(url_for('activity.activity_detail', id=activity_id))
        else:
            flash('活動建立失敗，系統發生錯誤。', 'danger')
            return redirect(url_for('activity.create_activity'))
            
    return render_template('activity/create.html')

@activity_bp.route('/activity/<int:id>', methods=['GET'])
def activity_detail(id):
    """活動詳情與管理名單頁面"""
    if not is_logged_in():
        flash('請先登入', 'warning')
        return redirect(url_for('auth.login'))
        
    activity = Activity.get_by_id(id)
    if not activity:
        flash('找不到該活動', 'danger')
        return redirect(url_for('activity.dashboard'))
        
    participants = Participant.get_by_activity_id(id)
    return render_template('activity/detail.html', activity=activity, participants=participants)

@activity_bp.route('/activity/<int:id>/participants', methods=['POST'])
def add_participants(id):
    """批次或單獨新增參加者"""
    if not is_logged_in():
        return redirect(url_for('auth.login'))
        
    # 可支援用逗號或換行分隔名單
    participant_names = request.form.get('participant_names', '')
    if not participant_names.strip():
        flash('請輸入參加者名單！', 'warning')
        return redirect(url_for('activity.activity_detail', id=id))
        
    # 分割名單字串，支援換行與逗號
    raw_names = participant_names.replace(',', '\n').split('\n')
    names = [name.strip() for name in raw_names if name.strip()]
    
    count = 0
    for name in names:
        if Participant.create(id, name):
            count += 1
            
    flash(f'成功加入了 {count} 位參加者。', 'success')
    return redirect(url_for('activity.activity_detail', id=id))

@activity_bp.route('/activity/<int:activity_id>/participants/<int:participant_id>/delete', methods=['POST'])
def delete_participant(activity_id, participant_id):
    """刪除參加者"""
    if not is_logged_in():
        return redirect(url_for('auth.login'))
        
    if Participant.delete(participant_id):
        flash('參加者已成功刪除。', 'info')
    else:
        flash('刪除參加者失敗。', 'danger')
        
    return redirect(url_for('activity.activity_detail', id=activity_id))

@activity_bp.route('/activity/<int:id>/draw', methods=['POST'])
def draw_prize(id):
    """執行抽籤動作"""
    if not is_logged_in():
        return redirect(url_for('auth.login'))
        
    prize_name = request.form.get('prize_name')
    draw_count_str = request.form.get('draw_count', '1')
    
    if not prize_name:
        flash('請輸入獎項名稱', 'danger')
        return redirect(url_for('activity.activity_detail', id=id))
        
    try:
        draw_count = int(draw_count_str)
        if draw_count <= 0:
            raise ValueError()
    except ValueError:
        flash('抽出數量必須是有效的正整數', 'danger')
        return redirect(url_for('activity.activity_detail', id=id))
        
    eligible = Participant.get_eligible_participants(id)
    
    if len(eligible) < draw_count:
        flash(f'目前未中獎の參加人數 ({len(eligible)}) 不足欲抽出的數量 ({draw_count})', 'warning')
        return redirect(url_for('activity.activity_detail', id=id))
        
    # Python random.sample 取出不重複名單
    winners = random.sample(eligible, draw_count)
    for winner in winners:
        DrawResult.create(id, winner['id'], prize_name)
        
    flash(f'恭喜抽出 {draw_count} 位得獎者！獎項：{prize_name}', 'success')
    return redirect(url_for('activity.activity_results', id=id))

@activity_bp.route('/activity/<int:id>/results', methods=['GET'])
def activity_results(id):
    """公開檢視特定活動的中獎紀錄清單"""
    activity = Activity.get_by_id(id)
    if not activity:
        flash('找不到該活動', 'danger')
        # 由於公開頁面，如果出錯導回登入頁較安全
        return redirect(url_for('auth.login')) 
        
    results = DrawResult.get_by_activity_id(id)
    return render_template('activity/results.html', activity=activity, results=results)
