# 1. Make sure you import your new functions at the top of __init__.py along with the others
from app.controllers.profile_controller import (
    show_profile, 
    show_edit_profile, 
    get_user_profile_data, 
    update_user_profile_data
)
# 2. Add these two routes right below the frontend page views
@app.route('/api/profile', methods=['GET'])
def api_get_profile():
    """URL path that the frontend fetches to get profile info"""
    response, status_code = get_user_profile_data()
    return response, status_code

@app.route('/api/profile/update', methods=['POST'])
def api_update_profile():
    """URL path that the frontend posts to when hitting 'Save'"""
    response, status_code = update_user_profile_data()
    return response, status_code