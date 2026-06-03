"""
Report view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from views.template_view import get_template
from controllers.order_controller import get_report_highest_spending_users, get_report_best_sellers

def show_highest_spending_users():
    """ Show report of highest spending users """
    users = get_report_highest_spending_users()
    rows = "".join([f"<li>Utilisateur {uid} : ${total:.2f}</li>" for uid, total in users])
    return get_template(f"<h2>Les plus gros acheteurs</h2><ul>{rows}</ul>")

def show_best_sellers():
    """ Show report of best selling products """
    products = get_report_best_sellers()
    rows = "".join([f"<li>Article {pid} : {qty} vendus</li>" for pid, qty in products])
    return get_template(f"<h2>Les articles les plus vendus</h2><ul>{rows}</ul>")