This module adds a server action to create a payment for selected moves that belong to the same partner.
The payment entry consists of account move lines that inherit values from the account move lines of the selected moves
(such as account_id, balance, currency, etc.), along with a single outstanding account move line for the total balance.
