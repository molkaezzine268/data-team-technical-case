# **DAT-04** / ⚠️ October 2023 is missing in the turnover report! 


## Context
The KPI Monthly Turnover is monitored by the CFO to ensure the health of Jump.

The CFO has noticed that there is no line for October 2023.


## Action
This needs to be corrected by still displaying a line for this month despite the lack of activity.


## Tips
1) The _Monthly Turnover_ is computed in [this file](../../dbt/models/marts/kpi/marts__kpi__monthly_turnover.sql)
2) The [dbt-utils](https://github.com/dbt-labs/dbt-utils) package (and its `date_spine` function) have been added as dependency to the project