# UML practice · Exo 2 · ABCD Records

Business specification (from the course gist): ABCD Records is a mail-order company selling CDs and tapes at discount prices to record club members.

- Only members can place orders; non-members receive a membership application form.
- Two member classes: Royal (discounts + priority) and Regular.
- Royal members can order unavailable items.
- Payment methods: cash, check, bank draft.
- The Order Processing Clerk handles verification and processing.
- The Collection Department Clerk handles payments.
- All orders are saved to a daily records file.

> Use case diagrams are drawn with a Mermaid flowchart: the rectangle is the system boundary, rounded shapes are use cases, actors stay outside the boundary, dashed arrows are «include» / «extend».

---

## Level 1

### Task 1.1 · Simple use case diagram

```mermaid
flowchart LR
    M["Actor: Member"]
    C["Actor: Order Processing Clerk"]
    subgraph SYS["ABCD Records Order System"]
        PO(["Place Order"])
        MP(["Make Payment"])
        VM(["Verify Membership"])
        PR(["Process Order"])
    end
    M --- PO
    M --- MP
    C --- VM
    C --- PR
    PO -. «include» .-> VM
```

### Task 1.2 · Basic class diagram

```mermaid
classDiagram
    class Member {
        -int member_id
        -str name
        -str address
        -str email
        +place_order(items) Order
        +make_payment(order, amount) None
    }
    class Order {
        -int order_id
        -date order_date
        -str status
        -float total
        +add_item(item_id, qty) None
        +compute_total() float
    }
    class OrderProcessingClerk {
        -int clerk_id
        -str name
        +verify_membership(member) bool
        +process_order(order) None
    }
    Member "1" -- "0..*" Order : places
    OrderProcessingClerk "1" -- "0..*" Order : processes
    OrderProcessingClerk ..> Member : verifies
```

---

## Level 2

### Task 2.1 · Complete use case diagram

```mermaid
flowchart LR
    M["Actor: Member"]
    RM["Actor: Royal Member"]
    NM["Actor: Non-Member"]
    OPC["Actor: Order Processing Clerk"]
    CDC["Actor: Collection Department Clerk"]
    RM -- "generalization (is a)" --> M
    subgraph SYS["ABCD Records"]
        PO(["Place Order"])
        VM(["Verify Membership"])
        VIA(["Verify Item Availability"])
        AD(["Apply Discount"])
        OUI(["Order Unavailable Items"])
        PRO(["Process Order"])
        PI(["Print Invoice"])
        PSL(["Print Shipping List"])
        MP(["Make Payment"])
        SMA(["Send Membership Application"])
    end
    M --- PO
    M --- MP
    RM --- OUI
    NM --- SMA
    OPC --- PRO
    CDC --- MP
    PO -. «include» .-> VM
    PO -. «include» .-> VIA
    PRO -. «include» .-> PI
    PRO -. «include» .-> PSL
    AD -. «extend» .-> PO
    OUI -. «extend» .-> PO
    SMA -. «extend» .-> VM
```

- «include» = mandatory: placing an order always verifies membership and availability; processing always prints the invoice and the shipping list.
- «extend» = optional: the discount and unavailable items only apply to Royal members; the application form is only sent when the membership check fails.

### Task 2.2 · Complete class diagram

```mermaid
classDiagram
    class Member {
        <<abstract>>
        -int member_id
        -str name
        -str address
        +discount()* float
        +place_order() Order
    }
    class RoyalMember {
        -float discount_rate
        +discount() float
        +can_order_unavailable() bool
    }
    class RegularMember {
        +discount() float
    }
    Member <|-- RoyalMember
    Member <|-- RegularMember

    class NonMember {
        -str name
        -str address
        +request_membership() None
    }
    class MembershipApplication {
        -int application_id
        -date sent_date
        +submit() None
    }
    NonMember "1" -- "0..1" MembershipApplication : receives

    class Item {
        <<abstract>>
        -int item_id
        -str title
        -str artist
        -float price
        -int stock
        +is_available(qty) bool
    }
    class CD {
        -int nb_tracks
    }
    class Tape {
        -int duration_min
    }
    Item <|-- CD
    Item <|-- Tape

    class Order {
        -int order_id
        -date order_date
        -str status
        +add_line(item, qty) None
        +total() float
    }
    class OrderLine {
        -int quantity
        -float unit_price
        -bool backordered
        +subtotal() float
    }
    class Invoice {
        -int invoice_id
        -float amount
        +print() None
    }
    class ShippingList {
        -int list_id
        -date shipping_date
        +print() None
    }

    class Payment {
        <<abstract>>
        -float amount
        -date date
        +process()* bool
    }
    class Cash
    class Check {
        -str check_number
    }
    class BankDraft {
        -str draft_number
    }
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft

    class OrderProcessingClerk {
        +verify_membership(member) bool
        +check_availability(order) bool
        +process_order(order) None
    }
    class CollectionDepartmentClerk {
        +record_payment(payment) None
    }
    class DailyRecordsFile {
        -date date
        +save(order) None
    }

    Member "1" -- "0..*" Order : places
    Order "1" *-- "1..*" OrderLine
    OrderLine "0..*" -- "1" Item
    Order "1" *-- "1" Invoice
    Order "1" *-- "1" ShippingList
    Order "1" -- "0..*" Payment : paid by
    OrderProcessingClerk "1" -- "0..*" Order : processes
    CollectionDepartmentClerk "1" -- "0..*" Payment : handles
    DailyRecordsFile "1" o-- "0..*" Order : records
```

