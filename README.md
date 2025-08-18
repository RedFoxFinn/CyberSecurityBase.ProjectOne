# Cyber Security Base - Course project 1

This repository is housing the course project of mine for the University of Helsinki course CSB.

Goal is to build a web app that's faulty and the provide the fixes. Faulty in this context means that it should contain at least 5 of the vulnerability categories from the [OWASP Top 10](https://owasp.org/Top10/) (2025 version could be already released. If that's true, try [this](https://owasp.org/www-project-top-ten/2021/) link instead).

```Make sure that (these are the most common reasons for project being rejected)

- The flaws are real, and not just hypothetical, and the fixes are included in the code.
- The flaws are in the code or in installation script, for example, having admin/admin user in the database is not enough.
- The fix actually fixes the problem, and not just hide it.
- Screenshots are included in the repository.
- There is a backend, and the flaws/fixes occur in the backend. Remember that the user can manipulate the frontend as much as possible.
```

## Selected vulnerability categories

### A01 - Broken access control
[description](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)

### A03 - Injection
[description](https://owasp.org/Top10/A03_2021-Injection/)

### A04 - Insecure design
[description](https://owasp.org/Top10/A04_2021-Insecure_Design/)

### A07 - Identification and authentication failures
[description](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)

### A08 - Software and data integrity failures
[description](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)

## Technically

The project is implemented in Python(3) using [Django](https://www.djangoproject.com/) framework and its features.

The code was written with Visual Studio Code as the IDE and in CUBBLI OS (Uni. Helsinki flavor of the Ubuntu).

## Report

The Essay / report is in separate file [here](REPORT.md). This is due to the fact that it is easier to copy/paste for submission form of the course.

Report states where in the code the vulnerabilities are implemented AND how or where the fix is provided.

- Approx. 1000 words, hard limit 800 -- 1500 words


### Screenshots

```In addition, you should add screenshots for each flaw demonstrating the effect of the flaw before and after the fix. Typically, the screenshots should be of your browser. Make sure that the screenshots do not contain any sensitive information. You can have multiple screenshots demonstrating the effect. Store them in a screenshots folder of your repository and name them flaw-1-before-1.png, flaw-1-after-1.png, and so on.```

So.. the screenshots we're talking about? As files, they're [here](screenshots/).

As extension to the report they are provided as a separate `.md` [here](SCREENSHOTS.md).