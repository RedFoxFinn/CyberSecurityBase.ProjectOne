## PROJECT LINK:
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne

## Link to this report:
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/REPORT.md

## NOTE 1

This report is purely textual, the screenshots are found separately as an extension to this report. Also partly because the submission field does not allow images, just text.

Screenshots in a directory:
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/tree/main/screenshots
Screenshots as a markdown file:
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/SCREENSHOTS.md

## NOTE 2

The in-code conditionals whether the code is run as vulnerable or not are only for demonstration and ease of use in evaluation. When running VULNERABLE=False, the conditionals will run the fixed variant of the project while it defaults to VULNERABLE=True if not given any additional CLI arguments (just the VULNERABLE=True/False implemented in this one..)

## NOTE 3

In the project there is a handy script to get things easily started: setup.sh.

When using it, on linux CLI type `chmod +x setup.sh && ./setup.sh` in the directory you have downloaded the source code and it will setup the virtual environment, install dependencies and create some simple sample data for testing purposes.

In the end it will give instructions on how to run the application.

## Disclaimer

Since I've been doing this project on the side of "Theory of computation", I might have forgot at some point what I was doing with some part of the application. Please forgive me.

## FLAW 1: Broken Access Control
LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views.py#203
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views.py#L252-L269
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views.py#L329-L351
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views.py#L373-L381

DESCRIPTION: The application does not allow to create tasks to others but will display all the saved tasks from every user to everyone in the vulnerable application variant. Even to those who are not logged in.
Those, who are logged in, may edit or delete any task saved in the system. This may enable ie. cyber-bullying, sabotaging or spying.
FIX: Implement proper checks of authentication and identification to ensure access to only users own tasks. In fixed application variant only the user may see, access, edit or delete the tasks they have entered to the application.

FIX-LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views.py#L206-L212
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views.py#L249-L250
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views.py#L325-L326
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views.py#L370-L371

## FLAW 2: Injection (SQL)
LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views.py#L409-436

DESCRIPTION: Using the raw sql-querying and embedding the search field string value directly to the query will cause the danger of SQL-injection in the vulnerable application variant. Vulnerable variant of the application has a insecure combination of raw-SQL querying and ORM usage since some of the queries are injection-proofed by the ORM and some aren't. This may happen due to different people of the team building different parts while using different approaches in the development.
FIX: Solely using the in-built ORM in the querying logic will prevent the SQL-injection possibility (unless the library itself becomes broken or vulnerable, but that's a completely different story) in the non-vulnerable variant of the application.

FIX-LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views.py#L440-L460

## FLAW 3: Insecure design
LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/config/settings.py#L19
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/config/settings.py#L24

DESCRIPTION: Small configuration problems consisting of public SECRET_KEY and anyone able to connect to the service directly (ALLOWED_HOSTS = ['*']) are creating big impact in the vulnerable application variant.
Additionally the poorly implemented authentication and authorization in the application logic generally makes the application insecure by design. Since the insecure design is actually broad concept, most of the things that are wrong in the vulnerable variant could be considered to be included in this category. But they are also included in others as well.
FIX: Usage of .env for the SECRET_KEY, limiting the ip-address space able to connect directly to the service or using a reverse proxy or some other port-forwarding method in front of the service would be good starting points in securing the service. Fixing the authentication & authorization problems in the codebase will make the application even more secure.

## FLAW 4: Identification & authentication failures
LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views#L528-L534

DESCRIPTION: When new user registers to the application service that's implementation of the vulnerable application variant, they are automatically given superuser permissions, which will subsequently allow them to manage every aspect of the service approachable from the network.
FIX: Setting the is_staff and is_superuser fields 'False' in the fixed variant will prevent users from being able to do anything harmful without some real admin to actually assess if they are to be trusted and if they should have the superuser rights. Something to be considered in real world applications that's not implemented here is that when registering to the service, the email should be verified as well. Otherwise anybody could be using any email, really.

FIX-LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/core/views#L537-L543

## FLAW 5: Security logging & monitoring failures
LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/config/settings.py#L110

DESCRIPTION: Ignoring the logging in the application might be a accidental or intentional mistake. Nevertheless it will have a great impact when the logs would be needed by not having them at all. This affects both service health and cyber security aspects and is therefore crucial to be fixed. In the vulnerable application variant the logging is virtually completely disabled by a single setting.
FIX: The fix is rather simple. Easiest variant would be removing the line completely, since Django has some good presets. More extensive configuration can be done too and in out fixed variant there is a small but customized setup. When the logging is properly implemented in any service, troubleshooting becomes easier. Whether it is to investigate a cyber-incident, system malfunctioning or hunting some extreme edge-case software bug causing issues with only a handful of users.

FIX-LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/main/apps/config/settings.py#L112-L131
