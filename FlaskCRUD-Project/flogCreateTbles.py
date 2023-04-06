from sqliteConnect import *

cursor.execute(
    """
CREATE TABLE "flogBlogTbl" (
	"UBR"   	    INTEGER NOT NULL UNIQUE,
	"Author"	    VARCHAR(30),
	"Blog Title"	TEXT(200),
	"Body"	        LONGTEXT,
	PRIMARY KEY("UBR" AUTOINCREMENT)
)"""
)

#...............................
cursor.execute("""
CREATE TABLE "flogUserTbl" (
	"User_ID" 		INTEGER NOT NULL UNIQUE, 
    "Username"	    VARCHAR(30) NOT NULL UNIQUE,
	"Password"	    VARCHAR(30),
	"First name"	VARCHAR(30),
	"Surname"	    VARCHAR(30),
	"Email address"	VARCHAR(100) NOT NULL UNIQUE,
	PRIMARY KEY("User_ID" AUTOINCREMENT)
)"""
)