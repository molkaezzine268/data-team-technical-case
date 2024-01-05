# **DAT-01** / Verify the sequentiality of invoices

## Context
The Accounting Team has reminded us that it is crucial for invoice references to be consecutive: they must follow the pattern `JMPXXXXX` where `XXXXX` is a number (padded with `0` to ensure a fixed-size reference).


## Action
Create a test to ensure that there are no gaps in the invoices. The test should be at the `WARN` level and should not block all the steps.


## Tips
1) You can rely on the `reference` column of the [`intermediate__invoices`](../../dbt/models/intermediate/intermediate__invoices.sql) model to retrieve the list of references
2) You can write your test in [this file](../../dbt/tests/intermediate/invoices/intermediate__invoices__references_should_be_sequential.sql)


