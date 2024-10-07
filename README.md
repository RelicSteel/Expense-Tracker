# Expense-Tracker
 My Expense Tracker made with Python and PyQt5

How to use Expense Tracker:

Firstly, there should be an Expense_Tracker.exe file, if not :(
Opening the file you will see a basic GUI pop-up - this is the login screen. Enter a username and a password then click Register to be prompted for a Successful Register. If not, feel free to use the built-in default - admin, password123.

Now, if this is your first time then you will be greeted with a message saying: "No previous expense file found, starting fresh." Just hit OK and you're now in the main file.

To enter your expenses, you will need to fill in 3 input fields:
- Description: What you bought (KFC, Shopping, Clothes)
- Amount: How much you spent (19.56 etc)
- Category: A drop-down box with options to select matching your expense.

Click Add Expense button and the data will appear in that big white void for you to see.

And that's it - the bare basics, but I'll add more - to challenge myself and to try and make this as close to a finished product as I could.

Edit and Delete Expense:

Click on the entry you wish to edit - a new pop-up box will appear - change any of the data you wish to add, you can even change the date too. Click OK - a pop-up will confirm successful edit. NOTE: this next bit is an error I forgot to fix and so is still in this version. When you click OK, a new pop-up will appear asking "Are you sure you want to edit this expense?". CLICK NO - it will not save your changes if you click yes.

Date - The date drop down's into a mini calendar, at the moment this will allow you to choose any date to add the expense under.

Delete Expense - Simply click on the entry you wish to delete, then click on the Delete expense button - confirm and it will delete.

Show Total - This will give you the total amount of all listed expense's.

Save Expenses - This will Save your list, A bit redunance as the program will save your list on close of the program.

Export to Excel - This as writen will export your list to a excel file.

Visualize Expenses - My Favorite part - will show a pie chart of all you list expense's. The data is broken into categories, So Food, Transport etc.

Toggle Dark Mode - I am a fan of Dark mode on all my device's/Software so had to add one.

Weekly/Monthly/Yearly Report - Will show you your expenses for the require date field enter, a total and by Category.

Saving files:

At the current moment I haven't added any datebase or proper security tech into this app, which means that when you create a new user and save your expenses the program will create a folder called Data. inside two new folders called Users and Expanses.

The User folder will contain only 1 json file, this file will list all users and passwords.
The expense folder will contain a json file for each user.

Where I struggled - 

While building this app I struggled a lot with implementing User's and User Login. The section where I had to save the files, and in general PyQT5. Learning a new Way to code while implementing it with python was a changlled for me at the beginning, understanding how to set a Window - give the buttons a layout and style, that was a big change from using Html/Css.

Thankfully there is lots of resourses online from Youtube videos and the offical Technical documents to AI that could read a code and tell me where I messed up with.

Conclusion and Future Updates -

This was a very challenging project. It has tested my basic understanding of Python and added new technology to my skills by learning at least the basics of PyQt5.

Now that it is done, or at least this version is done, I have a groundwork to go back to and add new things as I learn them, such as OAuth, Token-based Authentication, and Multi-factor Authentication.

As for the app itself, my biggest update for me is a more modern GUI system - I have my eye on learning Figma for this. There are also better visual charts to use and better methods of showing the data - bar charts, etc.

The biggest update, or more likely a whole app upgrade, is to link this to a bank app where you can get all your bank expenses per card you have, implement budgeting, and other bank-related app services.