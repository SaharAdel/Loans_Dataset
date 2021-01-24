# Loans_Dataset

### Summary of the dataset
The dataset contains 113,937 loans since 2005/2014 with 81 variables on each loan, including loan amount, current loan status, borrower income, borrower occupation, and many others.<br>
It's contains qualititave varibles such as loan status, loan category, borrower state and occupation and others. Also, it's contains quantitave variables such as loan amount, term, borrower income and others. <br>
[Prosper Loans Dataset Source](https://video.udacity-data.com/topher/2019/April/5ca78b26_dataset-project-communicate-data-findings/dataset-project-communicate-data-findings.pdf) and [Variables Description](https://docs.google.com/spreadsheets/d/1gDyi_L4UvIrLTEC6Wri5nbaMmkGmLQBk-Yx3z0XDEtI/edit#gid=0) 

### Plan of doing analysis
The plan starts with selecting some of the interesting features from the datset and investigate the relationship between them, and how they affect on the loans. <br>
The features are:
- Some of basic data: loan key, loan date creation, payment terms(months), loan status and category.
- Some of borrower data: borrower state, borrower occupation and if own a home.
- Some of income data: borrower range income, income verifiable and the monthly income.
- some of prosper loans (if there): prosper loans number, number of billed, payment status (on time, late < month or late > month)

### Main findings from the exploratory data analysis
- The most exist loans status are current, and completed. 
- The most exist loans categories are for debt consolidation, auto, home improvement, respectively. 
- The most exist borrowers state, CA by 13% followed by TX, FL and NY equally by 6%. 
- The most exist borrower's occupation, professional followed by computer programmer and executive.
- There is 50.5% of borrowers they owner home while there is 49.5% of them they didn't own.
- The range of most loans amount is between 5000 and 15000.
- There is a positive and weak relationship between the loan amount and the borrower income. 
- Finally, if the prosper loans was a lot, that will lead to late occurring in payment, either in less than a month or plus a month.
