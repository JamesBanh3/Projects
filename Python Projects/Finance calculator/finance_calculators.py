# import math functions
import math

#This program is an investment calculator

# Display information for user to understand to choose investment or bond

print ("investment \t- to calculate the amount of interest you'll earn on your investment\n\
bond \t\t- to calculate the amount you'll have to pay a home loan\n")

# get input from user

selection = input("Enter either 'investment' or 'bond' from \
the menu above to proceed: ").lower()

# Choosing investment
def investment():
	# Get deposit amount
	deposit = float(input("Enter deposit amount: "))
	# Get the interest rate
	interest = float(input("Enter interest rate without %: "))
	# Get years of investing
	years = int(input("Enter number of years planned of investing: "))
	# Simple or compound calculations
	print("\nHow would you like the interest to be calculated?\n\
simple interest\ncompound interest\n")
	rate = input("Enter either 'simple' or 'compound' from the menu above to proceed: ").lower()
	# calculate totals
	if rate == "simple":
		total = deposit*(1 + (interest/100)*years)
		print(f"\nThe total amount with simple interest after {years} years is {round(total,2)}.")
	elif rate == "compound":
		total = deposit * math.pow((1+interest/100),years)
		print(f"\nThe total amount with compound interest after {years} years is {round(total,2)}.")
	else:
		print("Invalid selection")


def bond():
	# Get value of house
	house = int(input("Enter present value of the house (whole numbers): "))
	# Get the interest rate
	interest = float(input("Enter interest rate without %: "))
	# Get number of months they plan to take to repay the bond
	months = int(input("Enter the number of months you plan to take to repay the bond: "))
	# Calculate the monthly repayments
	repayment = ((interest/1200)*house)/(1 - (1+(interest/1200))**(-months))
	# Print answer
	print (f"\nYour monthly repayments will be {round(repayment,2)} for {months} months.")

# Validate check

if selection == "investment":
	investment()
elif selection == "bond":
	bond()
else:
	print ("Invalid selection")

