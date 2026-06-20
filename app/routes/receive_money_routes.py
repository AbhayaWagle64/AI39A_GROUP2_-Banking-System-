from flask import Blueprint, render_template, session, request, jsonify
from app.auth import login_required
from app.models.register_model import RegisterModel
from app.models.notification_model import NotificationModel

main = Blueprint("receive_money", __name__)
register_model = RegisterModel()
notification_model = NotificationModel()


@main.route("/receive-money")
@login_required
def receive_money():
    user_id = session.get("user_id")
    reg = register_model.find_by_username(user_id) or {}
    epaisa_id = reg.get("epaisa_id", "")
    full_name = reg.get("full_name", user_id)
    return render_template(
        "wallet/receive_money.html",
        epaisa_id=epaisa_id,
        full_name=full_name,
    )


@main.route("/api/request-money", methods=["POST"])
@login_required
def request_money():
    data = request.get_json(silent=True) or {}
    from_epaisa = (data.get("from_epaisa") or "").strip()
    amount = data.get("amount")

    if not from_epaisa or not amount:
        return jsonify({"success": False, "message": "Recipient and amount are required."}), 400

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid amount."}), 400

    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be greater than 0."}), 400

    payer = register_model.find_by_epaisa_id(from_epaisa)
    if not payer:
        return jsonify({"success": False, "message": "No user found with that ePaisa ID."}), 404

    requester = register_model.find_by_username(session.get("user_id")) or {}
    notification_model.create(
        payer["username"], "Money Request",
        f"{requester.get('full_name', 'A user')} requested Rs. {amount:.2f} from you.",
        "info"
    )
    return jsonify({"success": True, "message": "Money request sent successfully."}), 200
