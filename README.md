# Instructions to run:
1. you can start a virtual environment here at the Outdoor-Buddies-web-app:
```bash
python -m venv venv
source venv/Scripts/activate (for windiows einvironments)

 ```
2. navigate to Outdoorbuddies_root
3. run:
```bash
pip install -r requirements.txt
```
4. This will download all the dependencies. You can make migrations if you want for using your own database. but there is a starting database on the github.
5. run the app:
```bash
python manage.py runserver
```
# Outdoor-Buddies-web-app
A Django framework website designed for CSCE A490: Web development
## the instructions for this project are as follows:
```
● Users must be able to register, login and logout.
● Usera must be able to create, store, and edit a profile, including a picture. Upload
the picture by browsing the file system, not by entering a URL.
● Users must be able to ask for a password reset, and email sent. (Easy to send via
gmail; we will cover that in a future class).
● Application must be deployed to the internet and use a non-sqlite database.
● Application must support search.
● Application needs to “seed” at least one table from a file.
● Application must be easy to navigate.
● Application must have (at a minimum) a Home Page, a Contact Us page, and a footer
at the bottom of each page with some information and some links; also, as
mentioned above, there will be pages for a user’s profile, search results, etc.
● Application needs some sort of “call to action.” This is the heart of the matter: An
item to sell, a book to check out from the library, a recipe to a cookbook, a sports
team (roster, results, schedule) etc. Of course, if you have a library, you need to be
able to add new books; if you have an online cookbook, you need a way to add
recipes; etc. In other words, you cannot rely on using the Django admin panel for
adding data.
```
you can read the full project description [Here](https://github.com/AKashton/Outdoor-Buddies-web-app/blob/main/2023%20Assignment%207_%20Final%20Project%20(1).pdf)
