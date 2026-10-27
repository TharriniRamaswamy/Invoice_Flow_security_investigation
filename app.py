from flask import Flask, jsonify, request
app = Flask(__name__)
#Fictional data for an isolated local security demo
invoices = { 101:{"id":101,"owner_id":1,"customer":"Alice","amount":250},
            102:{"id":102,"owner_id":2,"customer":"Bob","amount":700}}

@app.route("/api/invoices/<int:invoice_id>")
def get_invoice(invoice_id):
    # Demo-only identity selector, NOT real authentication.
    user_id = request.args.get("demo_user", type=int)

    if user_id not in (1, 2):
        return jsonify({"error": "Unknown demo user"}), 400

    invoice = invoices.get(invoice_id)

    if invoice is None:
        return jsonify({"error": "Invoice not found"}), 404

    # Intentionally vulnerable: no ownership check.
    return jsonify(invoice)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)

