"""Manage pharmacy inventory, prescriptions, and stock reports."""

import hashlib
import hmac
import json
import secrets
from datetime import date, datetime
from pathlib import Path
import ast
import operator
import os

# Global pharmacy state
medicines = {}


def add_medicine(
    name,
    qty=0,
    price=0.0,
    expiry="2099-12-31",
    audit=None,
):
    """Add medicine stock and record the transaction."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Medicine name must be a non-empty string.")

    if qty < 0:
        raise ValueError("Quantity cannot be negative.")

    if price < 0:
        raise ValueError("Price cannot be negative.")

    if audit is None:
        audit = []

    if name not in medicines:
        medicines[name] = {
            "qty": 0,
            "price": price,
            "expiry": expiry,
        }

    medicines[name]["qty"] += qty
    audit.append(
        f"{datetime.now()}: Stocked {qty} units of {name}"
    )
    return audit


def dispense_medicine(name, qty):
    """Dispense medicine when sufficient stock is available."""
    if qty <= 0:
        raise ValueError("Dispense quantity must be positive.")

    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")

    if medicines[name]["qty"] < qty:
        raise ValueError("Insufficient stock.")

    medicines[name]["qty"] -= qty

    if medicines[name]["qty"] == 0:
        del medicines[name]


def get_quantity(name):
    """Return the available quantity of a medicine."""
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")
    return medicines[name]["qty"]


def is_expired(name):
    """Check whether a medicine has expired."""
    if name not in medicines:
        raise KeyError(f"Medicine not found: {name}")

    expiry_date = datetime.strptime(
        medicines[name]["expiry"], "%Y-%m-%d"
    ).date()
    return expiry_date < date.today()


def bill_amount(prescription):
    """Calculate the total price for prescription items."""
    total = 0.0

    for name, quantity in prescription:
        if name not in medicines:
            raise KeyError(f"Medicine not found: {name}")
        if quantity <= 0:
            raise ValueError("Prescription quantities must be positive.")

        total += medicines[name]["price"] * quantity

    return total


def calculate_dosage(formula):
    """Calculate dosage using a restricted arithmetic expression."""

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            return operators[type(node.op)](
                evaluate(node.left), evaluate(node.right)
            )
        if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)
        ):
            value = evaluate(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        raise ValueError("Unsupported dosage expression.")

    expression = ast.parse(formula, mode="eval")
    result = evaluate(expression)

    if not isinstance(result, (int, float)):
        raise ValueError("Dosage result must be numeric.")
    return result


def patient_id(name, phone):
    """Create a SHA-256 identifier for a patient."""
    value = f"{name}{phone}".encode("utf-8")
    return hashlib.sha256(value).hexdigest()


def generate_rx_number():
    """Generate a hard-to-guess prescription reference."""
    return f"RX-{secrets.randbelow(900000) + 100000}"


def save_stock(file="pharmacy.json"):
    """Save medicine stock as JSON."""
    path = Path(file)
    with path.open("w", encoding="utf-8") as stock_file:
        json.dump(medicines, stock_file, indent=4)


def load_stock(file="pharmacy.json"):
    """Load validated stock data into the inventory."""
    path = Path(file)

    with path.open("r", encoding="utf-8") as stock_file:
        loaded_medicines = json.load(stock_file)

    if not isinstance(loaded_medicines, dict):
        raise ValueError("Invalid stock data.")

    medicines.clear()
    medicines.update(loaded_medicines)


def print_label(name):
    """Display a medicine label without invoking a shell."""
    print(f"Dispensing label: {name}")


def expiring_soon(days=30):
    """Return medicines expiring within the next specified days."""
    if days < 0:
        raise ValueError("Days cannot be negative.")

    today = date.today()
    result = []

    for name, medicine in medicines.items():
        expiry_date = datetime.strptime(
            medicine["expiry"], "%Y-%m-%d"
        ).date()

        if today <= expiry_date <= today.fromordinal(
            today.toordinal() + days
        ):
            result.append(name)

    return result


def pharmacist_login(password):
    """Authenticate using a password configured in the environment."""
    configured_password = os.environ.get("PHARMACY_DB_PASSWORD")

    if not configured_password:
        return False

    return hmac.compare_digest(password, configured_password)


def print_stock():
    """Print all medicine stock details."""
    print("===== Pharmacy Stock Report =====")

    for name, medicine in medicines.items():
        print(
            f"{name} -> {medicine['qty']} units, "
            f"Rs. {medicine['price']}, exp {medicine['expiry']}"
        )


def main():
    """Run a demonstration of the pharmacy manager."""
    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2027-12-15")
    add_medicine("Cetirizine 10mg", 10, 2.0, "2027-03-31")

    dispense_medicine("Paracetamol 500mg", 30)

    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))

    prescription = [
        ("Paracetamol 500mg", 10),
        ("Amoxicillin 250mg", 5),
    ]
    print("Bill:", bill_amount(prescription))
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print(
        "Login:",
        pharmacist_login(os.environ.get("PHARMACY_DB_PASSWORD", "")),
    )

    print_label("Paracetamol 500mg")
    save_stock()
    load_stock()
    print_stock()
    print("Expiring soon:", expiring_soon())


if __name__ == "__main__":
    main()
