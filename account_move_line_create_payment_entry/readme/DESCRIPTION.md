This module adds a server action to create a payment entry for selected journal items that belong to the same partner.
It also creates a corresponding payment record, linking them together. The payment entry consists of account move lines that inherit
values from the selected journal items (such as account_id, balance, currency, etc.), along with a single credit/debit move line for the 
total balance.
