# 👩‍🏫 Woodcock-Johnson IV Report Automator 🤖

This app is a tool to automatically generate and fill out reports for student's with an [IEP](https://en.wikipedia.org/wiki/Individualized_Education_Program)

The reports use data gathered and generated under the [Woodcock–Johnson Tests of Cognitive Abilities (WJ IV)](https://riversideinsights.com/woodcock_johnson_iv) framework to assess a student's cognitive abilities.

This application can be used by educators **under the following assumptions:**

1. Your school uses Riverside Score to generate Woodcock–Johnson Tests of Cognitive Abilities

1. You have 1+ saved Examinees in the "My Recent Examinees" table 👇

![My Recent Examinees](/readme_images/woodcock_johnson_dashboard.png?raw=true "My Recent Examinees")

1. You want to run reports for WJ IV Tests of Achievement Form A and Extended (Opposed to WJ IV Tests of Oral Language, etc.)

> :warning: After generating the reports you must manually edit the test dates **(DATES)** text in the doc which appears in this line:!
`Administered by: {{ resource_sepcialist_name }} DATES`