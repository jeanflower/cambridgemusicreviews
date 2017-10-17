from django.http import HttpResponse

def message(request):
    message = "<h1>What's the page about?</h1>"
    message = message + "Happy Birthday Laurence<br>"
    message = message + "<a href = http://jeanflower.pythonanywhere.com/laurence/messages>click here for a longer message!</a><p>"
    message = message + "<h1>Encode anything!</h1>"
    url = 'http://jeanflower.pythonanywhere.com/laurence/codes/hello/0'
    message = message + "Go to <a href = '"+url+"'>"+url+"</a><br>"
    url = 'http://jeanflower.pythonanywhere.com/laurence/codes/teacakes/1'
    message = message + "Go to <a href = '"+url+"'>"+url+"</a><br>"
    url = 'http://jeanflower.pythonanywhere.com/laurence/codes/tubemap/2'
    message = message + "Go to <a href = '"+url+"'>"+url+"</a><br>"
    message = message + "Explore your own words and numbers by adding them"
    message = message + " after http://jeanflower.pythonanywhere.com/laurence/codes/"
    message = message + "<p><p>"
    message = message + "<h1>What's under the hood?</h1>"
    url = 'http://pythonfiddle.com/'
    message = message + "To play with the code, go to <a href = '"+url+"'>"+url+"</a><br>"
    message = message + "copy and paste in this code, hit \"run\":<br>"
    message = message + "<pre>\
# define the task we want to perform<br>\
uncoded_message = \"happy birthday laurence\"<br>\
letter_shift = 1<br>\
# first set up an empty string to add characters to<br>\
# this will become the coded message after we've added characters<br>\
# one by one<br>\
message_coded = \"\"<br>\
<br>\
# look at each character of the uncoded message, one by one<br>\
# (use lowercase characters)<br>\
for character in uncoded_message.lower():<br>\
    # keep spaces as spaces, don't encode those to anything<br>\
    if character == ' ':<br>\
        # add a space onto our coded message<br>\
        message_coded = message_coded + ' '<br>\
        # go back to the 'for' and continue onto our next letter<br>\
        continue<br>\
    # turn this character into a number; the computer transkates<br>\
    # a-> 97, b->98 and so on<br>\
    number_form = ord(character)<br>\
    # it's easier to understand if a->0, b->1 and so on<br>\
    # so alter the number so that a->0, b->1 and so on<br>\
    number_form = number_form - 97<br>\
    # alter the number to apply the code; add letter_shift<br>\
    number_form = number_form + letter_shift<br>\
    # if numbers became more than 25 (e.g. maybe z would go to more)<br>\
    # wrap the numbers back using modulo arithmetic<br>\
    number_form = number_form % 26<br>\
    # now the number is between 0 and 25<br>\
    # we'll convert this number back to a letter again but<br>\
    # the computer wants to translate 97->a, 98->b etc<br>\
    # so change 0->97, 1->98, etc.<br>\
    number_form = number_form + 97<br>\
    # convert the number back to a character and add it to the end<br>\
    # of the encoded message<br>\
    message_coded = message_coded + chr(number_form)<br>\
<br>\
print(message_coded)<br>\
</pre>"
    message = message + "<p><p>"
    message = message + "Have fun! Love from Jean and Gem."
    return HttpResponse(message)


def make_coded_message(uncoded_message, shift):
    # first set up an empty string to add characters to
    # this will become the coded message after we've added characters
    # one by one
    message_coded = ""

    # look at each character of the uncoded message, one by one
    # use lowercase characters
    for character in uncoded_message.lower():
        if character == ' ':
            message_coded = message_coded + ' '
            continue
        # turn this character into a number; the natural translation is
        # a-> 97, b-> 98 and so on
        number_form =  ord(character)
        # alter the number so that a->0, b-> 1 and so on
        number_form = number_form - 97
        # alter the number to apply the code; add shift
        number_form = number_form + shift
        # if numbers became more than 25 (e.g. z would go to more)
        # wrap the numbers back using modulo arithmetic
        # now all our letters are between 0 and 25
        number_form = number_form % 26
        # finally, the computer wants to map 97->a, 98->b etc
        number_form = number_form + 97
        # convert the number back to a character and add it to the end
        # of the encoded message
        message_coded = message_coded + chr(number_form)
    return message_coded

def codes(request, message, shift):
    return HttpResponse(make_coded_message(message, int(shift)))
    
def messages(request):
    message = "happy birthday laurence"
    response = "<pre>"
    for shift in range(0, 27):
        response = response + make_coded_message(message, shift)
        response = response + "<br>"
    response = response + "</pre>"
    return HttpResponse(response)


