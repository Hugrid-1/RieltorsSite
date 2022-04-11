import unittest
from flask import Flask , request , redirect , render_template
import random


app = Flask( __name__ )


@app.route( '/' )
def mainPage( ):
    return render_template("index.html")

@app.route( '/about' )
def aboutPage( ):
    return render_template("about.html")

@app.route( '/contacts' )
def contactsPage( ):
    return render_template("contacts.html")

@app.route( '/buy' )
def buyPage( ):
    return render_template("buy.html")

@app.route( '/sell' )
def sellPage( ):
    return render_template("sell.html")

@app.route( '/registration' )
def registrationPage( ):
    return render_template("registration.html")
@app.route( '/account' )
def profilePage( ):
    return render_template("accountpage.html")


if __name__ == '__main__':
    app.run( )