### Sequence diagram · a Royal member orders 2 CDs (one unavailable) and pays by check

```mermaid
sequenceDiagram
    actor RM as RoyalMember
    participant OPC as :OrderProcessingClerk
    participant O as o:Order
    participant CD1 as cd1:CD
    participant CD2 as cd2:CD
    participant CDC as :CollectionDepartmentClerk
    participant CHK as chk:Check
    participant F as :DailyRecordsFile

    RM->>OPC: 1: place_order([cd1, cd2])
    OPC->>OPC: 2: verify_membership(member)
    OPC->>O: 3: «create»
    OPC->>CD1: 4: is_available(1)
    CD1-->>OPC: 5: True
    OPC->>O: 6: add_line(cd1, 1)
    OPC->>CD2: 7: is_available(1)
    CD2-->>OPC: 8: False
    opt member is Royal
        OPC->>O: 9: add_line(cd2, 1, backordered=True)
    end
    OPC->>O: 10: total()
    O-->>OPC: 11: amount (Royal discount applied)
    OPC-->>RM: 12: invoice
    RM->>CDC: 13: pay(amount, "check")
    CDC->>CHK: 14: «create» + process()
    CHK-->>CDC: 15: True
    CDC->>F: 16: save(o)
    CDC-->>RM: 17: receipt
```

---

## Level 3 · Advanced sequences

### Membership verification (success and failure)

```mermaid
sequenceDiagram
    actor Cust as Customer
    participant OPC as :OrderProcessingClerk
    participant REG as :MemberRegistry
    participant APP as app:MembershipApplication
    Cust->>OPC: 1: place_order(customer_id, items)
    OPC->>REG: 2: find(customer_id)
    REG-->>OPC: 3: member or None
    alt member found
        OPC-->>Cust: 4: membership verified, order continues
    else not a member
        OPC->>APP: 5: «create»
        OPC-->>Cust: 6: send(app), order refused
    end
```

### Payment processing (all types)

```mermaid
sequenceDiagram
    actor M as Member
    participant CDC as :CollectionDepartmentClerk
    participant PF as :PaymentFactory
    participant P as p:Payment
    participant B as :Bank
    participant O as o:Order
    M->>CDC: 1: pay(order, method, amount)
    CDC->>PF: 2: create(method, amount)
    PF-->>CDC: 3: p (Cash, Check or BankDraft)
    CDC->>P: 4: process()
    alt method = check
        P->>B: 5: clear(check_number)
        B-->>P: 6: cleared
    else method = bank draft
        P->>B: 7: verify(draft_number)
        B-->>P: 8: ok
    else method = cash
        Note over P: no external call
    end
    P-->>CDC: 9: success
    CDC->>O: 10: mark_paid()
    CDC-->>M: 11: receipt
```

### Item reordering for Royal members

```mermaid
sequenceDiagram
    actor RM as RoyalMember
    participant OPC as :OrderProcessingClerk
    participant I as item:CD
    participant S as :Supplier
    participant L as line:OrderLine
    participant SL as :ShippingList
    OPC->>I: 1: is_available(qty)
    I-->>OPC: 2: False
    opt member is Royal
        OPC->>S: 3: reorder(item, qty)
        S-->>OPC: 4: expected_date
        OPC->>L: 5: set_backordered(expected_date)
        OPC-->>RM: 6: notify(expected_date)
        S-)OPC: 7: delivery(item, qty)
        OPC->>SL: 8: «create» + print()
    end
```

### Complete order processing flow

```mermaid
sequenceDiagram
    actor M as Member
    participant OPC as :OrderProcessingClerk
    participant O as o:Order
    participant I as :Item
    participant INV as :Invoice
    participant SL as :ShippingList
    participant CDC as :CollectionDepartmentClerk
    participant F as :DailyRecordsFile
    M->>OPC: 1: place_order(items)
    OPC->>OPC: 2: verify_membership(member)
    OPC->>O: 3: «create»
    loop for each item
        OPC->>I: 4: is_available(qty)
        I-->>OPC: 5: True / False
        OPC->>O: 6: add_line(item, qty)
    end
    OPC->>O: 7: total()
    O-->>OPC: 8: amount
    OPC->>INV: 9: «create» + print()
    OPC->>SL: 10: «create» + print()
    M->>CDC: 11: pay(amount, method)
    CDC-->>M: 12: receipt
    CDC->>F: 13: save(o)
```
