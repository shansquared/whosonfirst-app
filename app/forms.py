from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required

class InputForm(Form):
	cdefault = 'Miguel Montero'
        fbdefault = 'Prince Fielder, Brandon Belt'
        sbdefault = 'Jason Kipnis'
        ssdefault = 'Elvis Andrus'
        tbdefault = 'Pablo Sandoval, David Freese, Chase Headley'
        ofdefault = 'Carlos Gonzalez, Jayson Werth, Nick Markakis, Andre Ethier, Dexter Fowler'
        catchernames = TextAreaField('C', default = cdefault, validators = [Required()])
        firstbnames = TextAreaField('1B', default = fbdefault, validators = [Required()])
        secondbnames = TextAreaField('2B', default = sbdefault, validators = [Required()])
        thirdbnames = TextAreaField('3B', default = tbdefault, validators = [Required()])
        ssnames = TextAreaField('SS', default = ssdefault, validators = [Required()])
        outfieldnames = TextAreaField('OF', default = ofdefault, validators = [Required()])

class IndividualForm(Form):
        pitchername = TextField('Pitcher', validators = [Required()])
	battername = TextField('Batter', validators = [Required()])


    
