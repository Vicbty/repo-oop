# UML practice · Exo 1 · Hospital Management System

Business specification (from the course gist):

- A patient posts a health problem online on the platform.
- The organizer reads the problem and consults a doctor.
- The doctor provides a prescription / solution.
- The organizer sends the prescription to the patient.
- The patient pays by check, cash or credit card.
- The organizer forwards the payment to the doctor.
- The organizer also acts as administrator: maintains the database, updates the system, issues member IDs and passwords.

---

## Task 1 · Basic class diagram (Patient, Doctor, Organizer)

```mermaid
classDiagram
    class Patient {
        -int patient_id
        -str name
        -str email
        -str password
        +post_problem(description) None
        +view_prescriptions() list
        +pay(amount, method) None
    }
    class Doctor {
        -int doctor_id
        -str name
        -str specialty
        -str password
        +review_problem(problem_id) None
        +write_prescription(problem_id, text) None
        +receive_payment(amount) None
    }
    class Organizer {
        -int organizer_id
        -str name
        -str password
        +read_problem(problem_id) None
        +consult_doctor(doctor, problem_id) None
        +send_prescription(patient) None
        +forward_payment(doctor, amount) None
        +create_member(name) int
    }
    Organizer "1..*" -- "0..*" Patient : manages
    Organizer "0..*" -- "1..*" Doctor : consults
    Patient "0..*" -- "0..*" Doctor : is treated by
```

At this stage the problem, the prescription and the payment are only parameters; task 2 turns them into classes.

---

## Task 2 · Complete class diagram (6 classes + payment types)

```mermaid
classDiagram
    class Patient {
        -int patient_id
        -str name
        -str address
        +post_problem(description) HealthProblem
        +pay(prescription, method) Payment
    }
    class Doctor {
        -int doctor_id
        -str name
        -str specialty
        +write_prescription(problem) Prescription
        +receive_payment(amount) None
    }
    class Organizer {
        -int organizer_id
        -str name
        +assign_doctor(problem, doctor) None
        +send_prescription(prescription) None
        +forward_payment(payment) None
        +create_member(name) int
    }
    class HealthProblem {
        -int problem_id
        -str description
        -datetime submitted_at
        +assign_doctor(doctor) None
        +attach_prescription(prescription) None
    }
    class Prescription {
        -int prescription_id
        -str content
        -float fee
        +summary() str
    }
    class Payment {
        <<abstract>>
        -float amount
        -datetime paid_at
        +process()* bool
    }
    class Cash {
        +process() bool
    }
    class Check {
        -str check_number
        +process() bool
    }
    class CreditCard {
        -str card_last4
        +process() bool
    }

    Patient "1" *-- "0..*" HealthProblem : posts
    HealthProblem "1" *-- "0..1" Prescription : answered by
    Doctor "1" -- "0..*" Prescription : writes
    Organizer "1" -- "0..*" HealthProblem : handles
    Prescription "1" -- "0..1" Payment : is paid by
    Patient "1" -- "0..*" Payment : makes
    Organizer "1" -- "0..*" Payment : forwards
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- CreditCard
```

Design choices:

- **Composition** Patient → HealthProblem: a health problem does not exist without its patient.
- **Composition** HealthProblem → Prescription: a prescription answers one problem (0..1 until the doctor replies).
- **Inheritance** for the payment types: each one overrides `process()` (polymorphism).

### Sequence diagram · a patient submits a problem, receives a prescription and pays

```mermaid
sequenceDiagram
    actor Patient
    participant O as :Organizer
    participant P as p:HealthProblem
    participant D as :Doctor
    participant R as rx:Prescription
    participant C as pay:CreditCard

    Patient->>O: 1: post_problem(description)
    O->>P: 2: «create» HealthProblem(description)
    O->>O: 3: read_problem(p)
    O->>D: 4: consult(p)
    D->>R: 5: «create» Prescription(content, fee)
    D-->>O: 6: rx
    O->>P: 7: attach_prescription(rx)
    O-->>Patient: 8: send_prescription(rx)
    Patient->>O: 9: pay(rx.fee, "card")
    O->>C: 10: «create» + process()
    C-->>O: 11: True / False
    alt payment accepted
        O->>D: 12: forward_payment(amount)
        O-->>Patient: 13: receipt
    else payment refused
        O-->>Patient: 14: payment_refused
    end
```

