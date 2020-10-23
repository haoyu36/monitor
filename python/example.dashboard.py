from grafanalib.core import (
    Alert, AlertCondition, Dashboard, Graph,
    GreaterThan, OP_AND, OPS_FORMAT, Row, RTYPE_SUM, SECONDS_FORMAT,
    SHORT_FORMAT, single_y_axis, Target, TimeRange, YAxes, YAxis
)


dashboard = Dashboard(
    title="Prometheus Http Requests",
    rows=[
        Row(panels=[
          Graph(
            title="prometheus 200",
            dataSource='204',
            targets=[
                Target(
                    expr='sum(prometheus_http_requests_total{code="200"})',
                    legendFormat="200",
                    refId='A',
                ),
            ],
            yAxes=YAxes(
                YAxis(format=OPS_FORMAT),
                YAxis(format=SHORT_FORMAT),
            ),
            ),
          Graph(
              title="prometheus all",
              dataSource='204',
              targets=[
                  Target(
                    expr='sum(prometheus_http_requests_total{})',
                    legendFormat="all",
                    refId='A',
                  ),
              ],
              yAxes=single_y_axis(format=SECONDS_FORMAT),
          ),
        ]),
    ],
).auto_panel_ids()
