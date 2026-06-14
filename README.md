# Library API project

A library management system that allows for book inventory management, subscription management, and smart lending system management that prevents duplication, loss of books, and more.

## Docker setup with MySql:
first time:
```
$ docker run --name mysql-library-api -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASW=library_db -d mysql:8
```

if exist:
```
docker start mysql-library-api
```

## Functions
 * main
 ### Books management:
 * creat book
 * get books - all / by id / (by gern?)
 * book detail update
 * borrow/return book
### Members managemant:
 * get members - all / by id
 * create and update member
 * de/activate member
 ### Reports functions:
 * summery
 * books by gern
 * top member

## Project structure
    library-api/
    │
    │
    ├── main.py
    ├── database/
    │   ├── db_connection.py
    │   ├── book_db.py
    │   └── member_db.py
    ├── routes/
    │   ├── book_routes.py
    │   ├── member_routes.py
    │   └── report_routes.py
    ├── logs/
    │   └── app.log
    │
    ├── README.md
    ├── requirements.txt
    └── .gitignore


## DB structure:
### books table:
contains:

    columns:
        - id: primary key
        - title: book title, not null, max 50 chars
        - author: author name, not null, max 50 chars
        - gern: ENUM of Fiction | Non-Fiction | Science | History | Other, any other value returns error, not null
        - is availble: TRUE or FALSE, not null
        - borrowed by member id: member id that borrowed the book, null if availble


### members table:
contains:

    columns:
        - id: primary key
        - name: member name, not null, max 50 chars
        - email: member email, not null, unique
        - is active: TRUE or FALSE, if FALSE can't borrow, not null
        - total borrows: count the member borrows and adds 1 on any new borrow


## System rules
    - create book: user sends title/author/gern and the system adds TRUE to 'is active' column and id to 'borrowed by' column
    - gern: one of Fiction | Non-Fiction | Science | History | Other, any other value returns error, must validate use in POST and PATCH
    - member create: user sends name and email and the system will add TRUE to 'is active' column and total_borrowed=0
    - email: must be unique and returns error if it dosen't unique
    - deactive member: if the 'is active' = FALSE, the user will not be allowed to borrow a book
    - unavailble book: if 'is active' = FALSE the book can't be borrowed
    - max books: the maximum number of books that can be borrow to member is 3
    - return book: only the member that borrowed this book can return the book


## Endpoints
### books:
| Method | Endpoint | תיאור |
| --- | --- | --- |
| POST | /books | יצירת ספר |
| GET | /books | כל הספרים |
| GET | /books/{id} | ספר לפי ID |
| PATCH | /books/{id} | עדכון ספר |
| PATCH | /books/{id}/borrow/{member_id} | השאלת ספר לחבר |
| PATCH | /books/{id}/return/{member_id} | | החזרת ספר מחבר |

### members:
| Method | Endpoint | תיאור |
| --- | --- | --- |
| POST | /members | יצירת חבר |
| GET | /members | כל החברים |
| GET | /members/{id} | חבר לפי ID |
| PATCH | /members/{id} | עדכון חבר |
| PATCH | /members/{id}/deactivate | השבתת חבר |
| PATCH | /members/{id}/activate | הפעלת חבר |

### reports:
| Method | Endpoint | תיאור |
| --- | --- | --- |
| GET | /reports/summary | דוח כללי |
| GET | /reports/books-by-genre | ספרים לפי ז'אנר |
| GET | /reports/top-member | החבר הכי פעיל |


## System flow
> the user run the setup call:

* create db if not exist >>>

![aaa](src/library-api.drawio.svg)


## How to run

```uvicorn main:app --reload```