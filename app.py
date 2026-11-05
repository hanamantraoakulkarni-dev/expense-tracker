from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        expense_name = request.form.get("expense_name")
        amount = request.form.get("amount")

        if expense_name and amount:
            try:
                amount = int(amount)

                if amount > 0:
                    with open("expenses.txt", "a", encoding="utf-8") as file:
                        file.write(f"{expense_name.strip()}: ₹{amount}\n")

                    print("Expense saved successfully!")

            except ValueError:
                print("Please enter a valid amount!")
open("expenses.txt", "a", encoding="utf-8").close()
    expenses = []

    with open("expenses.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if ": ₹" not in line or line.startswith("Total: ₹"):
                continue

            name, amount = line.split(": ₹", 1)

            try:
                expenses.append({
                    "name": name,
                    "amount": int(amount)
                })
            except ValueError:
                continue

    # Calculate total expenses
    total = sum(expense["amount"] for expense in expenses)

    # Find largest expense
    largest_expense = max(
        expenses,
        key=lambda expense: expense["amount"]
    ) if expenses else None

    # Count expenses
    expense_count = len(expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        largest_expense=largest_expense,
        expense_count=expense_count
    )


@app.route("/remove/<int:expense_index>", methods=["POST"])
def remove_expense(expense_index):

    with open("expenses.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    expense_line_indices = []

    for i, line in enumerate(lines):
        line = line.strip()

        if ": ₹" not in line or line.startswith("Total: ₹"):
            continue

        name, amount = line.split(": ₹", 1)

        try:
            int(amount)
            expense_line_indices.append(i)
        except ValueError:
            continue

    if 0 <= expense_index < len(expense_line_indices):
        line_to_remove = expense_line_indices[expense_index]
        lines.pop(line_to_remove)

        with open("expenses.txt", "w", encoding="utf-8") as file:
            file.writelines(lines)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
