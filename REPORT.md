## PROJECT LINK: https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne
installation instructions if needed

## NOTE: the in-code conditionals whether the code is run as vulnerable or not are only for demonstration and ease of use in evaluation. When running VULNERABLE=False, the conditionals will run the fixed variant of the project while it defaults to VULNERABLE=True

## FLAW 1: Broken Access Control
LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views.py#203
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views.py#L252-L269
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views.py#L329-L351
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views.py#L373-L381

DESCRIPTION: The application does not allow to create tasks to others but will display all the saved tasks from every user to everyone. Even those not logged in. Those, who are logged in, may edit or delete any task saved in the system. This may enable cyber-bullying, sabotaging or spying.
FIX: Implement proper checks of authentication and identification to ensure access to only users own tasks.

FIX-LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views.py#L206-L212
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views.py#L249-L250
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views.py#L325-L326
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views.py#L370-L371

## FLAW 2: Injection (SQL)
LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views.py#L409-436

DESCRIPTION: Using the raw sql-querying and embedding the search field text directly to the query will cause the danger of SQL-injection. Vulnerable variant of the application has a insecure combination of raw-SQL and ORM usage since some of the queries are injection-proofed by the ORM and some aren't.
FIX: Solely using the in-built ORM will prevent the SQL-injection possibility (unless the library becomes broken) in the non-vulnerable variant of the application.

FIX-LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views.py#L440-L460

## FLAW 3: Insecure design
LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/config/settings.py#L19
- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/config/settings.py#L24

DESCRIPTION: Small configuration problems consisting of public SECRET_KEY and anyone able to connect to the service directly (ALLOWED_HOSTS = ['*']) are creating big impact. Additionally the unimplemented authentication and authorization in the application generally makes the application insecure by design. Additionally the applilcation source core mixes usage of raw SQL-queries and ORM.
FIX: Usage of .env for the SECRET_KEY, limiting the ip-address space able to connect directly to the service or using a reverse proxy in front of the service would be good starting points in securing the service. Fixing the authentication & authorization problems in the codebase will make the application even more secure. Fix of Raw-SQL / ORM -situation will increase the security even more.

## FLAW 4: Identification & authentication failures
LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views#L528-L534

DESCRIPTION: When new user registers to the application service, they are automatically given superuser permissions which will subsequently allow them to manage every aspect of the service.
FIX: Setting the is_staf and is_superuser fields 'False' will prevent users from being able to do anything without some admin to actually assess if they should have the superuser rights.

FIX-LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/core/views#L537-L543

## FLAW 5: Security logging & monitoring failures
LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/config/settings.py#L110

DESCRIPTION: Ignoring the logging in the application might be a accidental or intentional mistake. Nevertheless it will have a great impact when the logs would be needed by not having them at all. This affects both service health and cyber security aspects and is therefore crucial to be fixed.
FIX: The fix is rather simple. Easiest variant would be removing the line completely, since Django has some good presets. More extensive configuration can be done too.

FIX-LINKS:

- https://github.com/RedFoxFinn/CyberSecurityBase.ProjectOne/blob/c8739e24084fc7a5262245c6e5378e9cb0032b3d/apps/config/settings.py#L112-L131
