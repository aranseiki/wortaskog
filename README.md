# wortaskog

About the project:

> A Simple Django Web App. This project is a lightweight, user-friendly Django web application designed to serve as your personal work diary. The app allows you to easily log your daily work activities, view them in a clean table format, and manage your logs with minimal effort.

#### This project is based in:

- Python + Django.
- GUI application.
- Deadline of 16 weeks.

#### URL/Route Structure: 

| URL | Path Purpose |
| --- | --- |
| /	| Home page (links to "Log Workday" and "View Work Log") |
| /log/	| Page to insert new log |
| /log/view/ | Page to view all logs |
| /log/edit/<log_id>/ | (Optional future feature) Edit existing log |
| /log/delete/<log_id>/ | (Optional future feature) Delete a log |
| /log/export/ | (Optional future feature) Export all logs as CSV |


#### Database Structure: 

| Field	| Type |
| --- | --- |
| Project | CharField |
| Month | CharField |
| Date | DateField |
| HoursWorked | CharField (you could normalize it later, but "8h", "7h30" is fine to start) |
| Observations | TextField (optional) |
| CreatedAt | DateTimeField (auto) |
| UpdatedAt | DateTimeField (auto) |


#### The application structure is:

```

    Home Page ("/") 
    |____ Insert Work Log ("/insert")
    |         |____ Select Project
    |         |____ Current Date (auto-filled)
    |         |____ Worked Hours
    |         |____ Observations
    |
    |____ View Work Logs ("/view")
    |         |____ Filter by Project
    |         |____ Filter by Month
    |         |____ List of Logs (date, hours, project, observations)
    |
    |____ Edit Existing Log ("/edit/<log_id>")
    |         |____ Same fields as Insert, but pre-filled for editing
    |
    |____ Delete Log ("/delete/<log_id>")
    |
    |____ Reports/Statistics ("/reports")
    |         |____ Hours Worked per Project (e.g., "Hours worked on Project A in March")
    |         |____ Most Worked Project of the Year (e.g., "Project B: 200 hours")
    |         |____ Summary of Hours Worked (monthly, quarterly, yearly)
    |
    |____ System Log ("/log")
    |         |____ Success Log (logs of successful operations)
    |         |____ Error Log (logs of failed operations, e.g., failed data entries) 

```
