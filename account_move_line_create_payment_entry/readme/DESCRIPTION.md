This module adds a server action to create a payment entry for selected journal items that belong to the same partner and to reconcile
the selected journal items with the journal items of the created entry. The payment entry consists of account move lines that inherit 
values from the selected journal items (such as account_id, balance, currency, etc.), along with a single credit move line for the total 
balance.
