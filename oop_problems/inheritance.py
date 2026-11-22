"""OOP Problems - Inheritance.

Exercises from the course gist "OOP Problems" (B. Dallard, AIDAMS 2A).
Run: python inheritance.py
"""


# ---------------------------------------------------------------------------
# Problem 1: Vehicle, Car, Bicycle
# ---------------------------------------------------------------------------
class Vehicle:
    def drive(self):
        return "Driving a vehicle"


class Car(Vehicle):
    def drive(self):
        return "Driving a car"


class Bicycle(Vehicle):
    def drive(self):
        return "Riding a bicycle"


# ---------------------------------------------------------------------------
# Problem 2: Person, Student, Employee
# ---------------------------------------------------------------------------
class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age}, from {self.address}."


class Student(Person):
    def __init__(self, name, age, address, field_of_study):
        super().__init__(name, age, address)
        self.field_of_study = field_of_study

    def introduce(self):
        return super().introduce() + f" I study {self.field_of_study}."


class Employee(Person):
    def __init__(self, name, age, address, company):
        super().__init__(name, age, address)
        self.company = company

    def introduce(self):
        return super().introduce() + f" I work at {self.company}."


# ---------------------------------------------------------------------------
# Problem 3: BankAccount and SavingsAccount
# ---------------------------------------------------------------------------
class BankAccount:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount

    def transfer(self, destination_account, amount):
        """Return False if the balance is not enough, True otherwise."""
        if amount > self.balance:
            return False
        self.withdraw(amount)
        destination_account.deposit(amount)
        return True


class SavingsAccount(BankAccount):
    def __init__(self, account_number, balance=0, interest_rate=0.02):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        super().deposit(interest)

    def check_balance(self):
        return self.balance


if __name__ == "__main__":
    # Problem 1
    results = [v.drive() for v in (Vehicle(), Car(), Bicycle())]
    assert results == ["Driving a vehicle", "Driving a car", "Riding a bicycle"]
    print("P1:", results)

    # Problem 2
    people = [Person("Ana", 40, "Lyon"),
              Student("Victoire", 19, "Paris", "AI"),
              Employee("Bo", 30, "Lille", "Thales")]
    for p in people:
        print("P2:", p.introduce())

    # Problem 3
    s1 = SavingsAccount("FR-001", 1000, 0.05)
    s2 = SavingsAccount("FR-002", 200)
    s1.add_interest()
    assert s1.check_balance() == 1050
    assert s1.transfer(s2, 300) is True
    assert (s1.check_balance(), s2.check_balance()) == (750, 500)
    assert s2.transfer(s1, 10_000) is False
    print("P3:", s1.check_balance(), s2.check_balance())

    print("All inheritance tests passed.")
