class Email(object):
    # Each instance of an email will be stored as an object with thier own values
    def __init__(self, from_address, subject_line, email_contents):
        self.from_address = from_address
        self.subject_line = subject_line
        self.email_contents = email_contents
        self.has_been_read = False
        self.is_spam = False
    
    # fuctions in each email that can be called and change the emails variable
    def mark_as_read(self):
        self.mark_as_read = True
        
    def mark_as_spam(self):
        self.is_spam = True

class Inbox:
    # Inbox object will contains a list of emails
    
    def __init__(self):
        self.list_of_emails = []

    # Add email will create an email object and add that email to the inbox
    def add_email(self, from_address, subject_line, email_contents):
        new_email = Email(from_address, subject_line,email_contents)
        self.list_of_emails.append(new_email)
        
    # List all email objects that match the senders address
    def list_messages_from_sender(self, sender_address):
        for count, email in enumerate(self.list_of_emails):
            # Check for matching address
            if email.from_address == sender_address:
                # print emails with their index
                print(f"{count}    {email.subject_line}")

    # Get the email with senders address and the index from user
    def get_email(self, sender_address, index):
        # Find the email
        email = self.list_of_emails[index]
        # Check if thwe email is from the right sender
        if email.from_address == sender_address:
            # Display email in user friendly interface
                print(f'''
From:     {email.from_address}
Subject:  {email.subject_line}
{email.email_contents}''')
        # Mark the email been read
        email.has_been_read = True
    
    # Let user mark email as spam
    def mark_as_spam(self, sender_address, index):
        # Find the email
        email = self.list_of_emails[index]
        if email.from_address == sender_address:
            # call the fuction within the email object
            email.mark_as_spam()
    
    def get_unread_emails(self):
        # Find the all email that are unread
        for count, email in enumerate(self.list_of_emails):
            if email.has_been_read == False:
                print(f"{count}    {email.subject_line}")
    
    def get_spam_emails(self):
        # Find the all email that are spam
        for count, email in enumerate(self.list_of_emails):
            if email.is_spam == True:
                print(f"{count}    {email.subject_line}")
    
    def delete(self, sender_address, index):
        # Find the email
        email = self.list_of_emails[index]
        if email.from_address == sender_address:
            # delete the email
            self.list_of_emails.pop(index)
            del email
            
      
usage_message = '''
Welcome to the email system! What would you like to do?

s - send email.
l - list emails from a sender.
r - read email.
m - mark email as spam.
gu - get unread emails.
gs - get spam emails.
d - delete email.
e - exit this program.
'''


#An Email Simulation

 
user_choice = ""
#Create a user inbox
user_inbox = Inbox()

#Load emails from a txt file
with open("emails.txt", 'r') as emails_file:
    emails_data = emails_file.read().split("\n")
    emails_data = [e for e in emails_data if e != ""]

# Get data from an email file upon program load
for index , email_str in enumerate (emails_data):
    email_components = email_str.split(";") 
    from_address = email_components[0]
    subject_line = email_components[1]
    email_contents = email_components[2]
    has_been_read = email_components[3]
    is_spam = email_components[4]
    
    # add the email to the inbox
    user_inbox.add_email(from_address,subject_line,email_contents)
    if has_been_read == "True": user_inbox.list_of_emails[index].has_been_read = True
    if is_spam == "True": user_inbox.list_of_emails[index].is_spam = True

# Save emails function
def save_emails_to_file():
    with open("emails.txt", "w") as emails_file:
        emails_list_to_write = []
        for e in user_inbox.list_of_emails:
            str_attrs = [
                e.from_address,
                e.subject_line,
                e.email_contents,
                str(e.has_been_read),
                str(e.is_spam),
            ]
            emails_list_to_write.append(";".join(str_attrs))
        emails_file.write("\n".join(emails_list_to_write))       
    
while True:
    user_choice = input(usage_message).strip().lower()
    if user_choice == "s":
        # Send an email (Create a new Email object)
        sender_address = input("Please enter the address of the sender\n:")
        subject_line = input("Please enter the subject line of the email\n:")
        contents = input("Please enter the contents of the email\n:")
        
        
        # Now add the email to the Inbox
        user_inbox.add_email(sender_address,subject_line,contents)
        

        # Print a success message
        save_emails_to_file()
        print("Email has been added to inbox.")
      
    elif user_choice == "l":
        # List all emails from a sender_address
        sender_address = input("Please enter the address of the sender\n:")

        # Now list all emails from this sender
        user_inbox.list_messages_from_sender(sender_address)
        
    elif user_choice == "r":
        # Read an email
        # Step 1: show emails from the sender
        sender_address = input("Please enter the address of the sender of the email\n:")

        # Step 2: show all emails from this sender (with indexes)
        user_inbox.list_messages_from_sender(sender_address)
        # Step 3: ask the user for the index of the email
        email_index = int(input("Please enter the index of the email that you would like to read\n:"))

        # Step 4: display the email
        user_inbox.get_email(sender_address,email_index)
        save_emails_to_file()
        
    elif user_choice == "m":
        # Mark an email as spam
        # Step 1: show emails from the sender
        sender_address = input("Please enter the address of the sender of the email\n:")

        # Step 2: show all emails from this sender (with indexes)
        user_inbox.list_messages_from_sender(sender_address)
        # Step 3: ask the user for the index of the email
        email_index = int(input("Please enter the index of the email to be marked as spam\n:"))

        # Step 4: mark the email as spam
        user_inbox.mark_as_spam(sender_address,email_index)
        # Step 5: print a success message
        print("Email has been marked as spam")
        save_emails_to_file()

    elif user_choice == "gu":
        # List all unread emails
        user_inbox.get_unread_emails()
        
    elif user_choice == "gs":
        # List all spam emails
        user_inbox.get_spam_emails()
        
    elif user_choice == "e":
        print("Goodbye")
        break
    
    elif user_choice == "d":
        # Delete an email
        # Step 1: show emails from the sender
        sender_address = input("Please enter the address of the sender of the email\n:")

        # Step 2: show all emails from this sender (with indexes)
        user_inbox.list_messages_from_sender(sender_address)
        # Step 3: ask the user for the index of the email
        email_index = int(input("Please enter the index of the email to be deleted\n:"))

        # Step 4: delete the email
        user_inbox.delete(sender_address,email_index)
        # Step 5: print a success message
        print("Email has been deleted")
        save_emails_to_file()

        
    else:
        print("Oops - incorrect input")
