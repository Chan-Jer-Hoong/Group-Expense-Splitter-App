class Expense:

    def __init__(self):
        self.total_expense = 0.00
        self.auto_split_amount = 0.00

    # Methods
    def auto_split(self, total_members) -> float:
        if self.get_auto_split_amount() > 0:
            return round(self.get_total_expense() / total_members, 2)
        else:
            return 0.00

    # Setter
    def set_total_expense(self, amount : float):
        self.total_expense = round(amount, 2)
    
    def set_auto_split_amount(self, amount : float):
        self.auto_split_amount = amount

    # Getter
    def get_total_expense(self) -> float:
        return self.total_expense
    
    def get_auto_split_amount(self) -> float:
        return self.auto_split_amount