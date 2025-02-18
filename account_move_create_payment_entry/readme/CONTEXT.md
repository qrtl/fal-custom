There are cases where payments are combined when purchasing from the
same partner using a currency different from the company’s currency.
When these bills belong to different months and have varying exchange
rates, the system automatically creates an exchange difference for them,
which is not needed in this scenario.

Example Scenario
~~~~~~~~~~~~~~~~

* Company currency: JPY (Japanese Yen)
* Exchange rates:
    * January 2025: 1 USD = 140 JPY
    * February 2025: 1 USD = 150 JPY

Created Bills
* January 2025
    * Bill001: 100 USD
    * Exchange Rate: 140 JPY/USD
    * Balance: ¥14,000
* February 2025
    * Bill002: 100 USD
    * Exchange Rate: 150 JPY/USD
    * Balance: ¥15,000

Payment Process
A USD 200 payment was created and matched with Bill001 (Jan) and Bill002 (Feb).
Due to the exchange rate difference between January and February, the system automatically generates an exchange difference of ¥1,000 for Bill001.