---

## Task 3 · Advanced

### Class diagram additions

```mermaid
classDiagram
    class User {
        <<abstract>>
        -int user_id
        -str name
        -str password_hash
        +login(password) bool
        +logout() None
    }
    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer

    class ProblemStatus {
        <<enumeration>>
        PENDING
        IN_REVIEW
        RESOLVED
    }
    class HealthProblem {
        -ProblemStatus status
        -datetime created_at
        -datetime updated_at
        +change_status(status) None
    }
    HealthProblem ..> ProblemStatus : uses

    class Prescription {
        -datetime issued_at
        -Prescription previous
    }
    Prescription "0..1" -- "0..*" Prescription : renews

    class PaymentStrategy {
        <<interface>>
        +pay(amount) bool
    }
    class CashPayment {
        +pay(amount) bool
    }
    class CheckPayment {
        +pay(amount) bool
    }
    class CreditCardPayment {
        +pay(amount) bool
    }
    PaymentStrategy <|.. CashPayment
    PaymentStrategy <|.. CheckPayment
    PaymentStrategy <|.. CreditCardPayment

    class Payment {
        -float amount
        -str status
        -datetime created_at
        +execute() bool
    }
    Payment "1" --> "1" PaymentStrategy : uses
```

### System Sequence Diagram 1 · Patient registration

```mermaid
sequenceDiagram
    actor Organizer
    participant S as :System
    Organizer->>S: 1: create_member(name, email)
    S-->>Organizer: 2: member_id, temporary_password
    Organizer->>S: 3: send_credentials(member_id)
    S-->>Organizer: 4: ok
```

### System Sequence Diagram 2 · Consultation flow

```mermaid
sequenceDiagram
    actor Patient
    actor Organizer
    actor Doctor
    participant S as :System
    Patient->>S: 1: submit_problem(description)
    S-->>Patient: 2: problem_id (status = PENDING)
    Organizer->>S: 3: review_problem(problem_id)
    Note over S: status = IN_REVIEW
    Organizer->>S: 4: assign_doctor(problem_id, doctor_id)
    Doctor->>S: 5: write_prescription(problem_id, content)
    Organizer->>S: 6: send_prescription(problem_id)
    Note over S: status = RESOLVED
    S-->>Patient: 7: prescription
```

### System Sequence Diagram 3 · Payment processing

```mermaid
sequenceDiagram
    actor Patient
    actor Organizer
    participant S as :System
    Patient->>S: 1: pay(prescription_id, method, amount)
    alt payment accepted
        S-->>Patient: 2: receipt
        Organizer->>S: 3: forward_payment(doctor_id, amount)
        S-->>Organizer: 4: transfer_confirmation
    else payment refused
        S-->>Patient: 5: payment_refused
    end
```

### Questions to consider

- **A patient consulting multiple doctors**: make the HealthProblem–Doctor link `0..*` on the doctor side, or add a `Consultation` class (problem, doctor, date, opinion) to keep the history of each opinion.
- **Reusable prescriptions**: separate the reusable content (a `PrescriptionTemplate` / treatment) from the prescription issued to one patient on one date, or use the `previous` reference for renewals.
- **Design pattern for payment**: **Strategy** (one interchangeable strategy per payment method), often combined with a **Factory** that picks the strategy from "cash", "check" or "card".
- **Data integrity during payments**: atomic transaction (payment and forwarding succeed or fail together), a payment status (PENDING / PAID / FAILED), a unique payment id to avoid duplicates (idempotency), a timestamped log, and a check of the amount against the prescription fee.
